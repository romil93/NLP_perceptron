import os, sys

directory = sys.argv


file_open = open(directory[1], "r", encoding="latin1")
file_content = file_open.read()

file_content_tokenized = file_content.split("\n")

correctly_classified_spam = 0
correctly_classified_ham = 0

classified_as_spam = 0
classified_as_ham = 0

actual_spam = 0
actual_ham = 0

for line in file_content_tokenized:
	label_path = line.split(" ", 1)
	if len(label_path) == 2:
		label = label_path[0]
		path = label_path[1]

		if label == "SPAM":
			classified_as_spam += 1
		else:
			classified_as_ham += 1

		if "spam" in path:
			if label == "SPAM":
				correctly_classified_spam += 1

			actual_spam += 1

		elif "ham" in path:
			if label == "HAM":
				correctly_classified_ham += 1

			actual_ham += 1

precision_spam = correctly_classified_spam / classified_as_spam
precision_ham =  correctly_classified_ham / classified_as_ham

recall_spam = correctly_classified_spam / actual_spam
recall_ham = correctly_classified_ham / actual_ham

f1score_spam = (2 * precision_spam * recall_spam) / (precision_spam + recall_spam)
f1score_ham = (2 * precision_ham * recall_ham) / (precision_ham + recall_ham)

print("SPAM:\n==========")
print("precision:", precision_spam, "recall:", recall_spam, "f1 score:", f1score_spam)
print("HAM:\n========")
print("precision:", precision_ham, "recall:", recall_ham, "f1 score:", f1score_ham)