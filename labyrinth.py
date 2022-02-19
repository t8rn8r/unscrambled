import random
import json
from wordfreq import word_frequency

known_word = "minotaur"
letters = "ashencneton"
startletters = "tiw"


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
        if letter not in hist2 or hist1[letter] > hist2[letter]:
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


def getCandidates(all_words, start, letters):
    """
    Finds words that could be created with the given letters
    Input: all_words -- set, dict, or list of words
           start -- starting character
           letters -- scrambled letters to make words from
    Output: Set of words starting with "start", and containing only "letters"
    """
    words = getWordsStartWith(all_words, start)
    available = histogram(letters + start)

    candidates = set()
    for word in words:
        if isSubhist(histogram(word), available):
            candidates.add(word)
    return candidates


def permute(words, visited=[], phrases=[]):

    visited.append(words.pop())

    print(visited)

    if len(words) == 0:
        return phrases
    else:
        return permute(words, visited, phrases)


def main():
    """
    create phrases with only the given global "letters" and rank according to usage frequency
    """

    print("histogram: " + str(histogram("test")))

    words = {}

    # get the text to unscramble from user input
    letters = ""
    while letters == "":
        # letters = input("\nEnter the complete text to unscramble:\n") TODO uncomment
        letters = "minotaurashencneton"  # TODO remove
        if letters == "":
            print("You have to give me some text to unscramble!\n")
    print("\nHere's what you entered: " + letters + "\n\n")

    # get any known words from user input
    # known_word = "" TODO uncomment
    # known_word = input("Is there a word you KNOW is in the unscrambled phrase?\n(If not, just press Enter):\n")
    known_word = "minotaur"  # TODO remove
    print("\nHere's what you entered: " + known_word + "\n\n")
    # if a known word is provided, remove its letters from 'letters'
    for char in known_word:
        letters = letters.replace(char, '', 1)

    # get start letters from user input
    startletters = ""
    # startletters = input("If you know the letters that the words in the phrase start with, enter them here with no spaces or punctuation:\nIf not, just press enter.\n") TODO uncomment
    startletters = "tiw"  # TODO remove
    if startletters != "":
        print("\nHere are the letters you entered: ", end='')
        for char in startletters:
            print(char + ", ", end='')
        print("\n\n")

    # Opening JSON file
    with open("words_dictionary.json") as json_file:
        print("Please wait while I search! (This WILL take a while!)\n")

        # get the list of all words
        words = json.load(json_file)
        # get all the words that might be in the scrambled text
        potential_words = set()
        for char in startletters:
            potential_words.update(getCandidates(words, char, letters))
            print(str(len(potential_words)) + " words found...", end='\r')
        print()

        totalhist = histogram(letters + "tiw")

        phrases = permute(potential_words)

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
