def first_or_none(el):
    return el[0] if el and len(el) > 0 else None


def clear_spaces(text):
    return " ".join(text.split()) if text else None
