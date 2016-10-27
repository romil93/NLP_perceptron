import os, sys
from pprint import pprint
import math, random

def get_features(token_list, file):
    file_open = open(file, "r", encoding="latin1")
    file_content = file_open.read()

    file_content_tokenized = set(file_content.split())
    token_list.update(file_content_tokenized)
    return token_list

def get_file_tokens(file):
    file_open = open(file, "r", encoding="latin1")
    file_content = file_open.read()

    file_content_tokenized = file_content.split()

    word_count_dict = {}
    for token in file_content_tokenized:
        if token in word_count_dict:
            word_count_dict[token] += 1
        else:
            word_count_dict[token] = 1

    return word_count_dict
    

def calculate_alpha(feature_list, bias, file_word_count):
    val = 0
    for token in file_word_count:
        val += (feature_list[token] * file_word_count[token])
    val += bias
    return val

def update_weight_for_tokens(feature_list, file_word_count, y):
    for token in file_word_count:
        feature_list[token] = feature_list[token] + ( y * file_word_count[token] )
    return feature_list

def write_to_file(bias, feature_list):
    out = {}
    out["bias"] = bias
    out["model"] = feature_list
    target = open('per_model.txt', 'w', encoding="latin1")
    target.write(str(out))

def main_func():
    directory = sys.argv

    max_iterations = 20
    token_list = set()
    
    file_word_count = {}
    for root, dirs, files in os.walk(directory[1]):
        for file in files:
            if file.endswith(".txt"):
                token_list = get_features(token_list, os.path.join(root, file))
                file_word_count[os.path.join(root, file)] = get_file_tokens(os.path.join(root, file))                                

    feature_list = {}
    for item in token_list:
        feature_list[item] = 0

    y_spam = 1
    y_ham = -1
    bias = 0

    num_features = len(feature_list)

    for i in range(max_iterations):
        for root, dirs, files in os.walk(directory[1]):
            random.shuffle(files)
            for file in files:
                y = 0
                if file.endswith(".txt"):
                    if ".spam.txt" in file:
                        y = y_spam
                    elif ".ham.txt":
                        y = y_ham

                    if y != 0:
                        alpha = calculate_alpha(feature_list, bias, file_word_count[os.path.join(root, file)])
                        if (alpha * y) <= 0:
                            feature_list = update_weight_for_tokens(feature_list, file_word_count[os.path.join(root, file)], y)
                            bias += y

    write_to_file(bias, feature_list)
    print(bias)

main_func()
