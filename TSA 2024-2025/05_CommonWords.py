"""
  Write a program in which you will accept two sentences from a user and then return the following: a list of words found in bothsentences and the number of times those words occur, a list of unique words not found in both sentences, and then the number of vowels in each sentence. Your program should follow the following steps:
  1. Ask the user for their first sentence
  2. Ask the user for their sencond sentence
  3. Calculate the followoing:
    - List of words found in both sentences and their frequency
    - List of words not found in both sentences
    - The number of vowels in both sentences
  4. Display the results in the following structure:
    - Words in both sentences: {word1} - {countWord1}, {word2} - {countWord2}
    - Unique Words: {word1}, {word2}, {word3}
    - Number of vowel: {numOfVowels}
"""
import re
from collections import Counter
sentence1 = input("Enter the first sentence: ")
sentence2 = input("Enter the second sentence: ")
# Convert sentences to lowercase and remove punctuation
sentence1 = re.sub(r'[^\w\s]', '', sentence1.lower())
sentence2 = re.sub(r'[^\w\s]', '', sentence2.lower())
# Split sentences into words
words1 = sentence1.split()