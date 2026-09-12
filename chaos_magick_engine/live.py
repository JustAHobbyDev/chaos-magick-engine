"""Live provider boundary: the Claude Messages API behind the engine's async adapter contract.

The anthropic SDK is imported only when a client is constructed here, so the deterministic core,
its tests, and the offline demo keep no runtime dependency. Nothing in this module touches engine
state; it turns a compiled request into one provider call and reports raw output, metadata, and
usage in the engine's own unit (Unicode characters). Provider tokens are recorded as metadata.
"""
from .adapters import Reply, Request

DEFAULT_MODEL = "claude-opus-5"
SYSTEM = ("You are invoked by the Chaos Magick Engine. The user message is a JSON request the engine "
          "compiled: its `instructions`, `authority`, and `response_contract` (or, for the examiner role, "
          "the contract in `instructions`) govern your reply. Reply with exactly one JSON object and nothing "
          "else: no code fences, no prose before or after it. Creative text belongs inside the JSON arguments.")


def read_key(path):
    key = open(path, encoding="utf-8").read().strip()
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
