class Sentence:
    def __init__(self, text):
        self.text = text
        self._keywords = []
        self._images = []
        self.google_search_query = None

    @property
    def keywords(self):
        return self._keywords

    @property
    def images(self):
        return self._images

    def add_keyword(self, new_keyword: str):
        self._keywords.append(new_keyword)

    def add_image(self, new_image: str):
        self._images.append(new_image)

    def reset_keywords_list(self):
        self._keywords.clear()

    def reset_images_list(self):
        self._images.clear()