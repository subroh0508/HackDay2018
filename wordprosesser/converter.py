import pickle
import MeCab
import sys, os
from wordprosesser.embedder import load_model


def load(pickle_file="../irasutoya_contents.pickle"):
    with open(pickle_file, 'rb') as f:
        result = pickle.load(f)

    print(len(result))


def pickle_to_text(src, dst):
    with open(src, 'rb') as f:
        result = pickle.load(f)

    lines = []
    for r in result:
        title_processed = separate(r["name"])
        url = r["url"]
        lines.append(title_processed + "," + url)

    with open(dst, mode='w') as f:
        f.write('\n'.join(lines))


def separate(text):
    mecab = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")
    mecab.parse('')

    stop_pos = ["助詞", "助動詞", "BOS/EOS"]
    stop_words = ["イラスト", "（", "）", "*"]

    node = mecab.parseToNode(text)

    word_filtered = []
    while node:
        word = node.feature.split(",")[6]
        pos = node.feature.split(",")[0]
        if not (pos in stop_pos or word in stop_words):
            word_filtered.append(word)
        node = node.next
    sentence_processed = " ".join(word_filtered)

    return sentence_processed


def dict_to_vector(src):
    with open(src) as f:
        lines = list(map(lambda l: l.strip(), f.readlines()))

    model = load_model("../model/entity_vector.model.bin")

    lines = lines[:100]
    outputs = []

    for line in lines:
        sentence, url = line.split(",")
        words = sentence.split()
        vectors = []
        for word in words:
            try:
                vector = model[word]
                vectors.append(vector)
            except KeyError:
                pass

        line_vectored = {"vectors": vectors, "url": url}
        outputs.append(line_vectored)

    with open('../res/irasutoya_vectors.pickle', 'wb') as f:
        pickle.dump(outputs, f)


def main():
    # pickle_to_text("../res/irasutoya_contents.pickle", "../res/irasutoya_dict.txt")
    dict_to_vector("../res/irasutoya_dict.txt")


if __name__ == "__main__":
    main()
