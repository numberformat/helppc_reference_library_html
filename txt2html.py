#!/bin/env python3

import os
import glob
import shutil
from dataclasses import dataclass

ASSETS_PATH="assets"
DOCS_PATH="docs"
BASE_PATH="dist"

TOPIC_SLUG_MAP={
  'INTERRUP.TXT': 'int',
  'ASM.TXT': 'asm',
  'C.TXT': 'c',
  'HARDWARE.TXT': 'hw',
  'MISC.TXT': 'misc',
  'TABLES.TXT': 'tables'
}

BYTE_REPLACEMENTS={
  0xb3: '│',
  0xc0: '└',
  0xc4: '─',
  0xda: '┌',
  0xc5: '┼',
  0xd9: '┘',
  0xb4: '┤',
  0xc2: '┬',
  0xc1: '┴',
  0xbf: '┐',
  0xc3: '├',
  0xf9: '∙'
}

FILENAME_REPLACEMENTS={
  ord(' '): '_',
  ord(','): '-',
  ord('.'): '_',
  ord('('): '-',
  ord(')'): '-'
}

@dataclass
class TopicRef:
  filename: str
  section: str

@dataclass
class Section:
  title: str
  topics: dict[str, str]

class TopicPageFactory:
  def __init__(self, template_path: str) -> None:
    with open(template_path) as stream:
      self.template = "".join(stream.readlines())
      self.body = {}
      self.style_href = None
      self.title = None

  def set_style_href(self, style_href: str) -> None:
    self.style_href = style_href

  def set_title(self, title: str) -> None:
    self.title = title

  def set_body(self, body: str) -> None:
    self.body = body

  def build(self) -> str:
    return self.template \
      .replace("$STYLE_HREF", self.style_href) \
      .replace("$TITLE", self.title) \
      .replace("$BODY", self.body)
  
class ListPageFactory:
  def __init__(self, template_path: str) -> None:
    with open(template_path) as stream:
      self.template = "".join(stream.readlines())
      self.entries = {}
      self.style_href = None
      self.title = None

  def add_entry(self, title: str, link: str) -> None:
    if link not in self.entries:
      self.entries[link] = title

  def set_style_href(self, style_href: str) -> None:
    self.style_href = style_href

  def set_title(self, title: str) -> None:
    self.title = title

  def build(self) -> str:
    html_entries = (
      f"<li><a href=\"{link}\">{title}</a></li>\n" 
      for (link, title) in self.entries.items()
    )
    entries_replacement = "      ".join(html_entries)[:-1]
    return self.template \
      .replace("$STYLE_HREF", self.style_href) \
      .replace("$TITLE", self.title) \
      .replace("$ENTRIES", entries_replacement)
  
def bytestostr(seq: bytes) -> str:
  return "".join(
    BYTE_REPLACEMENTS[b]
    if b in BYTE_REPLACEMENTS
    else chr(b)
    for b in seq
  )

def fname(ref: bytes) -> str:
  return "".join(
    FILENAME_REPLACEMENTS[b]
    if b in FILENAME_REPLACEMENTS
    else chr(b).lower()
    for b in ref
  )

def readrefs(file: str) -> dict[str, TopicRef]:
  refs: dict[str, str] = {}
  section_slug = TOPIC_SLUG_MAP[os.path.basename(file)]

  with open(file, "rb") as stream:
    while line := stream.readline():
      if line.startswith(b':'):
        line = line[1:].rstrip()
        byte_refs = line.split(b':')
        if byte_refs:
          topic_file = f"{fname(byte_refs[0])}.html"
          for byte_ref in byte_refs:
            topic_ref = byte_ref.decode().lower()
            refs[topic_ref] = TopicRef(topic_file, section_slug)

  return refs

def replace_links(line: str, refs: dict[str, TopicRef]) -> str:
  replaced = []
  pos = 0
  while pos < len(line):
    if line[pos] == '~':
      # discard first tilde
      pos += 1
      if line[pos] == '~':
        # if we get a second tilde, write the tilde
        replaced.append('~')
      else:
        link = ""
        while line[pos] != '~':
          link += line[pos]
          pos += 1
        # insert the link only if it's present in the refs
        if link.lower() in refs:
          topic_ref = refs[link.lower()]
          href = f"../{topic_ref.section}/{topic_ref.filename}"
          replaced.append(f'<a href="{href}">{link}</a>')
        else:
          print(f"Link '{link}' not found in refs, treating as plain text")
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
      if line.startswith('@'):
        section_title = line[1:]
      elif line.startswith(':'):
        # First tag in line
        current_ref = line[1:].split(':')[0].lower()
        topics[current_ref] = ""
      elif line.startswith('^'):
        topics[current_ref] += f"<h2>{line[1:]}</h2>\n"
      elif line.startswith('%'):
        topics[current_ref] += f"<b>{line[1:]}</b>\n"
      else:
        topics[current_ref] += f"{line}\n"

  return Section(section_title, topics)

def main() -> None:
  main_index_factory = ListPageFactory(os.path.join(ASSETS_PATH, "list.html"))

  main_index_factory.set_title("HelpPC reference Library")
  main_index_factory.set_style_href("style.css")

  shutil.rmtree(BASE_PATH, ignore_errors=True)
  os.mkdir(BASE_PATH)

  for basename in ["style.css", "webplus-ibm-vga-8x14.woff"]:
    shutil.copyfile(
      os.path.join(ASSETS_PATH, basename),
      os.path.join(BASE_PATH, basename)
    )

  # First pass, create the references
  refs: dict[str, TopicRef] = {}
  for file in glob.glob('docs/*.TXT'):
    refs |= readrefs(file)

  # Second pass, read the content
  sections: dict[str, Section] = {}
  for file in glob.glob('docs/*.TXT'):
    sections[file] = readsection(file, refs)

  for section_file, section in sections.items():
    # Create the section directory if it doesn't exist
    section_slug = TOPIC_SLUG_MAP[os.path.basename(section_file)]
    section_dir = os.path.join(BASE_PATH, section_slug)
    os.makedirs(section_dir, 0o755, exist_ok=True)

    # Write the index file
    factory = ListPageFactory(os.path.join(ASSETS_PATH, "list.html"))
    factory.set_title(section.title)
    factory.set_style_href("../style.css")
    for topic_ref in section.topics.keys():
      factory.add_entry(topic_ref.title(), refs[topic_ref].filename)

    index_file = os.path.join(BASE_PATH, section_slug, "index.html")

    with open(index_file, "w") as stream:
      print(f"Writing index file of section '{section_slug}'")
      stream.write(factory.build())

    # Write the topic files
    for topic_ref, topic_body in section.topics.items():
      factory = TopicPageFactory(os.path.join(ASSETS_PATH, "topic.html"))
      factory.set_title(topic_ref.title())
      factory.set_style_href("../style.css")
      factory.set_body(topic_body)

      topic_filename = refs[topic_ref].filename
      topic_file = os.path.join(BASE_PATH, section_slug, topic_filename)

      with open(topic_file, "w") as stream:
        print(f"Writing file '{topic_file}'")
        stream.write(factory.build())

  # Write main index file
  factory = ListPageFactory(os.path.join(ASSETS_PATH, "list.html"))
  factory.set_title("HelpPC Reference Library")
  factory.set_style_href("./style.css")

  for section_file, section in sections.items():
    section_slug = TOPIC_SLUG_MAP[os.path.basename(section_file)]
    section_index_file = os.path.join(section_slug, "index.html")
    factory.add_entry(section.title, section_index_file)

  main_index_file = os.path.join(BASE_PATH, "index.html")

  with open(main_index_file, "w") as stream:
    print(f"Writing main index file")
    stream.write(factory.build())

if __name__ == "__main__":
  main()
