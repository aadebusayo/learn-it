from .models import SourceChunk


def chunk_text(source_id: str, text: str, chunk_size: int = 1400, overlap: int = 160) -> list[SourceChunk]:
    if not text.strip():
        return []

    chunks: list[SourceChunk] = []
    start = 0
    index = 0
    text_length = len(text)

    while start < text_length:
        target_end = min(start + chunk_size, text_length)
        end = _find_boundary(text, start, target_end)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(
                SourceChunk(
                    id=f"{source_id}-chunk-{index + 1}",
                    source_id=source_id,
                    index=index,
                    text=chunk,
                    start_offset=start,
                    end_offset=end,
                )
            )
            index += 1
        if end >= text_length:
            break
        start = max(end - overlap, start + 1)

    return chunks


def _find_boundary(text: str, start: int, target_end: int) -> int:
    if target_end >= len(text):
        return len(text)

    paragraph = text.rfind("\n\n", start, target_end)
    if paragraph > start + 200:
        return paragraph

    sentence = max(text.rfind(". ", start, target_end), text.rfind("? ", start, target_end), text.rfind("! ", start, target_end))
    if sentence > start + 200:
        return sentence + 1

    space = text.rfind(" ", start, target_end)
    if space > start + 200:
        return space

    return target_end
