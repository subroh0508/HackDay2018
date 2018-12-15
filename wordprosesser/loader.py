import pickle


def load(pickle_file="../irasutoya_contents.pickle"):
    with open(pickle_file, 'rb') as f:
        result = pickle.load(f)

    print(len(result))


def pickle_to_corpus(src, dst):
    with open(src, 'rb') as f:
        result = pickle.load(f)

    titles = list(map(lambda d: d["name"], result))

    with open(dst, mode='w') as f:
        f.write('\n'.join(titles))


def main():
    pickle_to_corpus("../irasutoya_contents.pickle", "../res/corpus.txt")


if __name__ == "__main__":
    main()
