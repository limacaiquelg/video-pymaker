from models import Sentence


class Content:

    def __init__(self):
        self.search_term = None
        self.search_prefix = None
        self.original_source_content = None
        self.sanitized_source_content = None
        self._sentences = []
        self._number_of_sentences = 7
        self._downloaded_images = []

    @property
    def sentences(self):
        return self._sentences

    @property
    def number_of_sentences(self):
        return self._number_of_sentences

    @property
    def downloaded_images(self):
        return self._downloaded_images

    def add_sentence(self, new_sentence: Sentence):
        self._sentences.append(new_sentence)

    def add_downloaded_image(self, new_downloaded_image: str):
        self._downloaded_images.append(new_downloaded_image)

    def reset_sentences_list(self):
        self._sentences.clear()

    def reset_downloaded_images_list(self):
        self._downloaded_images.clear()
