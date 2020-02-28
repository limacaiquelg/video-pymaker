from helpers import exit_video_pymaker
from models.Content import Content
from robots import state


def ask_search_term() -> str:
    search_term = input('\nPlease, input a Wikipedia search term: ')

    if len(search_term) < 1:
        raise ValueError('Error: Invalid Input. This field is required. Please, try again.')

    return search_term


def ask_search_prefix() -> str:
    prefixes = {
        1: "Who is",
        2: "What is",
        3: "The history of"
    }

    for key, prefix in prefixes.items():
        print(f'[{key}] {prefix}')

    print('[0] CANCEL\n')
    search_prefix_index = input('Please, choose one option: ')

    if not search_prefix_index.isdecimal():
        raise ValueError('Error: Invalid input. This field accepts only numbers.')

    search_prefix_index = int(search_prefix_index)

    if search_prefix_index != 0 and search_prefix_index not in prefixes:
        raise ValueError('Error: Invalid search prefix. Please try again.')
    elif search_prefix_index == 0:
        raise ValueError('System stopped by the user.')

    search_prefix = prefixes[search_prefix_index]
    return search_prefix


def robot():
    try:
        content = Content()

        content.search_term = ask_search_term()
        content.search_prefix = ask_search_prefix()

        print(f'> [Input Robot] Saving content state...')
        state.save(content)
    except ValueError as value_error:
        print(f'\n> [Input Robot] {value_error}')
        exit_video_pymaker()
    except Exception as e:
        print(f'\n> [Input Robot] Unexpected Error: {e}')
        exit_video_pymaker()
