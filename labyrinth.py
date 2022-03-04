import random
import json
import csv
from wordfreq import word_frequency
import itertools as Iter

# known_word = "minotaur" # put /all/ the letters in letters, not just the unknown ones
# startletters = "tiw"
# letters = "minotaurashencnetontiw" # I use user input instead of global variables now

# this is a sloppy way of eliminating duplicates in getCandidates()
visited = {}


def histogram(letters):
    """
    Creates a frequency histogram of the given letters
    Input: letters -- word or scrambled letters
    Output: dictionary mapping from letters to the # of occurences of that letter
    """
    d = dict()
    for letter in letters:
        if letter in d:
            d[letter] += 1
        else:
            d[letter] = 1

    return d


def isSubhist(hist1, hist2):
    """
    Checks if hist1 is a subset of hist2
    Input: hist1, hist2 -- dictionary histograms
    Output: Boolean
    """

    for letter in hist1:

        if letter not in hist2:
            return False

        if hist1[letter] > hist2[letter]:
            return False

    return True


def getWordsStartWith(words, start):
    """
    Returns the subset of words that start with the letter "start"
    Input: words -- set, dict, or list of words
           start -- starting character
    Output: Set of words starting with "start"
    """
    return set([word for word in words if word[0] == start])


def getCandidatesStartWith(all_words, start, letters):
    """
    Finds words that could be created with the given letters
    Input: all_words -- set, dict, or list of words
           start -- starting character
           letters -- scrambled letters to make words from
    Output: Set of words starting with "start", and containing only "letters"
    """
    words = getWordsStartWith(all_words, start)
    # since we removed the starting letters, we have to put the current startletter back in the count
    available = histogram(letters + start)

    candidates = {}
    for word in words:
        # if the new word is too long, don't even try!
        if len(word) > len(letters):
            continue

        # now, check if the word fits with our remaining letters
        if isSubhist(histogram(word), available):
            candidates[word] = {}

    return candidates


def getCandidates(words, letters, current_phrase=list(), current_score=0):
    """
    Finds words that could be created with the given letters
    Input:  all_words -- set, dict, or list of words
            letters -- scrambled letters to make words from
    Output: Set of words containing only letters
    """
    available = histogram(letters)

    remaining_words = words.copy()
    for word in words:

        if len(word) > len(letters):
            remaining_words.pop(word)
            continue

        if len(word) < 3:
            remaining_words.pop(word)
            continue

        if not isSubhist(histogram(word), available):
            remaining_words.pop(word)
            continue
        else:
            remaining_letters = letters
            for char in word:
                remaining_letters = remaining_letters.replace(char, '', 1)

            getCandidates(remaining_words, remaining_letters,
                          current_phrase + [word], current_score + words[word])


    if letters == '':

        

        with open("output.csv", "a") as outfile:

            writer = csv.writer(outfile)

            output_phrase = current_phrase.copy()
            output_phrase.insert(0, current_score)
            writer.writerow(output_phrase)

    return


def main():
    """
    create phrases with only the given global "letters" and rank according to usage frequency
    """

    words = {}

    # get the text to unscramble from user input
    letters = ""
    while letters == "":
        # letters = input("\nEnter the complete text to unscramble:\n") TODO uncomment
        letters = "minotaurtiwashencneton"  # TODO remove
        if letters == "":
            print("You have to give me some text to unscramble!\n")

    print("\nHere's what you entered: " + letters + "\n\n")

    # get any known words from user input. all the letters in that word will be totally removed from consideration.
    # known_word = "" TODO uncomment
    # known_word = input("Is there a word you KNOW is in the unscrambled phrase?\n(If not, just press Enter)\n(If there are multiple words, enter them without spaces "likethis"):\n")
    known_word = "minotaur"  # TODO remove
    # if a known word is provided, remove its letters from 'letters'
    if known_word != "":
        print("\nHere's what you entered: " + known_word)
        for char in known_word:
            letters = letters.replace(char, '', 1)
        print("\nHere're the scrambled letters that remain: " + letters + "\n\n")
    else:
        print("\nNo known words! That's okay!\n\n")

    # get start letters from user input
    startletters = ""
    # # startletters = input("If you know the letters that the words in the phrase start with, enter them here with no spaces or punctuation:\nIf not, just press enter.\n") TODO uncomment
    # startletters = "tiw"  # TODO remove
    # if startletters != "":
    #     print("\nHere are the letters you entered: ", end='')
    #     for char in startletters:
    #         print(char + ", ", end='')
    #         letters = letters.replace(char, '', 1)
    #     print("\nAnd here are the remaining letters: " + letters)
    #     print("\nStarting letters: " + startletters + "\n\n")

    # else:
    #     startletters = letters
    #     print("\nNo kown starting letters! That's okay! We'll just check all the remaining letters: " + letters + "\n\n")

    # after all the user input, make a histogram of the remaining letters:
    totalletters = letters + startletters
    totalhist = histogram(totalletters)
    totallen = len(totalletters)

    # Opening JSON file
    with open("words_dictionary_sorted.json") as json_file:
        print("Please wait while I search! (This WILL take a while!)\nSeriously... you computer isn't frozen. Get comfy...\n")

        # get the list of all words
        words = json.load(json_file)
        # get all the words that might be in the scrambled text
        getCandidates(words, letters)

        print()

        for t in t_words:
            for i in i_words:
                for w in w_words:
                    if (histogram(t+i+w) == totalhist):
                        phrase = (t+" "+i+" "+w)
                        phrase += " "+known_word

                        wf = word_frequency(t, "en", wordlist='small', minimum=0.0) * \
                            word_frequency(i, "en", wordlist='small', minimum=0.0) * \
                            word_frequency(
                                w, "en", wordlist='small', minimum=0.0)

                        phrases[phrase] = wf

        print(
            dict(sorted(phrases.items(), key=lambda item: item[1], reverse=True)))


if __name__ == '__main__':
    main()
