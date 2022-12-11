from tts.guid import guid


class Bag:
    def __init__(self, transform, color, name, content, is_infinite=False):
        self.transform = transform
        self.content = content
        self.name = name
        self.color = color
        self.is_infinite = is_infinite

    def content_items(self):
        items = []
        for item in self.content:
            items.append(item.as_dict())
        return items
