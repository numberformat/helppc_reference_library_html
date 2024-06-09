from dataclasses import dataclass


@dataclass
class TopicRef:
    filename: str
    section: str


@dataclass
class Topic:
    title: str
    body: str


@dataclass
class Section:
    title: str
    topics: dict[str, Topic]
