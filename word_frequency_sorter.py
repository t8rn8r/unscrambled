import json

with open("words_dictionary_freq.json") as inputfile:

    input_dict = json.load(inputfile)

    sorted_dict = dict(sorted(input_dict.items(), key=lambda item: item[1], reverse=True))

    with open("words_dictionary_sorted.json", "w") as outputfile:

        output = json.dumps(str(sorted_dict), indent=4)
    
        outputfile.write(output)