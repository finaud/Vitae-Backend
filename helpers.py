import wikipedia

def get_wikipedia_excerpt(name: str, sentences: int) -> str:
    # Return a wikipedia excerpt of sentences length on name
    return wikipedia.summary(name, sentences=sentences)