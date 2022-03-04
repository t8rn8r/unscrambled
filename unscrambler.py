import pickle
import collections
from more_itertools import powerset
from dictionary_trie import TrieNode, Trie


text = "".join(sorted("tiwashencneton"))


def main():

    allwords = Trie()
    words = Trie()

    with open("words_trie.data", "rb") as infile:
        allwords = pickle.load(infile)

    combos = reversed(list(powerset(text)))
    for combo in combos:
        print(combo)

    print()


if __name__ == '__main__':
    main()
