"""Retrieves vocabulary words from the SAT Question of the Day (QOTD)
   and writes them to the vocab_words file. The BeautifulSoup library
   makes it easier to parse the html from the CollegeBoard's web page."""

from os import path
import sys

from datetime import datetime
import urllib2
import re
from bs4 import BeautifulSoup

DEFAULT_URL = 'http://sat.collegeboard.org/practice/sat-question-of-the-day'
CATEGORY_WITH_VOCAB = 'Sentence Completions'

BASE_PATH = path.dirname(path.abspath(__file__))
VOCAB_FILE = path.join(BASE_PATH, 'vocab_words')
COMMON_WORDS_FILE = path.join(BASE_PATH, 'common_words')


def main():
    """Gets vocab words from the QOTD page (if present) and
       writes them to the vocab_words file."""
    soup = get_soup()

    category = get_category(soup)
    if not category == CATEGORY_WITH_VOCAB:
        message = """%s %s: Unable to retrieve vocabulary
                    words from category \'%s\'"""
        print message % (datetime.now().strftime('%D %r'),
                         sys.argv[0], category)
        sys.exit()

    vocab_words = get_vocab_words(soup)
    write_to_file(vocab_words)
    print '\n'.join(vocab_words)


def get_soup():
    """Return BeautifulSoup version of QOTD html"""
    try:
        sat_question_page = urllib2.urlopen(sys.argv[1])
    except IndexError:
        sat_question_page = urllib2.urlopen(DEFAULT_URL)

    return BeautifulSoup(sat_question_page)


def get_category(soup):
    """Return category of QOTD"""
    question_form = soup.find(id='questionOfTheDay')
    unparsed_category = question_form.previousSibling.previousSibling
    category = unparsed_category.contents[0].split('>')[1].strip()
    return category


def get_vocab_words(soup):
    """Return list of vocabulary words from QOTD"""
    choices = soup.findAll(attrs={'for': re.compile('^qotdChoices[ABCDE]$')})
    unparsed_choices = [choice.contents[0] for choice in choices]

    rm_letter = re.compile('^\([ABCDE]\)')
    rm_dots = re.compile(' . .')

    # Remove letter choice [(A), (B), etc] from each unparsed choice.
    unparsed_choices = [rm_letter.sub('', choice)
                        for choice in unparsed_choices]

    # Remove the dots ( . .) from each choice. Only applicable if each
    # choice has more than one word. As a result, parsed_words will become
    # a list of lists (which must be combined).
    parsed_words = [rm_dots.sub('', choice).split()
                    for choice in unparsed_choices]

    # Combine all sublists into one long list.
    parsed_words = [word for sublist in parsed_words for word in sublist]

    return parsed_words


def write_to_file(vocab_words):
    """Append 'uncommon' newly found words to file"""
    common_words = get_common_words()

    vocab_file = open(VOCAB_FILE, 'a+')
    for word in vocab_words:
        if word not in common_words:
            vocab_file.write(word + '\n')

    vocab_file.close()


def get_common_words():
    """Retrieve list of common words from file"""
    common_words_file = open(COMMON_WORDS_FILE, 'r')
    common_words = [line.strip('\n') for line in common_words_file]
    common_words_file.close()
    return common_words

if __name__ == '__main__':
    main()
