import http.client
import os
import time
from random import random

import googleapiclient
import httplib2
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError, MediaUploadSizeError
from googleapiclient.http import MediaFileUpload

from models.Content import Content
from robots import state

CLIENT_SECRETS_FILE = os.path.join('credentials', 'client-secrets.json')

YOUTUBE_UPLOAD_SCOPE = ['https://www.googleapis.com/auth/youtube']
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

RETRIABLE_EXCEPTIONS = (
    httplib2.HttpLib2Error,
    IOError,
    http.client.NotConnected,
    http.client.IncompleteRead,
    http.client.ImproperConnectionState,
    http.client.CannotSendRequest,
    http.client.CannotSendHeader,
    http.client.ResponseNotReady,
    http.client.BadStatusLine
)

RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

httplib2.RETRIES = 1
MAX_RETRIES = 10


def get_authenticated_service() -> googleapiclient.discovery.Resource:
    print('> [YouTube Robot] Initiating authentication with OAuth...')
    print('> [YouTube Robot] Please, authorize video-pymaker to access your YouTube account:\n')

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, YOUTUBE_UPLOAD_SCOPE)
    credentials = flow.run_local_server()
    service = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)

    print('> [YouTube Robot] Thank you for allowing access to your YouTube account.')
    print('> [YouTube Robot] Please, do not forget to close the authentication tab in your browser.')

    return service


def resumable_upload(insert_request: googleapiclient.http.HttpRequest) -> str:
    response = None
    error = None
    retry = 0

    while response is None:
        try:
            print('> [YouTube Robot] Uploading file...')
            status, response = insert_request.next_chunk()
            if response is not None:
                if 'id' in response:
                    print('> [YouTube Robot] Your video was successfully uploaded.')
                    print(f'> [YouTube Robot] Video available at: https://youtu.be/{response["id"]}')

                    return response['id']
                else:
                    raise Exception(f'The upload failed with an unexpected response: {response}.')
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = f'A retriable HTTP error {e.resp.status} occurred: \n{e.content}'
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = f'A retriable error occurred: {e}'

        if error is not None:
            print(f'> [YouTube Robot] {error}.')
            retry += 1
            if retry > MAX_RETRIES:
                raise Exception('No longer attempting to retry.')

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep

            print(f'> [YouTube Robot] Sleeping {sleep_seconds} seconds and then retrying...')
            time.sleep(sleep_seconds)


def upload_video(content: Content, service: googleapiclient.discovery.Resource) -> str:
    VIDEO_FILENAME = os.path.abspath(os.path.join('content', 'output.mp4'))
    VIDEO_TITLE = f'{content.search_prefix} {content.search_term}'
    VIDEO_DESCRIPTION = '\n\n'.join(sentence.text for sentence in content.sentences)
    VIDEO_PRIVACY_STATUS = 'public'
    VIDEO_TAGS = [keyword for keyword in content.sentences[0].keywords]
    VIDEO_TAGS.insert(0, content.search_term)

    body = {
        'snippet': {
            'title': VIDEO_TITLE,
            'description': VIDEO_DESCRIPTION,
            'tags': VIDEO_TAGS
        },
        'status': {
            'privacyStatus': VIDEO_PRIVACY_STATUS
        }
    }

    print('> [YouTube Robot] Starting video upload...')

    try:
        insert_request = service.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=MediaFileUpload(VIDEO_FILENAME, chunksize=-1, resumable=True)
        )

        video_id = resumable_upload(insert_request)

        print('> [YouTube Robot] Video upload done!')

        return video_id
    except HttpError as e:
        print(f'> [YouTube Robot] An HTTP error {e.resp.status} occurred: \n{e.content}.')
    except Exception as e:
        print(f'> [YouTube Robot] Error: {e}.')


def upload_thumbnail(video_id: str, service: googleapiclient.discovery.Resource):
    VIDEO_THUMBNAIL_FILE = os.path.abspath(os.path.join('content', 'images', 'youtube-thumbnail.jpg'))

    print('> [YouTube Robot] Starting video thumbnail upload...')

    try:
        service.thumbnails().set(
            videoId=video_id,
            media_body=VIDEO_THUMBNAIL_FILE
        ).execute()

        print('> [YouTube Robot] The thumbnail was successfully set.')
    except HttpError as e:
        if e.resp.status == 403 and e.resp.reason == 'Forbidden':
            print('> [YouTube Robot] Error uploading thumbnail: you must have a verified account to upload custom '
                  'thumbnails.')
        else:
            raise
    except MediaUploadSizeError:
        print('> [YouTube Robot] Error uploading thumbnail: your thumbnail file is larger than 2MB.')
    except Exception as e:
        print(f'> [YouTube Robot] Error uploading thumbnail: {e}.')


def robot():
    print('\n>>> [YouTube Robot] Starting...')

    content = state.load()

    service = get_authenticated_service()
    video_id = upload_video(content, service)
    upload_thumbnail(video_id, service)

    state.save(content)

    print('>>> [YouTube Robot] Stopping. Work done!')




