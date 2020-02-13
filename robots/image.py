import os
import wget

from googleapiclient.discovery import build

from helpers import create_new_directory, access_credentials
from models import Content
from robots import state


def fetch_google_and_return_image_links(query: str) -> list:
    service = build('customsearch', 'v1', developerKey=access_credentials('google-search.json', 'api-key'))
    response = service.cse().list(
        q=query,
        cx=access_credentials('google-search.json', 'search-engine-id'),
        searchType='image',
        imgSize='xlarge',
        num=3,
        siteSearch='https://www.biography.com/',
        siteSearchFilter='e'
    ).execute()

    return [item.get('link') for item in response.get('items')]


def fetch_images_of_all_sentences(content: Content) -> Content:
    print('> [Image Robot] Starting querying images using Google Images...')
    first = True

    for sentence in content.sentences:
        sentence.reset_images_list()

        if first:
            query = f'{content.search_term}'
            first = False
        else:
            query = f'{content.search_term} {sentence.keywords[0]}'

        print(f'> [Image Robot] Querying Google Images with: \'{query}\'')

        for image_link in fetch_google_and_return_image_links(query):
            sentence.add_image(image_link)

        sentence.google_search_query = query

    print('> [Image Robot] All images were successfully fetched.')

    return content


def download_and_save(url: str, filename: str) -> bool:
    output_path = os.path.join('content', 'images', 'originals', filename)

    try:
        image_path = wget.download(url, out=output_path)

        if image_path is None or len(image_path) == 0:
            raise Exception('Error downloading image.')

        return True
    except Exception as e:
        print(f'> [Image Robot] WGet Error: {e}.')
        return False


def download_all_images(content: Content) -> Content:
    content.reset_downloaded_images_list()
    state.delete_images_directory()

    print('> [Image Robot] Starting downloading images...')

    IMAGES_DIRECTORY = os.path.join('content', 'images')
    create_new_directory(IMAGES_DIRECTORY, 'Image')

    ORIGINAL_IMAGES_DIRECTORY = os.path.join('content', 'images', 'originals')
    create_new_directory(ORIGINAL_IMAGES_DIRECTORY, 'Image')

    for sentence_index, sentence in enumerate(content.sentences):
        images = sentence.images

        for image_index, image in enumerate(images):
            try:
                if image in content.downloaded_images:
                    raise Exception('Image already downloaded.')

                if download_and_save(image, f'{sentence_index}-original.png'):
                    content.add_downloaded_image(image)
                    print(f'> [Image Robot] [S{sentence_index}][I{image_index}] Image successfully downloaded: {image}')
                    break

            except Exception as e:
                print(f'> [Image Robot] [S{sentence_index}][I{image_index}] Error ({image}): {e}')

    print('> [Image Robot] Images successfully downloaded.')

    return content


def robot():
    print('\n>>> [Image Robot] Starting...')

    content = state.load()
    content = fetch_images_of_all_sentences(content)
    content = download_all_images(content)
    state.save(content)

    print('>>> [Image Robot] Stopping. Work done!')
