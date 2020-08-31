import json


the_file = open("data.json")
file_data = json.load(the_file)
trie = file_data['trie']
sentences = file_data['sentences']

def replace_score(query,index,offset):
    reduced_score_dict= {0:5,1:4,2:3,3:2}
    reduced_score = reduced_score_dict[index+offset] if index in  reduced_score_dict.keys() else 1
    return (index + len(query)) *2 - reduced_score


def delete_or_add_score(query,index,offset):
    reduced_score_dict= {0:10,1:8,2:6,3:4}
    reduced_score = reduced_score_dict[index+offset] if index in  reduced_score_dict.keys() else 2
    return (index + len(query)) *2 - reduced_score

def get_ids(ids_dict):
    return [dict['id'] for dict in ids_dict]

def by_sub(query,trie):
    tmp_trie = trie
    # print(tmp_trie)
    for letter in query:
        # print(letter)
        if letter in tmp_trie.keys():
            tmp_trie = tmp_trie[letter]
        else:
            return []

    return get_ids(tmp_trie['sentences_ids'])

def by_replace(query,trie,index):
    res = []
    suitable_sentences={}
    score = replace_score(query,index,0)

    for key in trie.keys():
        if key != "sentences_ids":
            res += by_sub(query[1:],trie[key])

    for r in res:
        suitable_sentences[r] = score

    return suitable_sentences

def by_delete(query,trie,index):
    res = []
    suitable_sentences = {}
    score =delete_or_add_score(query,index,0)
    for key in trie.keys():
        if key != "sentences_ids":
            res += by_sub(query, trie[key])
    for r in res:
        suitable_sentences[r] = score
    return suitable_sentences


def by_add(query,trie,index):
    if len(query) == 1:
        return []
    res = []
    suitable_sentences = {}
    score = delete_or_add_score(query,index,0)
    for key in trie.keys():
        if key != "sentences_ids" :
            res += by_sub(query[1:], trie)
    for r in res:
        suitable_sentences[r] = score
    return suitable_sentences


def by_change(query):
    tmp_trie = trie
    results = {}
    for index, letter in enumerate(query):
        results.update(by_replace(query[index:], tmp_trie, index))
        # print("after replace")
        # print(results)
        results.update(by_delete(query[index:], tmp_trie, index))
        # print("after delete")
        # print(results)
        results.update(by_add(query[index:], tmp_trie, index))
        # print("after update")
        # print(results)
        if letter in tmp_trie:
            tmp_trie = tmp_trie[letter]
        else:
            break
        # results += by_add(query[index:],tmp_trie,index)
        # results += by_delete(query[index:], tmp_trie,index)
    return results

def find_5_best_sentences(suitable_sentences):
    return [k for k,v in sorted(suitable_sentences.items(), reverse= True, key=lambda item: item[1])][:5]

def find_sentences(query):
    score = len(query) * 2
    suitable_sentences = {}
    res = by_sub(query, trie)
    if len(res) >= 5:
        suitable_5_best_sentences_ids = res[0:5]
    else:
        for r in res:
            suitable_sentences[r] = score
        # print(suitable_sentences)
        res_change = by_change(query)
        # print(res_change)
        # print(res_change)
        # print(suitable_sentences)
        for key in res_change:
            if key not in suitable_sentences:
                suitable_sentences[key] = res_change[key]
        # print(suitable_sentences)
        suitable_5_best_sentences_ids = find_5_best_sentences(suitable_sentences)
        # print(suitable_5_best_sentences_ids)
    for id in suitable_5_best_sentences_ids:
        # print(sen)
        print(sentences[str(id)]['sentence'],"  file:", sentences[str(id)]['source'])
