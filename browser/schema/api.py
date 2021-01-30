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
            "mode" : {
                "type" : "string",
                "enum" : ["single", "multi"]
            },
            "plot1": {
                "type": "array",
                "items": {
                    "type": "number"
                }
            },
            "plot2": {
                "type": "array",
                "items": {
                    "type": "number"
                }
            }
        },
        "additionalProperties": False,
        "required": ["mode", "plot1"]
    }
    try:
        validate(data, schema)
    except ValidationError:
        abort(400)
