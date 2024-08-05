from .level import FeedbackLevel


def extract(onemap: dict):
    """Extract feedback from a test-feedback map.

    Returns
    -------
    feedback: str

    """
    assert 'feedback' in onemap
    level = onemap['level'] if 'level' in onemap else FeedbackLevel.LOWEST
    feedback = onemap['feedback']
    func_with_params = onemap['function'] if 'function' in onemap else None
    if func_with_params is not None:
        feedback = fill_content(feedback, func_with_params)
    return feedback, level


def fill_content(feedback: str, func_with_params) -> str:
    """Fill {content} in the feedback message."""
    assert func_with_params is not None
    if isinstance(func_with_params, dict):
        func = func_with_params.pop('name')
        params = func_with_params.pop('params')
        feedback = feedback.format(content=func(params=params))
    else:
        # in case there is no params
        func = func_with_params
        feedback = feedback.format(content=func())
    return feedback


def _context(qn, attr):
    """Fetch context given question number (qn) and attribute."""
    if attr is not None and qn in attr:
        attr_context = attr[qn]
    else:
        attr_context = None
    return attr_context


def context(qn, maps):
    """Fetch question, canonical, and student answer contexts.

    All contexts are collected inside the user defined module `maps`.

    """
    ctx = {}
    if "context" in maps.__dict__:
        mapsctx = maps.__dict__["context"]
        for ele in mapsctx:
            _ctx = _context(qn, mapsctx[ele])
            if _ctx is not None:
                ctx |= {
                    ele: _context(qn, mapsctx[ele])
                }
    return ctx
