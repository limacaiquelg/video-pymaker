import re
import nltk

import Algorithmia

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, KeywordsOptions

from helpers import access_credentials
from models import Content
from models.Sentence import Sentence
from robots import state


def fetch_content_from_wikipedia(content: Content) -> Content:
    print('> [Text Robot] Fetching content from Wikipedia...')

    algorithmia_client = Algorithmia.client(access_credentials('algorithmia.json', 'api_key'))
    wiki_algorithm = algorithmia_client.algo('web/WikipediaParser/0.1.2')
    wiki_response = wiki_algorithm.pipe(content.search_term)
    wiki_content = wiki_response.result.get('content')

    content.original_source_content = wiki_content
    print('> [Text Robot] Fetching done!')

    return content


def validate_lines_from_content(line: str) -> bool:
    if (len(line.strip()) == 0 and isinstance(len(line.strip()), type(0))) or line.strip().startswith('='):
        return False

    return True


def remove_blank_lines_and_markdown(text: str) -> str:
    all_lines = text.split('\n')

    sanitized_lines = list(filter(validate_lines_from_content, all_lines))
    sanitized_string = ' '.join(sanitized_lines)

    return sanitized_string


def remove_dates_in_parentheses(text: str) -> str:
    return re.sub("\\((?:\\([^()]*\\)|[^()])*\\)", "", text).replace("  ", " ")


def sanitize_content(content: Content) -> Content:
    print('> [Text Robot] Sanitizing content...')

    text_without_blank_lines_and_markdown = remove_blank_lines_and_markdown(content.original_source_content)
    text_without_dates_in_parentheses = remove_dates_in_parentheses(text_without_blank_lines_and_markdown)
    content.sanitized_source_content = text_without_dates_in_parentheses

    print('> [Text Robot] Content sanitized!')
    return content


def break_content_into_sentences(content: Content) -> Content:
    print('> [Text Robot] Breaking content into sentences...')

    text = content.sanitized_source_content
    tokenizer = nltk.tokenize.PunktSentenceTokenizer()
    sentences = tokenizer.tokenize(text)[:content.number_of_sentences]

    for sentence in sentences:
        content.add_sentence(Sentence(sentence))

    print(f'> [Text Robot] Content broke into sentences. Number of sentences: {content.number_of_sentences}.')
    return content


def fetch_watson_and_return_keywords(text: str) -> list:
    authenticator = IAMAuthenticator(access_credentials('watson-nlu.json', 'apikey'))
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2019-07-12',
        authenticator=authenticator
    )
    natural_language_understanding.set_service_url(access_credentials('watson-nlu.json', 'url'))

    watson_response = natural_language_understanding.analyze(
        text=text,
        features=Features(keywords=KeywordsOptions())
    ).get_result()

    return [keyword.get('text') for keyword in watson_response.get('keywords')]


def fetch_keywords_of_all_sentences(content: Content) -> Content:
    print('> [Text Robot] Fetching keywords from IBM Watson...')

    for sentence in content.sentences:
        print(f'> [Text Robot] Sentence: {sentence.text}')

        keywords = fetch_watson_and_return_keywords(sentence.text)

        for keyword in keywords:
            sentence.add_keyword(keyword)
            print(f'> [Text Robot] Keyword \'{keyword}\' added into the sentence above.')

    return content


def robot():
    print('\n>>> [Text Robot] Starting...')

    content = state.load()
    content = fetch_content_from_wikipedia(content)
    content = sanitize_content(content)
    content = break_content_into_sentences(content)
    content = fetch_keywords_of_all_sentences(content)
    state.save(content)

    print('>>> [Text Robot] Stopping. Work done!')
