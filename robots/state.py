import json
import os

from helpers import create_new_directory, remove_directory
from models.Content import Content
from models.Sentence import Sentence

CONTENT_DIRECTORY = 'content'
CONTENT_FILENAME = 'content.json'


def save(content: Content):
    content_string = json.dumps(convert_object_to_dict(content), indent=4)

    create_new_directory(CONTENT_DIRECTORY, 'State')

    with open(os.path.join(CONTENT_DIRECTORY, CONTENT_FILENAME), 'w') as file:
        file.write(content_string)

    print(f'> [State Robot] Content state saved successfully.')


def load() -> Content:
    with open(os.path.join(CONTENT_DIRECTORY, CONTENT_FILENAME), 'r') as file:
        content_dict = json.load(file)

    content = convert_dict_to_content_object(content_dict)
    print(f'> [State Robot] Content loaded successfully.')
    return content


def delete_content_directory():
    if remove_directory('content', 'State'):
        print('> [State Robot] Content directory successfully removed.')


def delete_images_directory(reset_downloaded_images_list=True):
    if remove_directory(os.path.join('content', 'images'), 'State'):
        print('> [State Robot] Images directory successfully removed.')

        if reset_downloaded_images_list:
            content = load()
            content.reset_downloaded_images_list()
            save(content)


def convert_object_to_dict(obj):
    if hasattr(obj, '__dict__'):
        obj = obj.__dict__

    if isinstance(obj, dict):
        return {k: convert_object_to_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list) or isinstance(obj, tuple):
        return [convert_object_to_dict(e) for e in obj]
    else:
        return obj


def convert_dict_to_content_object(dictionary: dict) -> Content:
    content = Content()

    content.search_term = dictionary.get('search_term')
    content.search_prefix = dictionary.get('search_prefix')
    content.original_source_content = dictionary.get('original_source_content')
    content.sanitized_source_content = dictionary.get('sanitized_source_content')

    for sentence_dict in dictionary.get('_sentences'):
        sentence = Sentence(sentence_dict.get('text'))

        for keyword in sentence_dict.get('_keywords'):
            sentence.add_keyword(keyword)

        for image in sentence_dict.get('_images'):
            sentence.add_image(image)

        content.add_sentence(sentence)

    for downloaded_image in dictionary.get('_downloaded_images'):
        content.add_downloaded_image(downloaded_image)

    return content
