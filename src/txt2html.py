#!/bin/env python3

import os
import glob
import shutil
from readrefs import readrefs
from readsection import readsection
from pagefactory import IndexPageFactory, TopicPageFactory
from common import TopicRef, Section
from argparse import ArgumentParser

ASSETS_PATH = "assets"
TEMPLATES_PATH = "templates"
DOCS_PATH = "docs"
BASE_PATH = "dist"

TOPIC_SLUG_MAP = {
    "INTERRUP.TXT": "int",
    "ASM.TXT": "asm",
    "C.TXT": "c",
    "HARDWARE.TXT": "hw",
    "MISC.TXT": "misc",
    "TABLES.TXT": "tables"
}

COLOR_SCHEMES: dict[str, dict[str, str]] = {
    # Default VGA-ish gray on black
    "gray-black": {
        "foreground": "#aaaaaa",
        "background": "#000000",
        "accent": "#ffffff"
    },
    # Bright phosphor looks
    "green-black": {
        "foreground": "#00ff5f",
        "background": "#000000",
        "accent": "#b7ffb7"
    },
    "amber-black": {
        "foreground": "#ffbf70",
        "background": "#000000",
        "accent": "#ffdca8"
    },
    "white-black": {
        "foreground": "#e5e5e5",
        "background": "#000000",
        "accent": "#ffffff"
    },
    # Classic blue-screen palettes
    "gray-blue": {
        "foreground": "#c0c0c0",
        "background": "#0000aa",
        "accent": "#ffff55"
    },
    "cyan-blue": {
        "foreground": "#00ffff",
        "background": "#0000aa",
        "accent": "#ffffff"
    },
    "yellow-blue": {
        "foreground": "#ffff55",
        "background": "#0000aa",
        "accent": "#ffffff"
    }
}


class MainArguments:
    generate_indices: bool
    color_scheme: str


def apply_color_scheme(style_path: str, scheme_name: str) -> None:
    scheme = COLOR_SCHEMES[scheme_name]
    accent = scheme.get("accent", scheme["foreground"])
    overrides = f"""

/* Color scheme: {scheme_name} */
body {{
  background-color: {scheme["background"]};
  color: {scheme["foreground"]};
}}
a, b, h1, h2, h3 {{
  color: {accent};
}}
"""
    with open(style_path, "a", encoding="utf-8") as stream:
        stream.write(overrides)


def main(args: MainArguments) -> None:
    # Copy assets over
    shutil.rmtree(BASE_PATH, ignore_errors=True)
    shutil.copytree(ASSETS_PATH, BASE_PATH, dirs_exist_ok=True)
    apply_color_scheme(os.path.join(BASE_PATH, "style.css"), args.color_scheme)

    # First pass, create the references
    refs: dict[str, TopicRef] = {}
    for section_file in glob.glob("docs/*.TXT"):
        section_slug = TOPIC_SLUG_MAP[os.path.basename(section_file)]
        refs |= readrefs(section_file, section_slug)

    # Second pass, read the content
    sections: dict[str, Section] = {}
    for file in glob.glob("docs/*.TXT"):
        sections[file] = readsection(file, refs)

    for section_file, section in sections.items():
        # Create the section directory if it doesn't exist
        section_slug = TOPIC_SLUG_MAP[os.path.basename(section_file)]
        section_dir = os.path.join(BASE_PATH, section_slug)
        os.makedirs(section_dir, 0o755, exist_ok=True)

        # Write the topic files
        for topic_ref, topic in section.topics.items():
            factory = TopicPageFactory(
                os.path.join(TEMPLATES_PATH, "topic.html")
            )
            factory.set_title(topic.title)
            factory.set_style_href("../style.css")
            factory.set_body(topic.body)

            topic_filename = refs[topic_ref].filename
            topic_file = os.path.join(BASE_PATH, section_slug, topic_filename)

            with open(topic_file, "w", encoding="utf-8") as stream:
                print(f"Writing file '{topic_file}'")
                stream.write(factory.build())

        if args.generate_indices:
            # Write the index file
            factory = IndexPageFactory(
                os.path.join(TEMPLATES_PATH, "list.html"))
            factory.set_title(section.title)
            factory.set_style_href("../style.css")
            for topic_ref, topic in section.topics.items():
                factory.add_entry(topic.title, refs[topic_ref].filename)

            index_file = os.path.join(ASSETS_PATH, section_slug, "index.html")

            with open(index_file, "w", encoding="utf-8") as stream:
                print(f"Writing index file of section '{section_slug}'")
                stream.write(factory.build())

    if args.generate_indices:
        # Write main index file
        factory = IndexPageFactory(os.path.join(TEMPLATES_PATH, "list.html"))
        factory.set_title("HelpPC Reference Library")
        factory.set_style_href("./style.css")

        for section_file, section in sections.items():
            section_slug = TOPIC_SLUG_MAP[os.path.basename(section_file)]
            section_index_file = os.path.join(section_slug, "index.html")
            factory.add_entry(section.title, section_index_file)

        main_index_file = os.path.join(ASSETS_PATH, "index.html")

        with open(main_index_file, "w", encoding="utf-8") as stream:
            print(f"Writing main index file")
            stream.write(factory.build())

    available_schemes = ", ".join(COLOR_SCHEMES.keys())
    print(
        "\nHTML generation complete.\n"
        "To view the HTML, serve the dist/ folder, e.g.: python -m http.server --directory dist 8080\n"
        f"Color schemes available (use -c): {available_schemes}"
    )


if __name__ == "__main__":
    argparser = ArgumentParser(prog="txt2html")
    # Specify -i to generate indices in the assets folder, to be used locally
    argparser.add_argument("-i", "--generate-indices", action="store_true")
    argparser.add_argument(
        "-c", "--color-scheme",
        choices=COLOR_SCHEMES.keys(),
        default="gray-black",
        help="Terminal-style color palette to apply to generated HTML."
    )
    main(argparser.parse_args(namespace=MainArguments))
