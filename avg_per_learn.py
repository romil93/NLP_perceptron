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

    return set(file_content_tokenized), word_count_dict

def calculate_alpha(feature_list, tokens, bias, file_word_count):
    val = 0
    for token in tokens:
        val += (feature_list[token] * file_word_count[token])
    val += bias
    return val

def update_weight_for_tokens(feature_list, tokens, y):
    for token in tokens:
        feature_list[token] = feature_list[token] + y
    return feature_list

def update_weight_for_avg_tokens(feature_list, tokens, y, c):
    for token in tokens:
        feature_list[token] = feature_list[token] + y*c
    return feature_list

def write_to_file(bias, feature_list):
    out = {}
    out["bias"] = bias
    out["model"] = feature_list
    target = open('per_model.txt', 'a')
    target.write(str(out))

def main_func():
    directory = sys.argv

    max_iterations = 30
    token_list = set()
    file_in_memory = {}
    
    file_word_count = {}
    for root, dirs, files in os.walk(directory[1]):
        for file in files:
            if file.endswith(".txt"):
                token_list = get_features(token_list, os.path.join(root, file))
                file_in_memory[os.path.join(root, file)], file_word_count[os.path.join(root, file)] = get_file_tokens(os.path.join(root, file))

    feature_list = {}
    avg_feature_list = {}

    for item in token_list:
        feature_list[item] = 0
        avg_feature_list[item] = 0

    y_spam = 1
    y_ham = -1

    bias = 0
    avg_bias = 0

    c = 1

    num_iterations = 0
    num_features = len(feature_list)

    for i in range(max_iterations):
        for root, dirs, files in os.walk(directory[1]):
            random.shuffle(files)
            for file in files:
                y = 0
                if file.endswith(".txt"):
                    if "spam" in file:
                        y = y_spam
                    else:
                        y = y_ham

                    tokens = file_in_memory[os.path.join(root, file)]
                    alpha = calculate_alpha(feature_list, tokens, bias,file_word_count[os.path.join(root, file)])
                    if (alpha * y) <= 0:
                        feature_list = update_weight_for_tokens(feature_list, tokens, y)
                        avg_feature_list = update_weight_for_avg_tokens(avg_feature_list, tokens, y, c)
                        bias += y
                        avg_bias += y*c
                    c = c + 1
                    # print(alpha, bias)
                    # for token in tokens:
                    #     print(token, feature_list[token]),
                    # print()
                # input()
    # pprint(feature_list)

    cal_support = 1/c
    for item in token_list:
        avg_feature_list[item] = feature_list[item] - (cal_support * avg_feature_list[item])
    avg_bias = bias - (cal_support * avg_bias)

    write_to_file(avg_bias, avg_feature_list)
    print(avg_bias)

main_func()
