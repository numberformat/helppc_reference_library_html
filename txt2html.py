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
class Section:
  title: str
  refs: dict[str, str]

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
  ).strip()

def makefname(slug: bytes) -> str:
  return "".join(
    FILENAME_REPLACEMENTS[b]
    if b in FILENAME_REPLACEMENTS
    else chr(b).lower()
    for b in slug
  )

def makesect(file: str) -> Section:
  refs: dict[str, str] = {}
  title: str = None

  with open(file, "rb") as stream:
    while line := stream.readline():
      if line.startswith(b'@'):
        line = line[1:].strip()
        title = bytestostr(line)
      elif line.startswith(b':'):
        line = line[1:].strip()
        byte_refs = line.split(b':')
        if byte_refs:
          topic_file = makefname(byte_refs[0]) + '.html'
          for byte_ref in byte_refs:
            topic_ref = byte_ref.decode().lower()
            refs[topic_ref] = topic_file

  return Section(title, refs)

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

  for file in glob.glob('docs/*.TXT'):
    section_slug = TOPIC_SLUG_MAP[os.path.basename(file)]
    section_dir = os.path.join(BASE_PATH, section_slug)
    os.makedirs(section_dir, 0o755, exist_ok=True)

    section = makesect(file)

    index_factory = ListPageFactory(os.path.join(ASSETS_PATH, "list.html"))
    index_factory.set_title(section.title)
    index_factory.set_style_href("../style.css")
    
    for (ref, file) in section.refs.items():
      index_factory.add_entry(ref.title(), file)

    with open(os.path.join(BASE_PATH, section_slug, "index.html"), "w") as stream:
      stream.write(index_factory.build())

    main_index_factory.add_entry(
      section.title,
      os.path.join(section_slug, "index.html")
    )

  with open(os.path.join(BASE_PATH, "index.html"), "w") as stream:
    stream.write(main_index_factory.build())

if __name__ == "__main__":
  main()
