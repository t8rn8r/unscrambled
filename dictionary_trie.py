import json
import pickle
from nltk.corpus import words

# could use this instead: https://tutorialedge.net/compsci/data-structures/getting-started-with-tries-in-python/

# I actually used this: https://albertauyeung.github.io/2020/06/15/python-trie.html/


class TrieNode:
    def __init__(self, char):
        self.char = char
        self.is_end = False
        self.counter = 0
        self.children = {}


class Trie(object):

    def __init__(self):
        self.root = TrieNode('')
        self.codex = {}

    def insert(self, word):

        node = self.root

        if type(word) == type('this is a hack!'):
            # sort the word's letters in alphabetical order to reduce mess
            sorted_word = "".join(sorted(word))
            # add the unsorted word to the codex under its sorted entry
            if sorted_word in self.codex:
                self.codex[sorted_word].append(word)
            else:
                self.codex[sorted_word] = [word]
            # actually insert the word, character by character
            for char in sorted_word:
                if char in node.children:
                    node = node.children[char]
                else:
                    new_node = TrieNode(char)
                    node.children[char] = new_node
                    node = new_node
            # this marks where we've run out of characters in a word
            node.is_end = True
            # TODO put an actual score in here using word frequency or something
            node.counter += 1
        
        if type(word) == type(['this','is','also','a','hack']):
            sorted_phrase = sorted(word)
            # no need for a codex here!
            for word in sorted_phrase:
                if word in node.children:
                    node = node.children[word]
                else:
                    new_node = TrieNode(word)
                    node.children[word] = new_node
                    node = new_node
            node.is_end = True
            node.counter += 1


    def dfs(self, node, prefix):

        if node.is_end:
            self.output.append((prefix + node.char, node.counter))

        for child in node.children.values():
            self.dfs(child, prefix + node.char)

    def query(self, prefix):

        self.output = []
        node = self.root

        for char in prefix:
            if char in node.children:
                node = node.children[char]
            else:
                return []

        self.dfs(node, prefix[:-1])

        return sorted(self.output, key=lambda prefix: prefix[1], reverse=True)

    def dfs_phrase(self, node, prefix):
        if len(node.children) == 0:
            self.output.append(prefix + [node.char])

        for child in node.children.values():
            self.dfs_phrase(child, prefix + [node.char])
    
    def query_phrases(self):
        self.output = []
        node = self.root 

        for word in node.children:
            self.dfs_phrase(node.children[word], [])

        return self.output

    def contains(self, string):

        node = self.root

        for char in string:
            if char in node.children:
                node = node.children[char]
            else:
                return False

        return node.is_end


def make_dict():

    words_trie = Trie()
    word_list = words.words()
    word_list = [x.lower() for x in word_list]
    word_list = set(word_list)

    for word in word_list:
        words_trie.insert(word)

    # https://docs.python.org/3/library/pickle.html
    with open("words_trie.data", "wb") as outfile:
        pickle.dump(words, outfile, pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    make_dict()
