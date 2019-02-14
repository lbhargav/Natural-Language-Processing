#####################################################################
'''
 # Bigram Model to find the probability of a sentence occurrence from a given corpus
 # @author Bhargav Lenka
'''
#####################################################################
# Importing libraries
import sys
import os
import math
import re
import pandas as pd
import numpy as np
import csv


# Function to extract words from the text
def extract_words(line):
    words = re.sub('[^a-zA-Z0-9\n\']', ' ', line)
    words_list = words.strip().split()
    words_list = [x.lower() for x in words_list]
    return words_list


# Function to get the vocabulary list and vocabulary dictionary count
def countVocab(myfile):
    vocab = set()
    vocabDict = {}
    with open(myfile, "r") as fileRead:
        lines = fileRead.readlines()
        for line in lines:
            words = extract_words(line)
            for word in words:
                vocab.add(word)
                vocabDict[word] = vocabDict.get(word, 0) + 1
    return vocabDict, vocab


# Function to match bigrams and count using regular expression
def matchBigrams(word1, word2, corpus):
    word1 = word1.strip()
    word2 = word2.strip()
    pattern = str(word1) + " " + str(word2)
    myfile = open(corpus, 'r')
    count = 0
    for line in myfile:
        match = re.findall(pattern, line, re.IGNORECASE)
        if (match != None):
            count = count + len(match)
    return (count)


# Function to count the bigram occorences corresponding to a statement
def bigramCountsForStatement(statement, corpus):
    words = extract_words(statement)
    # print(words)
    patternCounts = {}  # Dictionary to hold the bigram counts
    firstWord = None
    sen_words_set = []
    for firstWord in words:
        if not firstWord in sen_words_set:
            sen_words_set.append(firstWord)
        for secondWord in words:
            count = matchBigrams(firstWord, secondWord, corpus)
            if (firstWord, secondWord) not in patternCounts:
                patternCounts[firstWord, secondWord] = count
    return patternCounts, sen_words_set, words


# Function to create bigram table
def bigram_table(bigram_count, sen_words_set):
    bigram_count_list = np.reshape(list(bigram_count.values()), (len(sen_words_set), len(sen_words_set)))
    bigram_df = pd.DataFrame(bigram_count_list, index=sen_words_set, columns=sen_words_set)
    bigram_smoothing_df = pd.DataFrame(bigram_count_list + 1, index=sen_words_set, columns=sen_words_set)
    return bigram_df, bigram_smoothing_df, bigram_count_list


# Function to create bigram probability table
def bigram_prob_table(vocab_dict, vocab, sen_words_set, bigram_count_list):
    bigram_prob = []
    bigram_smoothing = bigram_count_list + 1
    bigram_smoothing_prob = []
    for i in range(0, len(sen_words_set)):
        bigram_prob.append(bigram_count_list[i] / vocab_dict.get(sen_words_set[i]))
        bigram_smoothing_prob.append(bigram_smoothing[i] / (vocab_dict.get(sen_words_set[i]) + len(vocab)))
    bigram_prob_df = pd.DataFrame(bigram_prob, index=sen_words_set, columns=sen_words_set)
    bigram_smoothing_prob_df = pd.DataFrame(bigram_smoothing_prob, index=sen_words_set, columns=sen_words_set)
    return bigram_prob_df, bigram_smoothing_prob_df


# Function to calculate sentence probability
def calSentenceProb(sentence, vocab, bigram_prob_df, bigram_smoothing_prob_df):
    result_prob = []
    words = extract_words(sentence)
    # print(words)
    bigram_prob = bigram_smoothing_prob = 1 / len(vocab)
    for i in range(0, len(words) - 1):
        bigram_prob = bigram_prob * bigram_prob_df[words[i + 1]][words[i]].round(2)
        bigram_smoothing_prob = bigram_smoothing_prob * bigram_smoothing_prob_df[words[i + 1]][words[i]]
    result_prob.append(bigram_prob)
    result_prob.append(bigram_smoothing_prob)
    return bigram_prob, bigram_smoothing_prob, result_prob


# Function to write to a CSV file
def write_to_csv(bigram_df, bigram_smoothing_df, bigram_prob_df, bigram_smoothing_prob_df,
                result_prob, sentence):

    try:
        with open(r'output.csv', "a") as f:
            filewriter = csv.writer(f, delimiter=',')
            filewriter.writerows([["Bigram Table" + "--" + str(sentence)]])
            bigram_df.to_csv(f, encoding='utf-8')
            filewriter.writerows([" "])
            filewriter.writerows([["Bigram Smoothing Table" + "--" + str(sentence)]])
            bigram_smoothing_df.to_csv(f, encoding='utf-8')
            filewriter.writerows([" "])
            filewriter.writerows([["Bigram Probability Table" + "--" + str(sentence)]])
            bigram_prob_df.to_csv(f, encoding='utf-8')
            filewriter.writerows([" "])
            filewriter.writerows([["Bigram Smoothing Probability Table" + "--" + str(sentence)]])
            bigram_smoothing_prob_df.to_csv(f, encoding='utf-8')
            filewriter.writerows([" "])
            filewriter.writerows([[sentence + "probability"]])
            rows = [["Bigram Probabilty", "Bigram Smoothing Probabilty"]]
            rows.append(result_prob)
            filewriter.writerows(rows)
        f.close()
    except:
        print("File not found")


# Driver function
def main():
    # corpus = r"C:\Users\lbhar\OneDrive\spring 2019\NLP\Corpus.txt"
    # S1 = "The chairman made the decision to bring in a new financial planner"
    # S2 = "The profit of the company was going down last year said by the chief executive"
    corpus = str(sys.argv[1])
    S1 = str(sys.argv[2])
    S2 = str(sys.argv[3])
    input_sen = [S1, S2]
    for sentence in input_sen:
        vocab_dict, vocab = countVocab(corpus)
        bigram_count, sen_words_set, sen_words = bigramCountsForStatement(sentence, corpus)
        # print(sen_words_set)
        bigram_df, bigram_smoothing_df, bigram_count_list = bigram_table(bigram_count, sen_words_set)
        bigram_prob_df, bigram_smoothing_prob_df = bigram_prob_table(vocab_dict, vocab, sen_words_set,
                                                                     bigram_count_list)
        bigram_sen_prob, bigram_smoothing_sen_prob, result_prob = calSentenceProb(sentence, vocab, bigram_prob_df,
                                                                                  bigram_smoothing_prob_df)
        write_to_csv(bigram_df, bigram_smoothing_df, bigram_prob_df, bigram_smoothing_prob_df,
                    result_prob, sentence)
        # print(bigram_sen_prob, bigram_smoothing_sen_prob)


if __name__ == '__main__':
    main()
