import json
trie = {}
sentences ={}

def get_data_from_file(file_name):
    the_file = open(file_name)
    return the_file.read().split("\n")

def add_sentence_to_data(sentence,index,source):
    sentences[index] = {"sentence": sentence, "source": source}

def add_sub_to_trie(sub,id,offset):
    tmp_trie = trie
    for letter in sub:
        if letter not in tmp_trie.keys():
            tmp_trie[letter] = {}
            tmp_trie[letter]['sentences_ids'] = [{'id':id,'offset':offset}]
        else:
            tmp_trie[letter]['sentences_ids'].append({'id':id,'offset':offset})
        tmp_trie = tmp_trie[letter]

def add_sentence_to_trie(sentence,id):
    for index in range(len(sentence)+1):
        add_sub_to_trie(sentence[index:],id,index)



def init_data():
    data = get_data_from_file("data.txt")
    data += get_data_from_file("freedom.txt")
    for index,sentence in enumerate(data):
        add_sentence_to_trie(sentence.lower(),index)
        add_sentence_to_data(sentence,index,"data.txt")
    data_for_file= {"sentences":sentences,"trie":trie}
    with open("data.json", "w") as data_file:
        json.dump(data_for_file ,data_file)
    # print(data)
    # print(trie)

init_data()