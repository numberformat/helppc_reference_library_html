#!/bin/env python3

import os
import glob
import shutil
from dataclasses import dataclass

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
class Topic:
  title: str
  entries: dict[str, str]

class IndexPageFactory:
  def __init__(self, template_path: str) -> None:
    with open(template_path) as file:
      self.template = "".join(file.readlines())
      self.topics=[]

  def add_topic(self, title: str, link: str) -> None:
    self.topics.append((title, link))
    
  def build(self) -> str:
    topic_list = (
      f"<li><a href=\"{link}\">{title}</a></li>\n" 
      for (title, link) in self.topics
    )
    replacement = "      ".join(topic_list)[:-1]
    return self.template.replace("%TOPICS%", replacement)
  
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

def maketopic(file: str) -> Topic:
  entries = {}
  title = None

  with open(file, "rb") as reader:
    while line := reader.readline():
      if line.startswith(b'@'):
        line = line[1:].strip()
        title = bytestostr(line)
      elif line.startswith(b':'):
        line = line[1:].strip()
        refs = line.split(b':')
        if refs:
          refs_file = os.path.join(
            TOPIC_SLUG_MAP[os.path.basename(file)], 
            makefname(refs[0]) + '.html'
          )
          for ref in refs:
            entries[ref.decode().lower()] = refs_file

  return Topic(title, entries)

def main() -> None:
  index_factory = IndexPageFactory("assets/index.html")
  
  shutil.rmtree('dist', ignore_errors=True)
  os.mkdir('dist')
  shutil.copyfile("assets/style.css", "dist/style.css")
  shutil.copyfile(
    "assets/webplus-ibm-vga-8x14.woff", 
    "dist/webplus-ibm-vga-8x14.woff"
  )

  for file in glob.glob('docs/*.TXT'):
    slug = TOPIC_SLUG_MAP[os.path.basename(file)]
    topic_dir = os.path.join(BASE_PATH, slug)
    os.makedirs(topic_dir, 0o755, exist_ok=True)

    topic = maketopic(file)

    index_factory.add_topic(
      topic.title,
      os.path.join(slug, "index.html")
    )

  with open("dist/index.html", "w") as file:
    file.write(index_factory.build())

if __name__ == "__main__":
  main()
