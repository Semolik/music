from fastapi import Form


def form_body(cls):
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(...) if arg.default !=
                        None else Form(None))
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls
