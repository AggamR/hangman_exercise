# I know it says to put them in a dict but that's really weird
# and a list makes much more sense
HANGMAN_PHOTOS = [
    '\tx-------x',
    (
        '\tx-------x\n'
        '\t|\n'
        '\t|\n'
        '\t|\n'
        '\t|\n'
        '\t|'
    ),
    (
        '\tx-------x\n'
        '\t|       |\n'
        '\t|       0\n'
        '\t|\n'
        '\t|\n'
        '\t|\n'
    ),
    (
        '\tx-------x\n'
        '\t|       |\n'
        '\t|       0\n'
        '\t|       |\n'
        '\t|\n'
        '\t|\n'
    ),
    (
        '\tx-------x\n'
        '\t|       |\n'
        '\t|       0\n'
        '\t|      /|\\\n'
        '\t|\n'
        '\t|\n'
    ),
    (
        '\tx-------x\n'
        '\t|       |\n'
        '\t|       0\n'
        '\t|      /|\\\n'
        '\t|      /\n'
        '\t|\n'
    ),
    (
        '\tx-------x\n'
        '\t|       |\n'
        '\t|       0\n'
        '\t|      /|\\\n'
        '\t|      / \\\n'
        '\t|\n'
    )
]

MAX_TRIES = len(HANGMAN_PHOTOS) - 1  # could be just 6 but this is more dynamic

OPENING_SCREEN = f"""
Welcome to the game Hangman
    _    _
   | |  | |
   | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __
   |  __  |/ _' | '_ \ / _' | '_ ' _ \ / _' | '_ \\
   | |  | | (_| | | | | (_| | | | | | | (_| | | | |
   |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                        __/ |
                       |___/

Number of attemps allowed: {MAX_TRIES}
"""


def choose_word(file_path, index):
    """
    Chooses a word from a file based on the given index.

    Args:
        file_path (str): The path to the file containing the words.
        index (int): The index of the word to choose (1-based).

    Returns:
        tuple: A tuple containing the total number
        of words in the file and the chosen word.
        If an error occurs while reading the file, it returns (0, '').
    """
    try:
        words = open(file_path, 'r').read().split('\n')
    except:
        return (0, '')
    # index-1 because the index starts from 1
    # and modulo is to make it circular
    return (len(words), words[(index - 1) % len(words)])


def print_hangman(num_of_tries):
    """
    Prints the hangman picture corresponding to
    the given number of tries remaining.

    Args:
        num_of_tries (int): The number of tries remaining.
    """
    print(HANGMAN_PHOTOS[num_of_tries])


def is_valid_input(letter_guessed):
    """
    Checks if the given input is a valid single letter.

    Args:
        letter_guessed (str): The input to be checked.

    Returns:
        bool: True if the input is a single letter, False otherwise.
    """
    return len(letter_guessed) == 1 and letter_guessed.isalpha()


def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """
    Tries to update the list of old letters guessed with a new letter.

    Args:
        letter_guessed (str): The new letter to be added to the list.
        old_letters_guessed (list): The list of previously guessed letters.

    Returns:
        bool: Whether or not the new letter is valid and not already guessed.
        prints 'X' and sorted list of old letters guessed
            if the input is invalid.
    """
    if is_valid_input(letter_guessed) and \
            letter_guessed not in old_letters_guessed:
        old_letters_guessed.append(letter_guessed)
        return True

    # I know these can be one print function call
    # but these are two different actions so I had prefered
    # writing two print calls
    print('X')
    # print all guessed letters, sorted, with arrows, if there are any
    if len(old_letters_guessed) != 0:
        print(' -> '.join(sorted(old_letters_guessed)))
    return False


def show_hidden_word(secret_word, old_letters_guessed):
    """
    Returns the secret word with unguessed letters replaced by underscores.

    Args:
        secret_word (str): The secret word to be guessed.
        old_letters_guessed (list): The list of previously guessed letters.

    Returns:
        str: The secret word with unguessed letters replaced by underscores
        and spaces between characters.
    """
    for letter in list(secret_word):
        if letter not in old_letters_guessed:
            secret_word = secret_word.replace(letter, '_')

    # creating the spaces between the characters
    return ' '.join(list(secret_word))


def check_win(secret_word, old_letters_guessed):
    """
    Checks if the player has won by guessing all letters in the secret word.

    Args:
        secret_word (str): The secret word to be guessed.
        old_letters_guessed (list): The list of previously guessed letters.

    Returns:
        bool: Whether or not all letters in the secret word have been guessed.
    """
    for letter in list(secret_word):
        if letter not in old_letters_guessed:
            return False

    return True


def main():
    """
    Main function of the program.
    Starting point and game loop.
    """
    print(OPENING_SCREEN)

    filename = input('Enter filename: ')
    index = ''

    while not index.isnumeric():
        index = input('Enter index: ')

    wordsnum, secret_word = choose_word(filename, int(index))
    if wordsnum == 0:
        print('invalid file.')
        return

    old_letters_guessed = []
    number_of_tries = 0

    print('LET THE GAME BEGIN!\n')

    # initial print
    print_hangman(number_of_tries)
    print(show_hidden_word(secret_word, old_letters_guessed))

    # game loop
    while (not check_win(secret_word, old_letters_guessed)) \
            and number_of_tries < MAX_TRIES:
        is_letter_valid = False
        # repeat untill input is valid
        while not is_letter_valid:
            # lower() is for handling caps
            letter_guessed = input('Guess a letter: ').lower()
            is_letter_valid = \
                try_update_letter_guessed(letter_guessed, old_letters_guessed)
        # bad guess
        if letter_guessed not in secret_word:
            print(':(')
            number_of_tries += 1
            print_hangman(number_of_tries)

        # print the hidden word
        print(show_hidden_word(secret_word, old_letters_guessed))

    if number_of_tries >= MAX_TRIES:
        print('LOSE')
    else:
        print('WIN')


if __name__ == '__main__':
    main()
