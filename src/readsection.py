from common import TopicRef, Section

BYTE_REPLACEMENTS = {
    0xb3: "│",
    0xc0: "└",
    0xc4: "─",
    0xda: "┌",
    0xc5: "┼",
    0xd9: "┘",
    0xb4: "┤",
    0xc2: "┬",
    0xc1: "┴",
    0xbf: "┐",
    0xc3: "├",
    0xf9: "∙"
}


def bytestostr(seq: bytes) -> str:
    return "".join(
        BYTE_REPLACEMENTS[b]
        if b in BYTE_REPLACEMENTS
        else chr(b)
        for b in seq
    )


def replace_links(line: str, refs: dict[str, TopicRef]) -> str:
    replaced = []
    pos = 0
    while pos < len(line):
        if line[pos] == "~":
            # Discard first tilde
            pos += 1
            if line[pos] == "~":
                # If we get a second tilde, write the tilde
                replaced.append("~")
            else:
                link = ""
                while line[pos] != "~":
                    link += line[pos]
                    pos += 1
                # Insert the link only if it's present in the refs
                if link.lower() in refs:
                    topic_ref = refs[link.lower()]
                    href = f"../{topic_ref.section}/{topic_ref.filename}"
                    replaced.append(f"<a href='{href}'>{link}</a>")
                else:
                    print(f"Link '{link}' not in refs, writing plain text")
                    replaced.append(link)
        else:
            replaced.append(line[pos])
        pos += 1
    return "".join(replaced)


def readsection(file: str, refs: dict[str, TopicRef]) -> Section:
    section_title = None
    topics = {}
    current_ref = None

    with open(file, "rb") as stream:
        while line := stream.readline():
            line = replace_links(bytestostr(line.rstrip()), refs)
            if line.startswith("@"):
                section_title = line[1:]
            elif line.startswith(":"):
                # First tag in line
                current_ref = line[1:].split(":")[0].lower()
                topics[current_ref] = ""
            elif line.startswith("^"):
                topics[current_ref] += f"<h2>{line[1:]}</h2>\n"
            elif line.startswith("%"):
                topics[current_ref] += f"<b>{line[1:]}</b>\n"
            else:
                topics[current_ref] += f"{line}\n"

    return Section(section_title, topics)
