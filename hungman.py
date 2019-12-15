#!/usr/bin/env python
# coding: utf-8

# In[109]:


# Problem Set 2, hangman.py
# Name: Pavlovska Kate
# Collaborators:NONE
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
    values, tmp_counter = set(secret_word), 0
    for tmp_letter_guessed in values:
        if tmp_letter_guessed in letters_guessed:
            tmp_counter += 1
    if tmp_counter == len(values):
        return True
    return False


def get_guessed_word(secret_word, letters_guessed):
    tmp_string_unknown, set_value = ['_' for tmp in range(0, len(secret_word), 1)], list(secret_word)
    for tmp in range(0, len(set_value), 1):
        if set_value[tmp] in letters_guessed:
            tmp_string_unknown[tmp] = set_value[tmp]
    tmp_string_unknown = ''.join(tmp_string_unknown)
    return tmp_string_unknown


def get_available_letters(letters_guessed):
    all_available_letters, letters = list('abcdefghijklmnopqrstuvwxyz'), []
    for tmp in all_available_letters:
        if tmp not in letters_guessed:
            letters.append(tmp)
    return ' '.join(letters)


def hangman(secret_word):
    word = ''.join(['_' for tmp in range(0, len(secret_word))])
    counters, warnings, set_with_used_letters = 6, 3, []

    print("Welcome to Hangman")
    print('I am thinking of a word that is', len(secret_word), 'letters long.')
    print('You have counters', counters, 'guesses left.')
    tmp_variants, letters_to_join = input('Print your letters with space:').split(' '), []

    for tmp in tmp_variants:
        if len(tmp) == 1 and not tmp.istitle() and tmp.isalpha():
            letters_to_join.append(tmp)
    if len(letters_to_join) > 5:
        letter_to_join = letters_to_join[0:5]
    set_with_used_letters = list(set(set_with_used_letters + letters_to_join))
    print(get_guessed_word(secret_word, set_with_used_letters))
    print('Available letters:', get_available_letters(set_with_used_letters), '\n')
    while counters > 0:
        counters -= 1
        guested = len(secret_word)

        def value_func(warnings):
            try:
                letter_to_join = input('Print your letter:')[0]
                if letter_to_join in set_with_used_letters:
                    warnings -= 1
                    print('Warning, you used this letter')
                    return value_func(warnings)

                elif letter_to_join.istitle() or not letter_to_join.isalpha():
                    print('Invalid input')
                    return value_func(warnings)
            except IndexError:
                print('Invalid length')
                return value_func(warnings)

            return letter_to_join, warnings

        letter_to_join, warnings = value_func(warnings)
        set_with_used_letters = list(set(set_with_used_letters + list(letter_to_join)))
        word = get_guessed_word(secret_word, set_with_used_letters)
        print(word)
        for tmp in word:
            if tmp != '_':
                guested -= 1
        if guested == 0:
            break

        if warnings < 3:
            print('You have only', warnings, 'wanrnings left')
        elif warnings < 1:
            break

        print('I am thinking of a word that is', len(secret_word), 'letters long.')
        print('You have counters', counters, 'guesses left.')
        print('Available letters:', get_available_letters(set_with_used_letters))
        print('---------------------------------------')
    if '_' not in word:
        print('Congratulations, you won!')
    else:
        print('The right word is', secret_word)
    print('Your total score for this game is:', len(set_with_used_letters) * counters)
    return len(set_with_used_letters) * counters


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
        if other_word[tmp] != my_word[tmp] and my_word[tmp] != '_':
            return False
    return True


def show_possible_matches(my_word):
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    suitable_words = []
    for word in wordlist:
        regex = '^%s$' % my_word.replace("_", "[a-z]")
        if re.match(regex, word):
            suitable_words.append(word)

    return suitable_words


def hangman_with_hints(secret_word):
    word = ''.join(['_' for tmp in range(0, len(secret_word))])
    counters, warnings, set_with_used_letters = 6, 3, []

    print("Welcome to Hangman")
    print('I am thinking of a word that is', len(secret_word), 'letters long.')
    print('You have counters', counters, 'guesses left.')
    tmp_variants, letters_to_join = input('Print your letters with space:').split(' '), []

    for tmp in tmp_variants:
        if len(tmp) == 1 and not tmp.istitle() and tmp.isalpha():
            letters_to_join.append(tmp)
    if len(letters_to_join) > 5:
        letter_to_join = letters_to_join[0:5]
    set_with_used_letters = list(set(set_with_used_letters + letters_to_join))
    print(get_guessed_word(secret_word, set_with_used_letters))
    print('Available letters:', get_available_letters(set_with_used_letters), '\n')
    while counters > 0:
        counters -= 1
        guested = len(secret_word)

        def value_func(warnings):
            try:
                letter_to_join = input('Print your letter:')[0]
                if letter_to_join == '*':
                    print('Possible word matches are:', show_possible_matches(word))
                    return value_func(warnings)

                if letter_to_join in set_with_used_letters:
                    warnings -= 1
                    print('Warning, you used this letter')
                    return value_func(warnings)

                elif letter_to_join.istitle() or not letter_to_join.isalpha():
                    print('Invalid input')
                    return value_func(warnings)
            except IndexError:
                print('Invalid length')
                return value_func(warnings)

            return letter_to_join, warnings

        letter_to_join, warnings = value_func(warnings)
        set_with_used_letters = list(set(set_with_used_letters + list(letter_to_join)))
        word = get_guessed_word(secret_word, set_with_used_letters)
        print(word)
        for tmp in word:
            if tmp != '_':
                guested -= 1
        if guested == 0:
            break
        if warnings < 1:
            break
        if warnings < 3:
            print('You have only', warnings, 'wanrnings left')

        print('I am thinking of a word that is', len(secret_word), 'letters long.')
        print('You have counters', counters, 'guesses left.')
        print('Available letters:', get_available_letters(set_with_used_letters))
        print('---------------------------------------')
    if '_' not in word:
        print('Congratulations, you won!')
    else:
        print('The right word is', secret_word)
    print('Your total score for this game is:', len(set_with_used_letters) * counters)
    return len(set_with_used_letters) * counters


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
    hangman(secret_word)

    ###############

    # To test part 3 re-comment out the above lines and
    # uncomment the following two lines.

    # secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)