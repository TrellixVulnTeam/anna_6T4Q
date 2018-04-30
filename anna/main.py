"""Main entry point for any experiments."""

import os
import sys
import anna.model.premade as models
import anna.data.dataset.fasttext as embeddings
import anna.data.dataset.reuters21578 as data


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: main.py DATA_FOLDER")
        exit(1)

    # Resolve data folder
    data_dir = os.path.abspath(sys.argv[1])

    # Fetch pre-trained word embeddings
    voc, emb = embeddings.fetch_and_parse(data_dir, voc_size=2000)

    # Fetch and preprocess dataset
    train_docs, test_docs, unused_docs, labels = data.fetch_and_parse(data_dir)

    # Create trainer for feedforward model
    model = models.AVGxBR(data_dir, labels, voc, emb)

    # Train model
    model.train(train_docs, test_docs)
