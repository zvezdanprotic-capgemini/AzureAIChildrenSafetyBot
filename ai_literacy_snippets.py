SNIPPETS = [
    "Did you know? I don't have feelings; I use patterns in data to answer questions!",
    "AI tip: If something feels unsafe or confusing, talk to a trusted adult.",
    "I'm a program, not a person. I can't keep secrets, so don't share private info.",
]


def get_snippet(index: int) -> str:
    if not SNIPPETS:
        return ""
    return SNIPPETS[index % len(SNIPPETS)]
