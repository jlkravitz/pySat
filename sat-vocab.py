#!/usr/bin/env python

from os import path
import sys

import urllib2
import re
from bs4 import BeautifulSoup

DEFAULT_URL = 'http://sat.collegeboard.org/practice/sat-question-of-the-day'
CATEGORY_WITH_VOCAB = 'Sentence Completions'
VOCAB_FILE = path.abspath('vocab_words')
COMMON_WORDS_FILE = path.abspath('common_words')

def main():
    soup = getSoup()

    category = getCategory(soup)
    if not category == CATEGORY_WITH_VOCAB: 
        print '%s: Unable to retrieve vocabulary words from category \"%s\"' % (sys.argv[0], category)
        sys.exit()

    vocabWords = getVocabWords(soup)

    writeToFile(vocabWords)
    
    print '\n'.join(vocabWords)
    

def getSoup():
    """Return BeautifulSoup version of QOTD html"""
    try:
        satQuestionPage = urllib2.urlopen(sys.argv[1])
    except IndexError:
        satQuestionPage = urllib2.urlopen(DEFAULT_URL)

    return BeautifulSoup(satQuestionPage)


def getCategory(soup):
    """Return category of QOTD"""
    questionForm = soup.find(id='questionOfTheDay')
    unparsedCategory = questionForm.previousSibling.previousSibling
    category = unparsedCategory.contents[0].split('>')[1].strip()
    return category

def getVocabWords(soup):
    """Return list of vocabulary words from QOTD"""
    choices = soup.findAll(attrs={'for': re.compile('^qotdChoices[ABCDE]$')})
    unparsedChoiceStrings = [choice.contents[0] for choice in choices]
    
    rmLetter = re.compile('^\([ABCDE]\)')
    rmDots = re.compile(' . .') 

    # Remove letter choice and dots (if > 1 word per choice) from choice. parsedWords is a list of lists
    # and the sublists will contain the number of words per choice (1 or 2).
    parsedWords = [rmDots.sub('', rmLetter.sub('', choice)).split() for choice in unparsedChoiceStrings]

    # combine all sublists of words into one long list
    parsedWords = [word for sublist in parsedWords for word in sublist]
   
    return parsedWords

def writeToFile(vocabWords):
    """Append 'uncommon' newly found words to file"""
    commonWords = getCommonWords()

    vocabFile = open(VOCAB_FILE, 'a+')
    for word in vocabWords:
        if word not in commonWords:
            vocabFile.write(word + '\n')

    vocabFile.close()

def getCommonWords():
    """Retrieve list of common words from file"""
    commonWordsFile = open(COMMON_WORDS_FILE, 'r')
    commonWords = [line.strip('\n') for line in commonWordsFile]
    commonWordsFile.close()
    return commonWords

if __name__ == '__main__':
    main()
