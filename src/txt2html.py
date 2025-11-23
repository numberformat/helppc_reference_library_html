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


class MainArguments:
    generate_indices: bool


def main(args: MainArguments) -> None:
    # Copy assets over
    shutil.rmtree(BASE_PATH, ignore_errors=True)
    shutil.copytree(ASSETS_PATH, BASE_PATH)

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


if __name__ == "__main__":
    argparser = ArgumentParser(prog="txt2html")
    # Specify -i to generate indices in the assets folder, to be used locally
    argparser.add_argument("-i", "--generate-indices", action="store_true")
    main(argparser.parse_args(namespace=MainArguments))
