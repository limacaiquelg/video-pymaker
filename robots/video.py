from moviepy.audio.fx.audio_fadein import audio_fadein
from moviepy.audio.fx.audio_fadeout import audio_fadeout
from moviepy.audio.fx.volumex import volumex
from moviepy.editor import *
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from wand.color import Color
from wand.drawing import Drawing
from wand.exceptions import BaseError
from wand.font import Font
from wand.image import Image

from helpers import create_new_directory
from models import Content
from robots import state


def convert_image(sentence_index: int):
    INPUT_FILE = os.path.join('content', 'images', 'originals', f'{sentence_index}-original.png[0]')
    OUTPUT_FILE = os.path.join('content', 'images', 'converted', f'{sentence_index}-converted.png')
    IMAGE_WIDTH = 1920
    IMAGE_HEIGHT = 1080

    try:
        with Image(filename=INPUT_FILE) as original_image:
            blurred_image = original_image.clone()
            blurred_image.background_color = Color('white')
            blurred_image.blur(0, 9)
            blurred_image.resize(IMAGE_WIDTH, IMAGE_HEIGHT)

            with original_image.clone() as front_image:
                front_image.background_color = Color('white')
                front_image.transform(resize=f'x{IMAGE_HEIGHT}')
                blurred_image.composite(front_image, operator='over', gravity='center')

            blurred_image.extent(IMAGE_WIDTH, IMAGE_HEIGHT)

            with blurred_image.convert('png') as converted_image:
                converted_image.save(filename=OUTPUT_FILE)

            blurred_image.close()

            print(f'> [Video Robot] Image converted: {OUTPUT_FILE}')

    except BaseError as e:
        print(f'> [Video Robot] Error converting image: {e}')


def convert_all_images(content: Content):
    print(f'> [Video Robot] Converting images...')

    CONVERTED_IMAGES_DIRECTORY = os.path.join('content', 'images', 'converted')
    create_new_directory(CONVERTED_IMAGES_DIRECTORY, 'Image')

    for sentence_index, sentence in enumerate(content.sentences):
        convert_image(sentence_index)


def create_sentence_image(sentence_index: int, text: str):
    OUTPUT_FILE = os.path.join('content', 'images', 'sentences', f'{sentence_index}-sentence.png')

    TEMPLATE_SETTINGS = {
        0: {
            'width': 1920,
            'height': 400,
            'gravity': 'center'
        },
        1: {
            'width': 1920,
            'height': 1080,
            'gravity': 'center'
        },
        2: {
            'width': 800,
            'height': 1080,
            'gravity': 'west'
        },
        3: {
            'width': 1920,
            'height': 400,
            'gravity': 'center'
        },
        4: {
            'width': 1920,
            'height': 1080,
            'gravity': 'center'
        },
        5: {
            'width': 800,
            'height': 1080,
            'gravity': 'west'
        },
        6: {
            'width': 1920,
            'height': 400,
            'gravity': 'center'
        }
    }

    image_width = TEMPLATE_SETTINGS[sentence_index].get('width')
    image_height = TEMPLATE_SETTINGS[sentence_index].get('height')

    with Image(width=image_width, height=image_height) as sentence_image:
        sentence_image.gravity = TEMPLATE_SETTINGS[sentence_index].get('gravity')

        sentence_image.caption(
            text,
            font=Font(
                'Helvetica, sans-serif',
                color=Color('white'),
                stroke_color=Color('#696969'),
                stroke_width=2
            )
        )
        sentence_image.save(filename=OUTPUT_FILE)

    print(f'> [Video Robot] Sentence image created: {OUTPUT_FILE}')


def create_all_sentences_images(content: Content):
    print(f'> [Video Robot] Creating all sentences images...')

    SENTENCES_IMAGES_DIRECTORY = os.path.join('content', 'images', 'sentences')
    create_new_directory(SENTENCES_IMAGES_DIRECTORY, 'Image')

    for sentence_index, sentence in enumerate(content.sentences):
        create_sentence_image(sentence_index, sentence.text)


def create_youtube_thumbnail():
    print('> [Video Robot] Creating the YouTube Thumbnail...')

    INPUT_FILE = os.path.join('content', 'images', 'converted', '0-converted.png')
    OUTPUT_FILE_PNG = os.path.join('content', 'images', 'youtube-thumbnail.png')
    OUTPUT_FILE_JPG = os.path.join('content', 'images', 'youtube-thumbnail.jpg')

    with Image(filename=INPUT_FILE) as original:
        original.save(filename=OUTPUT_FILE_PNG)

        with original.convert('jpeg') as youtube_thumbnail:
            youtube_thumbnail.save(filename=OUTPUT_FILE_JPG)

    print(f'> [Video Robot] YouTube Thumbnail created: {OUTPUT_FILE_PNG}')


def create_video_initial_images(content: Content):
    print('> [Video Robot] Creating initial images of the video...')
    VIDEO_PYMAKER_OUTPUT_FILE = os.path.join('content', 'images', 'video-pymaker.png')
    TITLE_INPUT_FILE = os.path.join('content', 'images', 'youtube-thumbnail.png')
    TITLE_OUTPUT_FILE = os.path.join('content', 'images', 'title.png')

    with Image(width=1920, height=1080, background=Color('black')) as video_pymaker_image:
        video_pymaker_image.noise('laplacian', attenuate=1.0)

        with Drawing() as title:
            title.fill_color = Color('white')
            title.font_family = 'Edwardian Script ITC'
            title.font_size = 300
            title.gravity = 'center'
            title.stroke_color = Color('#FFD700')
            title.stroke_width = 1
            title.text_kerning = -1
            video_pymaker_image.annotate('Video Pymaker', title, baseline=-100)

        with Drawing() as complement:
            complement.fill_color = Color('white')
            complement.font_family = 'Edwardian Script ITC'
            complement.font_size = 120
            complement.gravity = 'center'
            complement.stroke_color = Color('#FFD700')
            complement.stroke_width = 0.1
            complement.text_kerning = -1
            video_pymaker_image.annotate('Presents ', complement, baseline=150)

        video_pymaker_image.save(filename=VIDEO_PYMAKER_OUTPUT_FILE)

    with Image(filename=TITLE_INPUT_FILE) as title_image:
        title_image.gaussian_blur(sigma=10)
        title_image.noise('laplacian', attenuate=1.0)

        with Drawing() as title:
            title.fill_color = Color('white')
            title.font_family = 'Edwardian Script ITC'
            title.font_size = 250
            title.gravity = 'center'
            title.text_kerning = -1
            title_image.annotate(f'{content.search_prefix} {content.search_term}', title)

        title_image.save(filename=TITLE_OUTPUT_FILE)


def create_video_with_moviepy():
    IMAGES_DIRECTORY = os.path.join('content', 'images', 'converted')
    IMAGES_FILENAMES = os.listdir(IMAGES_DIRECTORY)
    IMAGES_LIST = [os.path.join(IMAGES_DIRECTORY, filemane) for filemane in IMAGES_FILENAMES]

    SENTENCES_DIRECTORY = os.path.join('content', 'images', 'sentences')
    SENTENCES_FILENAMES = os.listdir(SENTENCES_DIRECTORY)
    SENTENCES_LIST = [os.path.join(SENTENCES_DIRECTORY, filemane) for filemane in SENTENCES_FILENAMES]
    SENTENCES_POSITIONS = ['bottom', 'center', 'left', 'center', 'center', 'left', 'bottom']

    VIDEO_PYMAKER_FILE = os.path.join('content', 'images', 'video-pymaker.png')
    TITLE_FILE = os.path.join('content', 'images', 'title.png')

    AUDIO_PATH = os.path.join('assets', 'Cool_Blast_Disco_Ultralounge.mp3')

    OUTPUT_PATH = os.path.join('content', 'output.mp4')

    print('> [Video Clip] Starting rendering video with MoviePy...\n')

    video_pymaker_clip = (
        ImageClip(VIDEO_PYMAKER_FILE, duration=3)
        .fx(transfx.fadein, 0.5)
        .fx(transfx.fadeout, 0.5)
    )

    title_clip = (
        ImageClip(TITLE_FILE, duration=3)
        .fx(transfx.fadein, 0.5)
        .fx(transfx.fadeout, 0.5)
    )

    clips = [video_pymaker_clip, title_clip]

    for index, (image, sentence) in enumerate(zip(IMAGES_LIST, SENTENCES_LIST)):
        image_clip = (
            ImageClip(image, duration=10)
            .fx(transfx.fadein, 1.5)
            .fx(transfx.fadeout, 1.5)
        )

        sentence_clip = (
            ImageClip(sentence, duration=10)
            .set_position(SENTENCES_POSITIONS[index])
            .fx(transfx.fadein, 1.5)
            .fx(transfx.fadeout, 1.5)
        )

        clips.append(CompositeVideoClip([image_clip, sentence_clip]))

    audio_clip = (
        AudioFileClip(AUDIO_PATH)
        .fx(volumex, 0.8)
        .fx(audio_fadein, 1)
        .fx(audio_fadeout, 1)
    )

    final_clip = concatenate_videoclips([clip for clip in clips])

    final_clip = final_clip.set_audio(audio_clip)
    final_clip.write_videofile(OUTPUT_PATH, fps=24)
    print(f'> [Video Clip] Video available at: {OUTPUT_PATH}')


def robot():
    print('\n>>> [Video Robot] Starting...')

    content = state.load()
    convert_all_images(content)
    create_all_sentences_images(content)
    create_youtube_thumbnail()
    create_video_initial_images(content)
    create_video_with_moviepy()
    state.save(content)

    print('>>> [Video Robot] Stopping. Work done!')
