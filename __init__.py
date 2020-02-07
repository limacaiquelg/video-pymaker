from robots import input

print('>>>>> Welcome to video-pymaker! <<<<<')

try:
    search_term = input.ask_search_term()
    search_prefix = input.ask_search_prefix()

    if search_prefix == "CANCEL":
        print('>>>>> Thank you for using video-pymaker! <<<<<')
        quit()

    print(f'Search: {search_prefix} {search_term}')
except ValueError as value_error:
    print(f'[Input Robot] ERROR: {value_error}')
