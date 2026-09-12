"""Live provider boundary: the Claude Messages API and the OpenAI Responses API behind the engine's
async adapter contract.

Provider SDKs are imported only when a client is constructed here, so the deterministic core, its
tests, and the offline demo keep no runtime dependency. Nothing in this module touches engine state;
each adapter turns a compiled request into one provider call and reports raw output, metadata, and
usage in the engine's own unit (Unicode characters). Provider tokens are recorded as metadata.
"""
from .adapters import Reply, Request

DEFAULT_MODEL = "claude-opus-5"
OPENAI_MODEL = "gpt-5.6-sol"
SYSTEM = ("You are invoked by the Chaos Magick Engine. The user message is a JSON request the engine "
          "compiled: its `instructions`, `authority`, and `response_contract` (or, for the examiner role, "
          "the contract in `instructions`) govern your reply. Reply with exactly one JSON object and nothing "
          "else: no code fences, no prose before or after it. Creative text belongs inside the JSON arguments.")


def read_key(path):
    with open(path, encoding="utf-8") as handle:
        key = handle.read().strip()
    if not key:
        raise ValueError(f"empty key file: {path}")
    return key


class ClaudeAdapter:
    """One Messages API call per invocation. Cancellation is cooperative through the SDK's async client."""

    def __init__(self, model=DEFAULT_MODEL, effort="high", fallbacks=True, timeout=600.0,
                 key_file=None, client=None):
        self.model = model
        self.effort = effort
        self.fallbacks = fallbacks
        if client is None:
            import anthropic  # Deferred: only a live run needs the SDK.
            kwargs = {"timeout": timeout}
            if key_file:
                kwargs["api_key"] = read_key(key_file)
            client = anthropic.AsyncAnthropic(**kwargs)
        self.client = client

    def build(self, request: Request):
        params = {"model": self.model, "max_tokens": 16000, "system": SYSTEM,
                  "messages": [{"role": "user", "content": request.compiled}],
                  "output_config": {"effort": self.effort},
                  "metadata": {"user_id": f"invocation:{request.invocation_id}"}}
        if self.fallbacks:
            # Policy declines re-run on Anthropic's recommended model; the serving model is recorded.
            params["betas"] = ["server-side-fallback-2026-07-01"]
            params["fallbacks"] = "default"
        return params

    async def invoke(self, request: Request) -> Reply:
        response = await self.client.beta.messages.create(**self.build(request))
        text = "".join(block.text for block in response.content if getattr(block, "type", None) == "text")
        usage = getattr(response, "usage", None)
        metadata = {"provider": "anthropic", "synthetic": False, "requested_model": self.model,
                    "model": getattr(response, "model", None), "effort": self.effort,
                    "request_id": getattr(response, "_request_id", None),
                    "stop_reason": getattr(response, "stop_reason", None),
                    "tokens": {key: getattr(usage, key, None) for key in
                               ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")},
                    "fallbacks": [{"from": b.from_.model, "to": b.to.model} for b in response.content
                                  if getattr(b, "type", None) == "fallback"]}
        details = getattr(response, "stop_details", None)
        if details is not None:
            metadata["stop_details"] = {"category": getattr(details, "category", None),
                                        "explanation": getattr(details, "explanation", None)}
        if metadata["stop_reason"] == "refusal":
            text = ""  # A decline is recorded as an empty reply; the engine rejects it explicitly.
        return Reply(text, metadata, len(request.compiled) + len(text))


class OpenAIAdapter:
    """One Responses API call per invocation, on the flex service tier by default.

    Flex processing is priced at batch rates and may answer slowly or refuse capacity with a 429.
    The SDK retries that a bounded number of times; if capacity is still unavailable and fallbacks
    are on, the same request is re-issued once on the standard tier and the change is recorded, in
    the same way the Claude adapter records a server-side model fallback. The response is not stored
    on the provider side: the engine's invocation record is the record.
    """

    def __init__(self, model=OPENAI_MODEL, effort="high", service_tier="flex", fallbacks=True, timeout=900.0,
                 key_file=None, client=None, max_output_tokens=32000):
        self.model = model
        self.effort = effort
        self.service_tier = service_tier
        self.fallbacks = fallbacks
        self.max_output_tokens = max_output_tokens
        if client is None:
            import openai  # Deferred: only a live run needs the SDK.
            kwargs = {"timeout": timeout, "max_retries": 3}
            if key_file:
                kwargs["api_key"] = read_key(key_file)
            client = openai.AsyncOpenAI(**kwargs)
        self.client = client

    def build(self, request: Request, service_tier=None):
        # The ceiling covers reasoning tokens as well as the visible reply, which the engine bounds
        # separately in characters; exhausting it is reported as an incomplete response, not hidden.
        return {"model": self.model, "instructions": SYSTEM, "input": request.compiled,
                "reasoning": {"effort": self.effort}, "service_tier": service_tier or self.service_tier,
                "max_output_tokens": self.max_output_tokens, "store": False}

    async def invoke(self, request: Request) -> Reply:
        fallbacks = []
        try:
            response = await self.client.responses.create(**self.build(request))
        except Exception as exc:
            # Capacity refusals on the flex tier are not charged; the standard tier is the recorded fallback.
            if not (self.fallbacks and self.service_tier == "flex" and type(exc).__name__ == "RateLimitError"):
                raise
            fallbacks.append({"from": "flex", "to": "auto", "reason": str(exc)[:500]})
            response = await self.client.responses.create(**self.build(request, service_tier="auto"))
        text, refusals = "", []
        for item in getattr(response, "output", None) or []:
            if getattr(item, "type", None) != "message":
                continue
            for part in getattr(item, "content", None) or []:
                kind = getattr(part, "type", None)
                if kind == "output_text":
                    text += part.text
                elif kind == "refusal":
                    refusals.append(part.refusal)
        usage = getattr(response, "usage", None)
        input_details = getattr(usage, "input_tokens_details", None)
        output_details = getattr(usage, "output_tokens_details", None)
        incomplete = getattr(response, "incomplete_details", None)
        metadata = {"provider": "openai", "synthetic": False, "requested_model": self.model,
                    "model": getattr(response, "model", None), "effort": self.effort,
                    "request_id": getattr(response, "_request_id", None),
                    "response_id": getattr(response, "id", None),
                    "requested_service_tier": self.service_tier,
                    "service_tier": getattr(response, "service_tier", None),
                    "status": getattr(response, "status", None),
                    "incomplete_reason": getattr(incomplete, "reason", None) if incomplete is not None else None,
                    "tokens": {"input_tokens": getattr(usage, "input_tokens", None),
                               "output_tokens": getattr(usage, "output_tokens", None),
                               "cached_tokens": getattr(input_details, "cached_tokens", None),
                               "reasoning_tokens": getattr(output_details, "reasoning_tokens", None)},
                    "fallbacks": fallbacks}
        if refusals:
            # A decline is recorded as an empty reply; the engine rejects it explicitly.
            metadata["stop_details"] = {"category": "refusal", "explanation": " ".join(refusals)[:2000]}
            text = ""
        return Reply(text, metadata, len(request.compiled) + len(text))
