"""
Compatibility helpers for Starlette TemplateResponse API changes.

Starlette < 0.36 uses the positional dict form:
    TemplateResponse("name.html", {"request": req, "key": val})

Starlette >= 0.36 deprecated that and prefers:
    TemplateResponse(request=req, name="name.html", context={"key": val})

This project's venv runs Starlette 0.27 (old API).
The system Python used by pytest runs Starlette 1.10 (new API).

`tpl()` normalises the call so both versions work.
"""
import starlette

_STARLETTE_NEW_API = tuple(int(x) for x in starlette.__version__.split(".")[:2]) >= (0, 36)


def tpl(templates, name: str, request, context: dict | None = None):
    """
    Return a TemplateResponse that works on Starlette 0.27 and 1.10+.

    Usage:
        return tpl(templates, "index.html", request, {"result": result})
    """
    ctx = context or {}
    if _STARLETTE_NEW_API:
        return templates.TemplateResponse(request=request, name=name, context=ctx)
    else:
        return templates.TemplateResponse(name, {"request": request, **ctx})
