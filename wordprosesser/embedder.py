from gensim.models import word2vec
from gensim.models import KeyedVectors
import logging
import numpy as np

logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)


def train_model(corpus_src, dst, window=3, dimension=256):
    model = word2vec.Word2Vec(window=window, size=dimension, min_count=1)
    sentences = word2vec.LineSentence(corpus_src)
    model.build_vocab(sentences)
    model.train(sentences, total_examples=model.corpus_total_words, epochs=10)
    model.save(dst)


def get_model(model_src):
    model = word2vec.Word2Vec.load(model_src)
    print('Loaded', model_src)

    return model


def load_model(src):
    model = KeyedVectors.load_word2vec_format(src, binary=True)

    return model


def main():
    model = load_model("../model/entity_vector.model.bin")
    print(model["浄水器"])


if __name__ == "__main__":
    main()
