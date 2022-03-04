import json
import pickle

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
    
    def insert(self, words):
        
        for word in words:

            node = self.root

            sorted_word = "".join(sorted(word))

            if sorted_word in self.codex:
                self.codex[sorted_word].append(word)
            else:
                self.codex[sorted_word] = [word]

            for char in sorted_word:
                if char in node.children:
                    node = node.children[char]
                else:
                    new_node = TrieNode(char)
                    node.children[char] = new_node
                    node = new_node

            # this marks where we've run out of characters in a word
            node.is_end = True

            # TODO put an actual score in here using word frequency
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

    
    def contains(self, string):
        
        self.output = []
        node = self.root 

        for char in string:
            if char in node.children:
                node = node.children[char]
            else:
                return False

        return node.is_end


def main():
    trie = Trie()
    trie.insert(["a", "ab", "abc", "ac", "abcd", "acd", "abd", "aabd"])

    print(trie.contains("ab"))


def make_dict():
    
    words = Trie()
    word_codex = {}

    with open("words_dictionary_sorted.json") as infile:
        
        input_dict = json.load(infile)

        words.insert(input_dict)
        word_codex = words.getCodex()

    # https://docs.python.org/3/library/pickle.html 
    with open("words_trie.data", "wb") as outfile:
        pickle.dump(words, outfile, pickle.HIGHEST_PROTOCOL)

    with open("words_codex.data", "wb") as outfile:
        pickle.dump(word_codex, outfile, pickle.HIGHEST_PROTOCOL)




if __name__ == '__main__':
    main()