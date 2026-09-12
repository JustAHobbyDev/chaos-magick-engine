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


def string(value):
    require(type(value) is str and 0 < len(value) <= 12000, "expected nonempty bounded string")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        raise Invalid("text must be valid UTF-8") from None


def label(value):
    """Titles and names: short identifiers, never a second content channel."""
    string(value)
    require(len(value) <= 200, "expected label of at most 200 characters")


OUTCOMES = ("completed", "abandoned", "deferred")


def outcome(value):
    require(value in OUTCOMES, f"outcome must be exactly one of {'/'.join(OUTCOMES)}; put any account in the intent")


def strings(value):
    require(type(value) is list and len(value) <= 100, "expected bounded list")
    for item in value:
        string(item)


def integer(value):
    require(type(value) is int and 0 < value <= 2**63 - 1, "expected positive 64-bit integer")


def reference(value):
    fields(value, ("id", "version"))
    string(value["id"])
    integer(value["version"])


def references(value):
    require(type(value) is list and len(value) <= 100, "expected reference list")
    for item in value:
        reference(item)


def wake_condition(value):
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
    "assimilate": dict(assessment_ref=reference, self_account_change=string,
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
    require(type(raw) is str and len(raw) <= limit, "output character bound exceeded")
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
    fields(value, ("intent", "operation"))
    string(value["intent"])
    op = value["operation"]
    fields(op, ("name", "arguments"))
    string(op["name"])
    require(op["name"] in CONTRACTS, "unknown operation")
    schema = CONTRACTS[op["name"]]
    fields(op["arguments"], schema)
    for key, validator in schema.items():
        validator(op["arguments"][key])
    return value


def assessment(raw, limit):
    value = parse(raw, limit)
    fields(value, ("examined_refs", "observations", "source_relationship", "claim_status",
                   "possible_developments", "limits"))
    references(value["examined_refs"])
    for key in ("observations", "possible_developments", "limits"):
        strings(value[key])
        require(bool(value[key]), f"{key} cannot be empty")
    string(value["source_relationship"])
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
        return cls(**data)
