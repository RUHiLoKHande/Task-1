def chunk_text(text, max_len=1000):
    words = text.split()
    chunks, chunk = [], []

    for word in words:
        chunk.append(word)
        if len(" ".join(chunk)) >= max_len:
            chunks.append(" ".join(chunk))
            chunk = []
    if chunk:
        chunks.append(" ".join(chunk))
    return chunks
