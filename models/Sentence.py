class Sentence:
    def __init__(self, text):
        self.text = text
        self._keywords = []
        self._images = []

    def add_keyword(self, new_keyword: str):
        self._keywords.append(new_keyword)

    def add_image(self, new_image: str):
        self._images.append(new_image)
