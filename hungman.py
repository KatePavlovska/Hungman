#!/usr/bin/env python
# coding: utf-8

# In[66]:


# Problem Set 2, hangman.py
# Name: Pavlovska Kate
# Collaborators: None
# Time spent: ~ 10 - 12 hrs

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import re

WORDLIST_FILENAME = "words.txt"
set_with_repeated = []
SET_WITH_USED_LETTERS = []


def load_words():
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    return random.choice(wordlist)


def is_word_guessed(secret_word, letters_guessed):
    values = set(secret_word)
    list_of_bools = map(lambda letter: True if letter in letters_guessed else False, values)
    return all(list(list_of_bools))


def get_guessed_word(secret_word, letters_guessed):
    tmp_string_unknown, set_value = ['_ ' for tmp in secret_word], list(secret_word)
    for tmp in range(0, len(set_value), 1):
        if set_value[tmp] in letters_guessed:
            tmp_string_unknown[tmp] = set_value[tmp]
    tmp_string_unknown = ''.join(tmp_string_unknown)
    return tmp_string_unknown


def get_available_letters(letters_guessed):
    all_available_letters = list('abcdefghijklmnopqrstuvwxyz')
    for tmp in all_available_letters:
        if tmp in letters_guessed:
            all_available_letters.remove(tmp)
    return ' '.join(all_available_letters)


def value_func(warnings):
    try:
        global set_with_repeated, SET_WITH_USED_LETTERS
        letter_to_join = input('Print your letter:')[0]
        if letter_to_join in SET_WITH_USED_LETTERS:
            warnings -= 1
            print('Warning, you used this letter')
            set_with_repeated.append(letter_to_join)
            return value_func(warnings)
        elif letter_to_join.istitle():
            letter_to_join = letter_to_join.lower()
        elif not letter_to_join.isalpha():
            print('Invalid input')
            return value_func(warnings)
    except IndexError:
        print('Invalid length')
        return value_func(warnings)

    return letter_to_join, warnings


def hangman(secret_word):
    global SET_WITH_USED_LETTERS, set_with_repeated
    word = '_' * len(secret_word)
    counter_of_trials, warnings = 6, 3

    print("Welcome to Hangman")
    print('I am thinking of a word that is', len(secret_word), 'letters long.')
    print('You have counters', counter_of_trials, 'guesses left.')
    print('Available letters:', get_available_letters(SET_WITH_USED_LETTERS), '\n')

    while counter_of_trials > 0:
        guested = len(secret_word)
        letter_to_join, warnings = value_func(warnings)
        if letter_to_join not in secret_word:
            print('Your guess is wrong')
            counter_of_trials -= 1
        SET_WITH_USED_LETTERS = list(set(SET_WITH_USED_LETTERS + list(letter_to_join)))
        word = get_guessed_word(secret_word, SET_WITH_USED_LETTERS)
        print(word)

        if is_word_guessed(secret_word, word):
            break

        if 0 < warnings < 3:
            print('You have only', warnings, 'warnings left')
        elif warnings < 1:
            counter_of_trials -= 1

        print('I am thinking of a word that is', len(secret_word), 'letters long.')
        print('You have counters', counter_of_trials, 'guesses left.')
        print('Available letters:', get_available_letters(SET_WITH_USED_LETTERS))
        print('---------------------------------------')

    if is_word_guessed(secret_word, word):
        print('Congratulations, you won!')
    else:
        print('The right word is', secret_word)
    print('Your total score for this game is:',
          (len(SET_WITH_USED_LETTERS) - len(set_with_repeated)) * counter_of_trials)

    return (len(SET_WITH_USED_LETTERS) - len(set_with_repeated)) * counter_of_trials


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
# (hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    '''
    if len(my_word) != len(other_word):
        return False
    for tmp in range(0, len(other_word), 1):
        if (other_word[tmp] != my_word[tmp] and my_word[tmp] != '_') or (
                other_word[tmp] != my_word[tmp] and my_word[tmp] == '_' and other_word[tmp] in my_word):
            return False
    return True


def show_possible_matches(my_word):
    # wordlist: list of strings
    wordlist = lo()
    suitable_words = []
    for word in wordlist:
        regex = '^%s$' % my_word.replace("_", "[a-z]")
        if re.match(regex, word):
            suitable_words.append(word)

    print(suitable_words)
    return 0


def value_func_f(word, warnings):
    try:
        global set_with_repeated, SET_WITH_USED_LETTERS
        letter_to_join = input('Print your letter:')[0]
        if letter_to_join == '*':
            print('Possible word matches are:', show_possible_matches(word))
            return value_func_f(word, warnings)
        if letter_to_join in SET_WITH_USED_LETTERS:
            warnings -= 1
            print('Warning, you used this letter')
            set_with_repeated.append(letter_to_join)
            return value_func_f(word, warnings)
        elif letter_to_join.istitle():
            letter_to_join = letter_to_join.lower()
        elif not letter_to_join.isalpha():
            print('Invalid input')
            return value_func_f(word, warnings)
    except IndexError:
        print('Invalid length')
        return value_func_f(word, warnings)
    return letter_to_join, warnings


def hangman_with_hints(secret_word):
    global SET_WITH_USED_LETTERS, set_with_repeated
    SET_WITH_USED_LETTERS.clear()
    set_with_repeated.clear()
    word = '_' * len(secret_word)
    counter_of_trials, warnings = 6, 3
    print("Welcome to Hangman")
    print('I am thinking of a word that is', len(secret_word), 'letters long.')
    print('You have counters', counter_of_trials, 'guesses left.')
    print('Available letters:', get_available_letters(SET_WITH_USED_LETTERS), '\n')

    while counter_of_trials > 0:
        guested = len(secret_word)
        word = get_guessed_word(secret_word, SET_WITH_USED_LETTERS)
        letter_to_join, warnings = value_func_f(word, warnings)
        if letter_to_join not in secret_word:
            print('Your guess is wrong')
            counter_of_trials -= 1
        SET_WITH_USED_LETTERS = list(set(SET_WITH_USED_LETTERS + list(letter_to_join)))
        word = get_guessed_word(secret_word, SET_WITH_USED_LETTERS)
        print(word)

        if match_with_gaps(secret_word, word):
            break

        if 0 < warnings < 3:
            print('You have only', warnings, 'warnings left')
        elif warnings < 1:
            counter_of_trials -= 1

        print('I am thinking of a word that is', len(secret_word), 'letters long.')
        print('You have counters', counter_of_trials, 'guesses left.')
        print('Available letters:', get_available_letters(SET_WITH_USED_LETTERS))
        print('---------------------------------------')

    if is_word_guessed(secret_word, word):
        print('Congratulations, you won!')
    else:
        print('The right word is', secret_word)
    print(SET_WITH_USED_LETTERS, set_with_repeated)
    print('Your total score for this game is:',
          (len(SET_WITH_USED_LETTERS) - len(set_with_repeated)) * counter_of_trials)

    return (len(SET_WITH_USED_LETTERS) - len(set_with_repeated)) * counter_of_trials


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.
if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    wordlist = load_words()
    secret_word = choose_word(wordlist)
    # hangman(secret_word)

    ###############

    # To test part 3 re-comment out the above lines and
    # uncomment the following two lines.

    # secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)