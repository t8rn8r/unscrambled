import pickle
import collections
from more_itertools import powerset
from dictionary_trie import TrieNode, Trie
from wordfreq import word_frequency
import csv


# global_text = "".join(sorted("tiwashencneton")) # this is Tate's labyrinth puzzle
# global_text = "".join(sorted("ckkiaomgnilotirldb")) # 'to kill a mockingbird'
global_text = "".join(sorted("otebroontbtoe"))  # 'to be or not to be'

phrases = Trie()
phrase_count = 0


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
        global phrase_count
        phrase_count += 1
        phrases.insert(current_phrase)
        print("%i phrases found!" % phrase_count, end='\r')

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

    ################################
    # THIS PART IS FOR YOU! ########
    ################################

    # only choose the best n words
    n = 200
    # bigger 'b' prefers longer words; smaller 'b' chooses more frequent words.
    b = 1
    # only consider words at least 'l' letters long
    l = 2
    # include these words even if they're too short
    whitelist = ['a', 'i', 'be', 'to', 'or', 'and']
    # don't include these words no matter what
    blacklist = ['bo', 'botonee', 'tort', 'bott', 'brot', 'ro',
                 'ort', 'bor', 'tornote', 'bobo', 'tenter', 'oto',
                 'terton', 'te', 'neebor', 'boreen', 'bon', 'boort', 
                 'betone', 'otto', 'oberon']

    ################################

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
                word, 'en', wordlist='small', minimum=0) * pow(b, len(word))
    
    # sort by my custom scoring for each word
    word_freq = dict(
        sorted(word_freq.items(), key=lambda item: item[1], reverse=True))
    print()
    print("%i potential words found!" % len(word_freq))

    new_words = Trie()
    count = 0
    for word in word_freq:
        if (len(word) >= l or word in whitelist) and word not in blacklist:
            count += 1
            if count == n:
                break
            new_words.insert(word)

    get_phrases(global_text, dict(new_words.query('')))

    with open('output.csv', 'w') as outfile:
        csvwriter = csv.writer(outfile)
        for phrase in phrases.query_phrases():
            for word in phrase:
                decoded_words = allwords.codex[word]
                csvwriter.writerow(decoded_words)
            csvwriter.writerow("")

    print('\ndone')


if __name__ == '__main__':
    main()
