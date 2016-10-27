import os, sys

def reading():
    s = open('per_model.txt', 'r', encoding="latin1").read()
    return eval(s)

def get_file_tokens(file):
    feature_list = {}
    file_open = open(file, "r", encoding="latin1")
    file_content = file_open.read()

    file_content_tokenized = file_content.split()
    for word in file_content_tokenized:
            feature_list[word] = 0
    return feature_list

def calculate_alpha(feature_list, tokens, bias):
    val = 0
    for token in tokens:
        if token in feature_list:
            val += feature_list[token]
    val += bias
    return val

def write_to_file(target, line):
    target.write(str(line))

def main_func():
        directory = sys.argv
        model_content = reading()
        output_file_name = directory[2]
        bias = model_content["bias"]
        feature_list = model_content["model"]
        target = open(output_file_name, 'a')


        for root, dirs, files in os.walk(directory[1]):
            for file in files:
                if file.endswith(".txt"):
                    tokens = get_file_tokens(os.path.join(root, file))
                    alpha = calculate_alpha(feature_list, tokens, bias)

                    if alpha > 0:
                        write_to_file(target, "SPAM " + os.path.join(root, file) + "\n")
                    else:
                        write_to_file(target, "HAM " + os.path.join(root, file) + "\n")
                    # if "spam" in file:
                    #     if alpha > 0:
                    #         print(alpha,"spam","spam",file)
                    #     else:
                    #         print(alpha,"spam","ham",file)
                    # else:
                    #     if alpha > 0:
                    #         print(alpha,"ham","spam",file)
                    #     else:
                    #         print(alpha,"ham","ham",file)
main_func()
