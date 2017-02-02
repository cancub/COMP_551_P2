# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import nltk
import re, string

# get the training data
df = pd.read_csv('../csv_files/train_input.csv')

# get the common stopwords
sw = nltk.corpus.stopwords.words("english")

# stemmer is needed to boil down words to their roots
stemmer = nltk.stem.porter.PorterStemmer()

# words that we want to remove that are unlikely to show up in 
# stopwords but that we want to remove anyways
additional_words = ["</s>", "<number>", "</d>"]

# common website names
#websites = ["com","org","edu"]



#iterate through the list of posts
for index, row in df.iterrows():
        
    print index
    start_string = row['conversation']

    # get each of the words in the conversation
    conv_words = start_string.split(" ")
                
    conv_words_pruned = []
    
    # get rid of any noisy information
    for i in range(len(conv_words)):
        test_word = conv_words[i]

        # don't keep strings with speaker
        if "<speaker_" in test_word:
            continue
        
        # take out unnecesary additional words
        for ad_word in additional_words:
            if ad_word in test_word:
                #remove this substring
                test_word = test_word.replace(ad_word,"")
        
        # get rid of any leftover punctuation and whitespace
        test_word = test_word.strip('\t\r\n').translate(None, string.punctuation)
        
        # don't add empty strings or stop words
        if (not test_word) or (test_word in sw):
            continue
        
        conv_words_pruned.append(stemmer.stem(test_word))
        
    df.set_value(index,'conversation'," ".join(conv_words_pruned))
    
df.to_csv("../csv_files/train_input_processed.csv", index=False)
        
#    print conv_words_pruned