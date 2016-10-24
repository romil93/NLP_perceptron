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

    return file_content_tokenized

def calculate_alpha(feature_list, tokens, bias):
    val = 0
    for token in tokens:
        val += feature_list[token]
    val += bias
    return val

def update_weight_for_tokens(feature_list, tokens, y):
    for token in tokens:
        feature_list[token] = feature_list[token] + y
    return feature_list

def write_to_file(bias, feature_list):
    out = {}
    out["bias"] = bias
    out["model"] = feature_list
    target = open('per_model.txt', 'a')
    target.write(str(out))

def main_func():
    directory = sys.argv

    max_iterations = 20
    token_list = set()

    file_in_memory = {}

    for root, dirs, files in os.walk(directory[1]):
        for file in files:
            if file.endswith(".txt"):
                token_list = get_features(token_list, os.path.join(root, file))
                file_in_memory[os.path.join(root, file)] = get_file_tokens(os.path.join(root, file))

    feature_list = {}
    for item in token_list:
        feature_list[item] = 0

    y_spam = 1
    y_ham = -1
    bias = 0

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
                    alpha = calculate_alpha(feature_list, tokens, bias)
                    if (alpha * y) <= 0:
                        feature_list = update_weight_for_tokens(feature_list, tokens, y)
                        bias += y
                    # print(alpha, bias)
                    # for token in tokens:
                    #     print(token, feature_list[token]),
                    # print()
                # input()
    # pprint(feature_list)
    write_to_file(bias, feature_list)
    print(bias)

main_func()
