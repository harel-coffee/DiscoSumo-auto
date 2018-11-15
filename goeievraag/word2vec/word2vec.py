__author__='thiagocastroferreira'

import logging
FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT)

import json
import spacy

from gensim.models import Word2Vec

QUESTIONS='/roaming/fkunnema/goeievraag/parsed/question_parsed.json'

ANSWERS='/roaming/fkunnema/goeievraag/parsed/answer_parsed.json'


def run():
    nlp = spacy.load('nl', disable=['tagger', 'parser', 'ner'])
    documents = []

    questions = json.load(open(QUESTIONS))
    for question in questions:
        text = question['questiontext'] + ' '
        text += question['description']

        text = list(map(lambda token: str(token).lower(), nlp(text)))
        documents.append(text)

    answers = json.load(open(ANSWERS))
    for answer in answers:
        text = answer['answertext']
        text = list(map(lambda token: str(token).lower(), nlp(text)))
        documents.append(text)

    logging.info('Training...')
    fname = 'word2vec.model'
    model = Word2Vec(documents, size=300, window=50, min_count=1, workers=10)
    model.save(fname)

if __name__ == '__main__':
    logging.info('Loading corpus...')
    run()