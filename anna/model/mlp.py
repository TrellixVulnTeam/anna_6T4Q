"""Multi layer perceptron using different binary classifiers for each label"""

import os
import tensorflow as tf
from model.trainer import Trainer
from model.encoder.naive import NaiveEmbeddingEncoder
from model.decoder.feedforward import FeedForwardDecoder


class MLP(Trainer):
    """
    Maps a Multi-label classification problem into binary classifiers,
    having one independent classifier for each label. All outputs share
    the core embedding layer.
    """

    def __init__(self,
                 data_dir,
                 labels,
                 name=None,
                 optimizer="adam",
                 metric="val_ebf1",
                 max_words=300,
                 num_layers=2,
                 hidden_size=1024,
                 voc_size=300000,
                 chain=False,
                 fixed_emb=False,
                 hinge=False,
                 save=False,
                 verbose=True):
        """
        Maps a Multi-label classification problem into binary classifiers,
        having one independent classifier for each label. All models share
        the core embedding layer.

        Args:
            data_dir (str): path to the folder where datasets are stored
            labels (list[str]): list of possible outputs
            name (str): name of the model (used when serializing to disk)
                        (default: combination of parameters)
            optimizer (str): one of: adam, rmsprop, momentum
                             (default: adam)
            metric (str): metric to optimize (e.g. val_loss, val_acc, etc.)
                          (default: val_ebf1)
            max_words (int): number of words to use when embedding text fields
                             (default: 300)
            num_layers (int): number of hidden layers in the MLP
                              (default: 2)
            hidden_size (int): size of the hidden units on each hidden layer
                               (default: 1024)
            voc_size (int): maximum size of the word vocabulary
                            (default: 300000)
            chain (bool): True if classifiers' output should be chained
                          (default: False)
            fixed_emb (bool): True if word embeddings shouldn't be trainable
                              (default: False)
            hinge (bool): True if loss should be hinge (i.e. maximum margin)
                          (default: False)
            save (bool): always save the best model (default: False)
            verbose (bool): print messages of progress (default: True)
        """
        # Encode doc as average of its initial `max_words` word embeddings
        encoder = NaiveEmbeddingEncoder(data_dir, max_words,
                                        fixed_emb, voc_size)

        # Classify labels with independent logistic regressions
        decoder = FeedForwardDecoder(data_dir, labels, num_layers,
                                     hidden_size, chain, hinge)

        # Generate name
        if not name:
            name = "mlp_{}_layers-{}_voc-{}_hidden-{}{}{}{}"
            name = name.format(optimizer, num_layers, voc_size, hidden_size,
                               "_hinge" if hinge else "",
                               "_chain" if chain else "",
                               "_fixed-emb" if fixed_emb else "")

        super().__init__(data_dir, labels, name, encoder, decoder, optimizer,
                         metric, save, verbose)
