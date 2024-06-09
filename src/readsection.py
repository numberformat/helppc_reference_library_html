from common import Topic, TopicRef, Section

TITLE_MAP = {
    "int table": "Interrupt Tables",
}


BYTE_REPLACEMENTS = {
    # Control characters
    0x01: "☺",
    0x02: "☻",
    0x03: "♥",
    0x04: "♦",
    0x05: "♣",
    0x06: "♠",
    0x07: "•",
    0x08: "◘",
    # 0x09: "○", # Horizontal tab breaks formatting if replaced
    0x0a: "◙",
    0x0b: "♂",
    0x0c: "♀",
    0x0d: "♪",
    0x0e: "♫",
    0x0f: "☼",
    0x10: "►",
    0x11: "◄",
    0x12: "↕",
    0x13: "‼",
    0x14: "¶",
    0x15: "§",
    0x16: "▬",
    0x17: "↨",
    0x18: "↑",
    0x19: "↓",
    0x1a: "→",
    0x1b: "←",
    0x1c: "∟",
    0x1d: "↔",
    0x1e: "▲",
    0x1f: "▼",

    # Extended latin characters
    0x7f: "⌂",
    0x80: "Ç",
    0x81: "ü",
    0x82: "é",
    0x83: "â",
    0x84: "ä",
    0x85: "à",
    0x86: "å",
    0x87: "ç",
    0x88: "ê",
    0x89: "ë",
    0x8a: "è",
    0x8b: "ï",
    0x8c: "î",
    0x8d: "ì",
    0x8e: "Ä",
    0x8f: "Å",
    0x90: "É",
    0x91: "æ",
    0x92: "Æ",
    0x93: "ô",
    0x94: "ö",
    0x95: "ò",
    0x96: "û",
    0x97: "ù",
    0x98: "ÿ",
    0x99: "Ö",
    0x9a: "Ü",
    0x9b: "¢",
    0x9c: "£",
    0x9d: "¥",
    0x9e: "₧",
    0x9f: "ƒ",
    0xa0: "á",
    0xa1: "í",
    0xa2: "ó",
    0xa3: "ú",
    0xa4: "ñ",
    0xa5: "Ñ",
    0xa6: "ª",
    0xa7: "º",
    0xa8: "¿",
    0xa9: "⌐",
    0xaa: "¬",
    0xab: "½",
    0xac: "¼",
    0xad: "¡",
    0xae: "«",
    0xaf: "»",

    # Block characters
    0xb0: "░",
    0xb1: "▒",
    0xb2: "▓",
    0xb3: "│",
    0xb4: "┤",
    0xb5: "╡",
    0xb6: "╢",
    0xb7: "╖",
    0xb8: "╕",
    0xb9: "╣",
    0xba: "║",
    0xbb: "╗",
    0xbc: "╝",
    0xbd: "╜",
    0xbe: "╛",
    0xbf: "┐",
    0xc0: "└",
    0xc1: "┴",
    0xc2: "┬",
    0xc3: "├",
    0xc4: "─",
    0xc5: "┼",
    0xc6: "╞",
    0xc7: "╟",
    0xc8: "╚",
    0xc9: "╔",
    0xca: "╩",
    0xcb: "╦",
    0xcc: "╠",
    0xcd: "═",
    0xce: "╬",
    0xcf: "╧",
    0xd0: "╨",
    0xd1: "╤",
    0xd2: "╥",
    0xd3: "╙",
    0xd4: "╘",
    0xd5: "╒",
    0xd6: "╓",
    0xd7: "╫",
    0xd8: "╪",
    0xd9: "┘",
    0xda: "┌",
    0xdb: "█",
    0xdc: "▄",
    0xdd: "▌",
    0xde: "▐",
    0xdf: "▀",

    # Math characters
    0xe0: "α",
    0xe1: "ß",
    0xe2: "Γ",
    0xe3: "π",
    0xe4: "Σ",
    0xe5: "σ",
    0xe6: "μ",
    0xe7: "τ",
    0xe8: "Φ",
    0xe9: "Θ",
    0xea: "Ω",
    0xeb: "δ",
    0xec: "∞",
    0xed: "φ",
    0xee: "ε",
    0xef: "∩",
    0xf0: "≡",
    0xf1: "±",
    0xf2: "≥",
    0xf3: "≤",
    0xf4: "⌠",
    0xf5: "⌡",
    0xf6: "÷",
    0xf7: "≈",
    0xf8: "°",
    0xf9: "∙",
    0xfa: "·",
    0xfb: "√",
    0xfc: "ⁿ",
    0xfd: "²",
    0xfe: "■"
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
    topics: dict[str, Topic] = {}
    current_ref = None

    with open(file, "rb") as stream:
        while line := stream.readline():
            line = replace_links(bytestostr(line.rstrip()), refs)
            if line.startswith("@"):
                section_title = line[1:]
            elif line.startswith(":"):
                if current_ref:
                    # Trim current body from extra newlines
                    stripped = topics[current_ref].body.strip('\r\n')
                    topics[current_ref].body = stripped
                # Use first tag in line as ref
                current_ref = line[1:].split(":")[0].lower()
                topics[current_ref] = Topic("", "")
            elif line.startswith("^"):
                if current_ref in TITLE_MAP:
                    topics[current_ref].title = TITLE_MAP[current_ref]
                    topics[current_ref].body += f"<h2>{line[1:]}</h2>\n"
                else:
                    # Take title from the ^ line if we don't override it
                    topics[current_ref].title = line[1:]
            elif line.startswith("%"):
                topics[current_ref].body += f"<b>{line[1:]}</b>\n"
            else:
                topics[current_ref].body += f"{line}\n"

    return Section(section_title, topics)
