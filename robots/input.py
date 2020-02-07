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
        raise ValueError('Invalid input. This field accepts only numbers.')

    search_prefix_index = int(search_prefix_index)

    if search_prefix_index != 0 and search_prefix_index not in prefixes:
        raise ValueError('Invalid search prefix. Please try again.')
    elif search_prefix_index == 0:
        return "CANCEL"

    search_prefix = prefixes[search_prefix_index]
    return search_prefix
