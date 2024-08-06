# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 11:19:45 2024

@author: 90545
"""

# my_similarity_package/similarity.py

import pandas as pd
import string
import numpy as np

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

def preprocess_sentence(sentence):
    
    # Cümleyi küçük harfe çevir ve noktalama işaretlerini kaldır
    sentence = sentence.lower().translate(str.maketrans("", "", string.punctuation))
    words = sentence.split()
    return words

def create_count_matrix(sentences):
    
    # Tüm kelimeleri birleştirip benzersiz kelimeleri bulun
    all_words = []
    for sentence in sentences:
        words = preprocess_sentence(sentence)
        all_words.extend(words)
    
    unique_words = list(set(all_words))
    # ps = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    #unique_words = [ps.stem(word) for word in unique_words]
    unique_words = [lemmatizer.lemmatize(word) for word in unique_words]
    unique_words = sorted(set(unique_words))
    
    # Boş matris oluştur (satırlar cümleler, sütunlar benzersiz kelimeler)
    count_matrix = pd.DataFrame(0, index=['cumle1', 'cumle2'], columns=unique_words)
    
    for i, sentence in enumerate(sentences):
        words = preprocess_sentence(sentence)
        for word in words:
            count_matrix.iloc[i][word] = words.count(word)
    
    return count_matrix

# # Cümleler
# cumle1 = "A new World Bank report holds out similar fears. At the current growth rate, India will need 75 years to reach a quarter of America's per capita income, World Development Report 2024 says. It also says more than 100 countries – including India, China, Brazil and South Africa - face “serious obstacles” that could hinder their efforts to become high-income countries in the next few decades."
# cumle2 = "In India, Mexico, and Peru, firms that operate for 40 years typically double in size, while in the US, they grow seven-fold in the same period. This indicates that firms in middle-income countries struggle to grow significantly, but still survive for decades. Consequently, nearly 90% of firms in India, Peru, and Mexico have fewer than five employees, with only a small fraction having 10 or more, the report says."
# # Cümleleri liste halinde sakla
# sentences = [cumle1, cumle2]

# # Kelime sayım matrisini oluştur
# count_matrix = create_count_matrix(sentences)
def CosineSimilarity(cumle1,cumle2):
    
    sentences = [cumle1, cumle2]
    df = create_count_matrix(sentences)
    vec1 = df.iloc[0].values
    vec2 = df.iloc[1].values
    
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    
    cosine_similarity = dot_product / (norm_vec1*norm_vec2)
        
    return cosine_similarity

# x = CosineSimilarity(count_matrix)
