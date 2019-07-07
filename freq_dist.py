#!/usr/bin/env python3
import os
import re

import click
import nltk
import pprint

DAYS = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday'
]


@click.command()
@click.argument("source_dir", type=click.Path(exists=True))
@click.argument("n_gram_size", type=click.INT)
@click.option('-n', '--number', type=click.INT, default=20,
              help='The number of results from the frequency distribution '
                   'to show')
def freq_dist(source_dir, n_gram_size, number):

    corpus = ''
    files = os.listdir(source_dir)

    for f in files:
        pathfile = source_dir + '/' + f
        if os.path.isdir(pathfile):
            continue
        pprint.pprint(f)
        with open(pathfile, 'r') as fh:
            src = fh.read()
        corpus += ' ' + src

    corpus = re.sub('\[x\]', '', corpus)
    for day in DAYS:
        corpus = re.sub(day, '', corpus)
    corpus = re.sub('[^A-Za-z\s]+', '', corpus)
    corpus = corpus.lower()

    tokens = nltk.word_tokenize(corpus)
    stop_words = nltk.corpus.stopwords.words('english')
    ps = nltk.stem.PorterStemmer()
    tokens = [ps.stem(t) for t in tokens if t not in stop_words and len(t) > 1]

    ngs = nltk.ngrams(tokens, n_gram_size)
    fdist = nltk.FreqDist(ngs)
    fdist.plot(number)


if __name__ == '__main__':
    freq_dist()
