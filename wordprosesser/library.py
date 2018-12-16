import pickle
from wordprosesser.embedder import load_model
from wordprosesser.converter import separate
import numpy as np


class IrasutoyaLibrary:
    CACHE_DST = "./.cache"

    def __init__(self, src_pickle):
        self._data = IrasutoyaLibrary.load_vectors(src_pickle)
        self._model = load_model("../model/entity_vector.model.bin")
        self._cache = IrasutoyaLibrary.restore_cache()

    @staticmethod
    def load_vectors(src):
        with open(src, 'rb') as f:
            data = pickle.load(f)

        return data

    def translate_to_images(self, sentence):
        words = separate(sentence).split()
        print(words)
        urls = [self.get_closest_image_url(w) for w in words]
        urls = [url for url in urls if url]

        return urls

    def get_closest_image_url(self, word):
        try:
            cache = self._cache[word]
            print("Cached.")
            return cache
        except KeyError:
            pass

        try:
            self._model[word]
        except KeyError:
            return None

        max_ = -1.0
        closest_data = None
        for d in self._data:
            cos_sim = self.calc_max_cos_sim(d["vectors"], word)
            if max_ < cos_sim:
                closest_data = d
                max_ = cos_sim
                if max_ == 1.0:
                    break

        url = closest_data["url"]
        self._cache[word] = url
        if len(self._cache) % 30 == 0:
            self.store_cache()

        return url

    def store_cache(self):
        with open(IrasutoyaLibrary.CACHE_DST, 'wb') as f:
            pickle.dump(self._cache, f)
            print("Stored cache to", IrasutoyaLibrary.CACHE_DST, "(Size: {})".format(len(self._cache)))

    @staticmethod
    def restore_cache():
        try:
            with open(IrasutoyaLibrary.CACHE_DST, 'rb') as f:
                cache = pickle.load(f)
                print("Restored Cache.", "(Size: {})".format(len(cache)))
        except FileNotFoundError:
            cache = dict()
            print("There was no cache file.")

        return cache

    def calc_max_cos_sim(self, src_vectors, word):
        if len(src_vectors) == 0:
            return -1.0
        vector = np.asarray(self.get_vector(word))

        max_ = -1.0
        for sv in src_vectors:
            cos_sim = IrasutoyaLibrary.cos_sim(sv, vector)
            if max_ < cos_sim:
                max_ = cos_sim

        return max_

    def calc_sum_cos_sim(self, src_vectors, word):
        if len(src_vectors) == 0:
            return -1.0
        vector = np.asarray(self.get_vector(word))

        sum_ = 0.0
        for sv in src_vectors:
            sum_ += IrasutoyaLibrary.cos_sim(sv, vector)

        return sum_

    def calc_average_cos_sim(self, src_vectors, word):
        if len(src_vectors) == 0:
            return -1.0
        vector = np.asarray(self.get_vector(word))

        sum_ = 0.0
        for sv in src_vectors:
            sum_ += IrasutoyaLibrary.cos_sim(sv, vector)

        return sum_ / len(src_vectors)

    @staticmethod
    def cos_sim(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def get_vector(self, word):
        return self._model[word]

    def search(self, word):
        for d in self._data:
            if word in d["sentence"]:
                print(d)


def main():
    library = IrasutoyaLibrary("../res/irasutoya_vectors.pickle")
    urls = library.translate_to_images("もう辛い．仕事辞めたい帰りたい死にたい．もう辛い．仕事辞めたい帰りたい死にたい．")

    print("\n".join(urls))


if __name__ == "__main__":
    main()
