import pickle

def save_chunks(chunks, filename="vector_store.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(chunks, f)


def load_chunks(filename="vector_store.pkl"):
    with open(filename, "rb") as f:
        return pickle.load(f)