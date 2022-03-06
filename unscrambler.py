import pickle
import collections
from more_itertools import powerset
from dictionary_trie import TrieNode, Trie
from wordfreq import word_frequency


# global_text = "".join(sorted("tiwashencneton"))
global_text = "".join(sorted("tiwashencneton"))

phrases = Trie()


def get_words(text, allwords):
    words = Trie()

    # Figure out all the possible words made from every combination of text
    combos = set(reversed(list(powerset(text))))
    n_combos = len(combos)
    count = 0
    # iterate through all combos from longest to shortest
    # print()
    for combo in combos:
        combo = "".join(combo)
        # count += 1
        # percent = count*100/n_combos
        # print("Checking all possible combinations...\t%02.1f%% done! (%i out of %i)" % (
        #     percent, count, n_combos), end='\r')

        if allwords.contains(combo):
            words.insert(combo)

    return words


def get_phrases(text, words_dict, current_phrase=[]):

    word_list = sorted(list(words_dict), key=len, reverse=True)

    if len(text) == 0:
        phrases.insert(current_phrase)
        print("%i phrases found!" % len(phrases.query_phrases()), end='\r')

    for word in word_list:
        words_dict.pop(word)

        new_text = text
        for c in word:
            new_text = new_text.replace(c, '', 1)

        new_words_trie = Trie()
        for w in words_dict:
            new_words_trie.insert(w)
        new_words = dict(get_words(new_text, new_words_trie).query(''))

        current_phrase.append(word)

        get_phrases(new_text, new_words, current_phrase)

        current_phrase.pop()


def main():

    allwords = Trie()
    with open("words_trie.data", "rb") as infile:
        allwords = pickle.load(infile)

    words = get_words(global_text, allwords)

    # Get the frequency of each of the words
    alphabetical_word_list = words.query('')
    word_freq = {}
    count = 0
    print()
    for alphabetical_word in alphabetical_word_list:
        # isolate the word from the "score"
        alphabetical_word = alphabetical_word[0]
        count += 1
        percent = count*100/len(alphabetical_word_list)
        print("Checking word frequencies...\t\t%02.1f%% done! (%i out of %i)" %
              (percent, count, len(alphabetical_word_list)), end='\r')
        # First, you have to "decode" the words from the codex
        codex_words = allwords.codex[alphabetical_word]
        for word in codex_words:
            # This gives each word a "frequency" proportional to its frequency and its length
            # word_freq[w] = word_frequency(w, 'en', wordlist='small', minimum=0) * pow(1000, len(w))
            word_freq[word] = word_frequency(
                word, 'en', wordlist='small', minimum=0) * pow(10, len(word))
    # sort by my custom scoring for each word
    word_freq = dict(
        sorted(word_freq.items(), key=lambda item: item[1], reverse=True))
    print()
    print("%i potential words found!" % len(word_freq))
    # clear phrases (just in case!)
    phrases = []
    get_phrases(global_text, dict(words.query('')))

    print()


if __name__ == '__main__':
    main()
