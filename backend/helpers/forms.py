import inspect
from typing import Type

from fastapi import Form
from pydantic import BaseModel
from pydantic.fields import ModelField


def form_body(cls):
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            inspect.Parameter(
                model_field.alias,
                inspect.Parameter.POSITIONAL_ONLY,
                default=Form(... if model_field.required else model_field.default,
                             description=model_field.field_info.description),
                annotation=model_field.outer_type_,
            ) for model_field in cls.__fields__.values()
        ]
    )
    return cls
