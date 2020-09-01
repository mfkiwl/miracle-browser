from flask import abort
from jsonschema import validate, ValidationError


def compare_experiments(data):
    schema = {
        "type": "object",
        "properties": {
            "target1": {"type": "string"},
            "target2": {"type": "string"}
        },
        "additionalProperties": False,
        "required": ["target1", "target2"]
    }
    try:
        validate(data, schema)
    except ValidationError:
        abort(400)


def compare_results(data):
    schema = {
        "type": "object",
        "properties": {
            "target1": {"type": "string"},
            "target2": {"type": "string"},
            "experiment": {"type": "string"}
        },
        "additionalProperties": False,
        "required": ["target1", "target2", "experiment"]
    }
    try:
        validate(data, schema)
    except ValidationError:
        abort(400)


def compare_plots(data):
    schema = {
        "type": "object",
        "properties": {
            "trace_ids": {
                "type": "array",
                "items": {
                    "type": "number"
                }
            }
        },
        "additionalProperties": False,
        "required": ["trace_ids"]
    }
    try:
        validate(data, schema)
    except ValidationError:
        abort(400)
