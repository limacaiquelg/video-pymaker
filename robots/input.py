from models.Content import Content
from robots import state


def ask_search_term():
    search_term = input('\nPlease, input a Wikipedia search term: ')
    return search_term


def ask_search_prefix():
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
        raise ValueError('> [Input Robot] ERROR: Invalid input. This field accepts only numbers.')

    search_prefix_index = int(search_prefix_index)

    if search_prefix_index != 0 and search_prefix_index not in prefixes:
        raise ValueError('> [Input Robot] ERROR: Invalid search prefix. Please try again.')
    elif search_prefix_index == 0:
        raise ValueError('> [Input Robot] System stopped by the user.')

    search_prefix = prefixes[search_prefix_index]
    return search_prefix


def robot():
    content = Content()

    content.search_term = ask_search_term()
    try:
        content.search_prefix = ask_search_prefix()
    except ValueError as value_error:
        print(value_error)

    print(f'> [Input Robot] Saving content state...')
    state.save(content)
