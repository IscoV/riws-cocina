def first_or_none(el):
    return el[0] if el and len(el) > 0 else None


def n_or_none(el, n):
    return el[n] if el and len(el) > n else None


def clear_spaces(text):
    return " ".join(text.split()) if text else None
