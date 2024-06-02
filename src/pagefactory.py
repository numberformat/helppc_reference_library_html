class TopicPageFactory:
    def __init__(self, template_path: str) -> None:
        with open(template_path) as stream:
            self.template = "".join(stream.readlines())
            self.body = None
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


class IndexPageFactory:
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
            f'<li><a href="{link}">{title}</a></li>\n'
            for (link, title) in self.entries.items()
        )
        entries_replacement = "      ".join(html_entries)[:-1]
        return self.template \
            .replace("$STYLE_HREF", self.style_href) \
            .replace("$TITLE", self.title) \
            .replace("$ENTRIES", entries_replacement)
