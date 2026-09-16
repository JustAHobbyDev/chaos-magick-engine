"""Strict public contracts. All authority and operation IDs belong to the engine."""
import json
import math
from dataclasses import dataclass


class Invalid(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Invalid(message)


def fields(value, names):
    require(type(value) is dict and set(value) == set(names),
            f"expected exactly fields {sorted(names)}")


STRING_LIMIT = 12000  # Operator command bodies; model strings are bounded from the configured reply size.
ENVELOPE_CHARS = 2000  # Room the JSON envelope and short fields need inside one reply.


def string_bound(output_chars):
    """The largest string a reply may carry: the whole-reply bound less envelope room, so the two never disagree."""
    return output_chars - ENVELOPE_CHARS


def string(value, bound=STRING_LIMIT):
    require(type(value) is str and value, "expected nonempty string")
    require(len(value) <= bound, f"string of {len(value)} characters exceeds the {bound}-character bound")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        raise Invalid("text must be valid UTF-8") from None


def label(value, bound=STRING_LIMIT):
    """Titles and names: short identifiers, never a second content channel."""
    string(value, bound)
    require(len(value) <= 200, "expected label of at most 200 characters")


OUTCOMES = ("completed", "abandoned", "deferred")


def outcome(value, bound=None):
    require(value in OUTCOMES, f"outcome must be exactly one of {'/'.join(OUTCOMES)}; put any account in the intent")


def strings(value, bound=STRING_LIMIT):
    require(type(value) is list and len(value) <= 100, "expected bounded list")
    for item in value:
        string(item, bound)


def integer(value, bound=None):
    require(type(value) is int and 0 < value <= 2**63 - 1, "expected positive 64-bit integer")


def reference(value, bound=STRING_LIMIT):
    fields(value, ("id", "version"))
    string(value["id"], bound)
    integer(value["version"])


def references(value, bound=STRING_LIMIT):
    require(type(value) is list and len(value) <= 100, "expected reference list")
    for item in value:
        reference(item, bound)


def wake_condition(value, bound=None):
    require(type(value) is dict and value.get("kind") in ("timer", "event"), "unsupported wake condition")
    if value["kind"] == "timer":
        fields(value, ("kind", "at"))
        at = value["at"]
        # Bounded before any float conversion: an oversized integer must be a rejection, not a fault.
        require(type(at) in (int, float) and 0 < at < 2**53, "timer must be a finite positive timestamp")
    else:
        fields(value, ("kind", "event"))
        require(value["event"] == "operator", "unsupported wake event")


# Arguments are exact; references carry immutable versions, never model authority.
CONTRACTS = {
    "begin_working": dict(question=string, intended_product=string, motivation=string),
    "select_working": dict(working_id=string),
    "read_corpus": dict(entry_id=string),
    "read_artifact": dict(artifact_id=string, version=integer),
    "define_frame": dict(name=label, entities=strings, relations=strings,
                         assumptions=strings, moves=strings, invocation=string),
    "enter_frame": dict(frame_id=string, version=integer),
    "write_artifact": dict(title=label, kind=string, content=string,
                           source_refs=references, parent_refs=references),
    "revise_artifact": dict(artifact_id=string, expected_version=integer,
                            content=string, change_note=string),
    "leave_frame": dict(product_refs=references, extraction_note=string),
    "assimilate": dict(assessment_ref=reference, reply=string, self_account_change=string,
                       doctrine_changes=strings, next_pursuit=string),
    "finish_working": dict(outcome=outcome, product_refs=references, unresolved_questions=strings),
    "wait": dict(reason=string, wake_condition=wake_condition),
}
KINDS = {"exegesis", "theory", "rite", "transmission", "agent_seed", "frame", "research_note"}
PHASES = {
    "begin_working": {None, "settled"},
    "select_working": {None, "orientation", "assimilation", "settled"},
    "read_corpus": {None, "orientation", "exploration", "assimilation", "settled"},
    "read_artifact": {None, "orientation", "exploration", "assimilation", "settled"},
    "define_frame": {"orientation", "exploration", "assimilation"},
    "enter_frame": {"orientation", "assimilation"},
    "write_artifact": {"orientation", "exploration", "assimilation"},
    "revise_artifact": {"orientation", "exploration", "assimilation"},
    "leave_frame": {"exploration"},
    "assimilate": {"assimilation"},
    "finish_working": {"orientation", "exploration", "assimilation"},
    "wait": {None, "orientation", "exploration", "assimilation", "settled"},
}


def parse(raw, limit):
    require(type(raw) is str, "output character bound exceeded: reply is not text")
    require(len(raw) <= limit, f"output character bound exceeded: reply of {len(raw)} characters, bound {limit}")
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "duplicate JSON field")
            result[key] = value
        return result
    try:
        return json.loads(raw, object_pairs_hook=pairs,
                          parse_constant=lambda _: (_ for _ in ()).throw(Invalid("nonfinite JSON")))
    except (ValueError, RecursionError) as exc:
        raise Invalid(f"invalid JSON: {exc}") from exc


def proposal(raw, limit):
    value = parse(raw, limit)
    bound = string_bound(limit)
    fields(value, ("intent", "operation"))
    named("intent", string, value["intent"], bound)
    op = value["operation"]
    fields(op, ("name", "arguments"))
    string(op["name"], bound)
    require(op["name"] in CONTRACTS, "unknown operation")
    schema = CONTRACTS[op["name"]]
    fields(op["arguments"], schema)
    for key, validator in schema.items():
        named(key, validator, op["arguments"][key], bound)
    return value


def named(key, validator, value, bound):
    """A rejection names the argument it concerns; the model cannot repair what it cannot locate."""
    try:
        validator(value, bound)
    except Invalid as exc:
        remedy = ("; shorten it, or write the product as more than one artifact, each within the bound, "
                  "later parts naming earlier ones in parent_refs") if key == "content" and "exceeds" in str(exc) else ""
        raise Invalid(f"{key}: {exc}{remedy}") from None


def assessment(raw, limit):
    value = parse(raw, limit)
    bound = string_bound(limit)
    fields(value, ("examined_refs", "observations", "source_relationship", "serves_sought", "claim_status",
                   "possible_developments", "limits"))
    named("examined_refs", references, value["examined_refs"], bound)
    for key in ("observations", "possible_developments", "limits"):
        named(key, strings, value[key], bound)
        require(bool(value[key]), f"{key} cannot be empty")
    named("source_relationship", string, value["source_relationship"], bound)
    named("serves_sought", string, value["serves_sought"], bound)
    require(value["claim_status"] in ("supported_by_supplied_material", "speculative", "unexamined"),
            "invalid claim status")
    return value


@dataclass(frozen=True)
class Config:
    episode_steps: int
    call_timeout: float
    retry_limit: int
    input_chars: int
    output_chars: int
    standing_calls: int
    standing_usage_chars: int
    shutdown_timeout: float

    @classmethod
    def from_dict(cls, data):
        fields(data, cls.__dataclass_fields__)
        for key, value in data.items():
            if key in ("call_timeout", "shutdown_timeout"):
                require(type(value) in (int, float) and math.isfinite(value) and 0 < value <= 3600,
                        f"invalid {key}")
            else:
                require(type(value) is int and 0 <= value <= 10**9, f"invalid {key}")
                require(value > 0 or key == "retry_limit", f"{key} must be positive")
        require(data["output_chars"] > ENVELOPE_CHARS, f"output_chars must exceed the {ENVELOPE_CHARS}-character envelope allowance")
        return cls(**data)
