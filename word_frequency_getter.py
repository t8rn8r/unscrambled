from wordfreq import word_frequency
import json

sorted_words = {}

with open("words_dictionary.json") as json_file:
    all_words = json.load(json_file)
    
    for word in all_words:
        all_words[word] = word_frequency(word, "en", wordlist='small', minimum=0.0)

    with open("words_dictionary_freq.json", "w") as outfile:
        output = json.dumps(all_words, indent=4)
        outfile.write(output)