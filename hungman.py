#!/usr/bin/env python
# coding: utf-8

# In[8]:


# Problem Set 2, hangman.py
# Name: Pavlovska Kate KM-93
# Collaborators:NONE
# Time spent: ~13 hour 

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string
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
    all_available_letters = [letter for letter in 'abcdefghijklmnopqrstuvwxyz' if letter not in letters_guessed]
    return ' '.join(all_available_letters)


def value_func(warnings, SET_WITH_USED_LETTERS, set_with_repeated):
    try:
        letter_to_join = input('Print your letter:')[0]
        if letter_to_join in SET_WITH_USED_LETTERS:
            warnings -= 1
            print('Warning, you used this letter')
            set_with_repeated.append(letter_to_join)
            return value_func(warnings, SET_WITH_USED_LETTERS, set_with_repeated)
        elif letter_to_join.istitle():
            letter_to_join = letter_to_join.lower()
        elif not letter_to_join.isalpha():
            print('Invalid input')
            return value_func(warnings, SET_WITH_USED_LETTERS, set_with_repeated)
    except IndexError:
        print('Invalid length')
        return value_func(warnings, SET_WITH_USED_LETTERS, set_with_repeated)

    return letter_to_join, warnings


def hangman(secret_word, SET_WITH_USED_LETTERS, set_with_repeated):
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
        letter_to_join, warnings = value_func(warnings, SET_WITH_USED_LETTERS, set_with_repeated)
        if letter_to_join not in secret_word and letter_to_join not in ['a', 'e', 'i', 'o', 'u', 'y']:
            print('Your guess is wrong')
            counter_of_trials -= 1
        elif letter_to_join not in secret_word and letter_to_join in ['a', 'e', 'i', 'o', 'u', 'y']:
            print('Your guess is wrong')
            counter_of_trials -= 2
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
        print('Your total score for this game is:', len(set(secret_word)) * counter_of_trials)
        return len(set(secret_word)) * counter_of_trials
    else:
        print('The right word is', secret_word)
        return 0


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
    my_word, other_word = [letter for letter in my_word if letter != ' '], list(other_word)
    if len(list(my_word)) != len(list(other_word)):
        return False
    for tmp in range(0, len(list(other_word)), 1):
        if (other_word[tmp] != my_word[tmp] and my_word[tmp] != '_') or (
                other_word[tmp] != my_word[tmp] and my_word[tmp] == '_' and other_word[tmp] in my_word):
            return False
    return True


def show_possible_matches(my_word, wordlist):
    wordlist = load_words()
    suitable_words = []
    print(my_word)
    for word in wordlist:
        #         regex = '^%s$' % my_word.replace("_ ", "[a-z]")
        if match_with_gaps(my_word, word):
            suitable_words.append(word)

    print(suitable_words)


def value_func_f(word, warnings, SET_WITH_USED_LETTERS, set_with_repeated, wordlist):
    try:
        letter_to_join = input('Print your letter:')[0]
        if letter_to_join == '*':
            show_possible_matches(word, wordlist)
            return value_func_f(word, warnings, SET_WITH_USED_LETTERS, set_with_repeated, wordlist)
        if letter_to_join in SET_WITH_USED_LETTERS:
            warnings -= 1
            print('Warning, you used this letter')
            set_with_repeated.append(letter_to_join)
            return value_func_f(word, warnings, SET_WITH_USED_LETTERS, set_with_repeated, wordlist)
        elif letter_to_join.istitle():
            letter_to_join = letter_to_join.lower()
        elif not letter_to_join.isalpha():
            print('Invalid input')
            return value_func_f(word, warnings, SET_WITH_USED_LETTERS, set_with_repeated, wordlist)
    except IndexError:
        print('Invalid length')
        return value_func_f(word, warnings, SET_WITH_USED_LETTERS, set_with_repeated, wordlist)
    return letter_to_join, warnings


def hangman_with_hints(secret_word, SET_WITH_USED_LETTERS, set_with_repeated, wordlist):
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
        letter_to_join, warnings = value_func_f(word, warnings, SET_WITH_USED_LETTERS,
                                                set_with_repeated, wordlist)
        if letter_to_join not in secret_word and letter_to_join not in ['a', 'e', 'i', 'o', 'u', 'y']:
            print('Your guess is wrong')
            counter_of_trials -= 1
        elif letter_to_join not in secret_word and letter_to_join in ['a', 'e', 'i', 'o', 'u', 'y']:
            print('Your guess is wrong')
            counter_of_trials -= 2

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
        print('Your total score for this game is:', len(set(secret_word)) * counter_of_trials)
        return len(set(secret_word)) * counter_of_trials
    else:
        print('The right word is', secret_word)
        return 0


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
    hangman(secret_word, SET_WITH_USED_LETTERS, set_with_repeated)

    ###############

    # To test part 3 re-comment out the above lines and
    # uncomment the following two lines.

    secret_word = choose_word(wordlist)
    wordlist = [word for word in wordlist if len(word) == len(secret_word)]
    hangman_with_hints(secret_word, SET_WITH_USED_LETTERS, set_with_repeated, wordlist)

# In[ ]: