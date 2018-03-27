import re
import os

from tensor2tensor.data_generators import problem, text_encoder
from tensor2tensor.data_generators import translate, text_problems, translate_ende
from tensor2tensor.layers import common_hparams
from tensor2tensor.utils import registry, metrics
from tensor2tensor.models.transformer import transformer_base
import tensorflow as tf


@registry.register_problem
class TranslateEnToRu(translate_ende.TranslateEndeWmt32k):

    @property
    def is_generate_per_split(self):
    # Because we have train/dev/test subsets
        return True

    @property
    def vocab_filename(self):
        return "vocab.enru.%d" % self.approx_vocab_size

    def eval_metrics(self):
        return [metrics.Metrics.APPROX_BLEU, metrics.Metrics.NEG_LOG_PERPLEXITY]

    def generate_samples(self, data_dir, tmp_dir, dataset_split):
        is_train_dataset = dataset_split == problem.DatasetSplit.TRAIN
        dataset_label = 'train' if is_train_dataset else 'dev'
        ext = '.txt'
        ru_path = os.path.join(data_dir, 'ru.'+dataset_label+ext)
        en_path = os.path.join(data_dir, 'en.'+dataset_label+ext)

        return text_problems.text2text_txt_iterator(en_path, ru_path)
