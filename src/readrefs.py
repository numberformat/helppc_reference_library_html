from common import TopicRef

FILENAME_REPLACEMENTS = {
    ord(" "): "_",
    ord(","): "-",
    ord("."): "_",
    ord("("): "-",
    ord(")"): "-"
}


def fname(ref: bytes) -> str:
    return "".join(
        FILENAME_REPLACEMENTS[b]
        if b in FILENAME_REPLACEMENTS
        else chr(b).lower()
        for b in ref
    )


def readrefs(section_file: str, section_slug: str) -> dict[str, TopicRef]:
    refs: dict[str, str] = {}

    with open(section_file, "rb") as stream:
        while line := stream.readline():
            if line.startswith(b":"):
                line = line[1:].rstrip()
                byte_refs = line.split(b":")
                if byte_refs:
                    topic_file = f"{fname(byte_refs[0])}.html"
                    for byte_ref in byte_refs:
                        topic_ref = byte_ref.decode().lower()
                        refs[topic_ref] = TopicRef(topic_file, section_slug)

    return refs
