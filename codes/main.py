# -*- coding: utf-8 -*-
import trie
import string
import nltk
from nltk.tokenize import TweetTokenizer

def check_word(trie, word):
    suggest_list = []
    if check_dictionary(trie, word) == False:
        for i in range(3):
            if len(suggest_list) > 5:
                break
            edited_word_list = edit_word_once(word)
            for edited_word in edited_word_list:
                if len(suggest_list) > 5:
                    break
                if check_dictionary(trie, edited_word) == True:
                    suggest_list.append(edited_word)
        if len(suggest_list) == 0:
            suggest_list.append('No suggestion')
    return suggest_list

def edit_word_once(word):
    splits = []
    delete_list = []
    traspose_list = []
    replace_list = []
    insert_list = []
    result = []
    for i in range(len(word) + 1):
        splits.append((word[0:i], word[i:]))
    for (a, b) in splits:
        if len(b) >= 1:
            delete_list.append(a + b[1:])
            for c in string.ascii_lowercase:
                replaced_word = a + c + b[1:]
                if word == replaced_word:
                    continue
                replace_list.append(replaced_word)
        if len(b) >= 2:
            second_half = b[1] + b[0] + b[2:]
            traspose_list.append(a + second_half)
        for c in string.ascii_lowercase:
            insert_list.append(a + c + b)
    result = delete_list + traspose_list + replace_list + insert_list
#    print(splits)
#    print(delete_list)
#    print(traspose_list)
#    print(replace_list)
#    print(insert_list)
#    print(result)
    return result

def check_dictionary(trie, word):
    return trie.find(word)

def load_dictionary_from_json(filepath):
    with open(filepath) as dictionary_file:
        words = set(dictionary_file.read().split())
    return words

def load_dictionary_from_txt(filepath):
    with open(filepath) as dictionary_file:
        words = dictionary_file.readlines()
    return words

def load_dictionary_to_trie(words, trie):
    for word in words:
        trie.insert(word.strip())

if __name__ == '__main__':
    trie = trie.Trie()
    words = load_dictionary_from_txt('data/google-10000-english-usa.txt')
    load_dictionary_to_trie(words, trie)
    #print(trie.find('ternary'))
    #print(trie.find('aa'))
    #edit_word_once('test')
    #print(check_word(trie, 'tesa'))
    text = input('input text:')
    #tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    tokenizer = TweetTokenizer()
    s = tokenizer.tokenize(text)
    #print(s)
    for word in s:
        print(word + repr(check_word(trie, word)))
