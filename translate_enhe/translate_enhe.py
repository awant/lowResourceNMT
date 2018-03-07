import re
import os

from tensor2tensor.data_generators import problem, text_encoder
from tensor2tensor.data_generators import translate, text_problems
from tensor2tensor.layers import common_hparams
from tensor2tensor.utils import registry
from tensor2tensor.models.transformer import transformer_base
import tensorflow as tf


@registry.register_hparams
def transformer_enhe():
    hparams = transformer_base()
    hparams.num_hidden_layers = 2
    hparams.hidden_size = 128
    hparams.filter_size = 512
    hparams.num_heads = 4
    return hparams


@registry.register_problem
class TranslateHeToEn(translate.TranslateProblem):

    @property
    def approx_vocab_size(self):
        return 8*1024

    @property
    def vocab_type(self):
        return text_problems.VocabType.SUBWORD # CHARACTER, TOKEN - custom user vocab

    @property
    def is_generate_per_split(self):
    # Because we have train/dev/test subsets
        return True

    def generate_samples(self, data_dir, tmp_dir, dataset_split):
        is_train_dataset = dataset_split == problem.DatasetSplit.TRAIN
        dataset_label = 'train' if is_train_dataset else 'dev'
        ext = '.txt'
        he_path = os.path.join(data_dir, 'he.'+dataset_label+ext)
        en_path = os.path.join(data_dir, 'en.'+dataset_label+ext)

        return text_problems.text2text_txt_iterator(he_path, en_path)
