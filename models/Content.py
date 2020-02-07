from models import Sentence


class Content:

    def __init__(self):
        self.search_term = None
        self.search_prefix = None
        self.original_source_content = None
        self.sanitized_source_content = None
        self._sentences = []
        self._downloaded_images = []

    def add_sentence(self, new_sentence: Sentence):
        self._sentences.append(new_sentence)

    def add_downloaded_image(self, new_downloaded_image: str):
        self._downloaded_images.append(new_downloaded_image)
