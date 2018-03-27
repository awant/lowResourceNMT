import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import collections

from tensor2tensor import models
from tensor2tensor import problems
from tensor2tensor.layers import common_layers
from tensor2tensor.utils import trainer_lib
from tensor2tensor.utils import t2t_model
from tensor2tensor.utils import registry
from tensor2tensor.utils import metrics

from tensorflow.contrib.eager.python import tfe
tfe.enable_eager_execution()

Modes = tf.estimator.ModeKeys

main_dir = '/Volumes/Elements/LowResourceNMT/models/t2t'
data_dir = os.path.join(main_dir, 'data')
tmp_dir = os.path.join(main_dir, 'tmp')
train_dir = os.path.join(main_dir, 'train')
checkpoint_dir = os.path.join(main_dir, 'checkpoints')


ende_problem = problems.problem("translate_ende_wmt32k")
# print('ende_problem', ende_problem)
# print('vocab type', ende_problem.vocab_type)
# sys.exit(-1)

# simple encoder, for example: SubwordTextEncoder. Just mapping from str to idxs in vocab file
encoders = ende_problem.feature_encoders(data_dir)

def encode(input_str, output_str=None):
  inputs = encoders["inputs"].encode(input_str) + [1]
  batch_inputs = tf.reshape(inputs, [1, -1, 1])
  return {"inputs": batch_inputs}

def decode(integers):
  integers = list(np.squeeze(integers))
  if 1 in integers:
    integers = integers[:integers.index(1)]
  return encoders["inputs"].decode(np.squeeze(integers))


model_name = "transformer"
hparams_set = "transformer_base"
hparams = trainer_lib.create_hparams(hparams_set, data_dir=data_dir, problem_name="translate_ende_wmt32k")

translate_model = registry.model(model_name)(hparams, Modes.EVAL)
print('translate_model', translate_model)

ckpt_name = "transformer_ende_test"
ckpt_path = tf.train.latest_checkpoint(os.path.join(checkpoint_dir, ckpt_name))

def translate(inputs):
  encoded_inputs = encode(inputs)
  encoded_inputs['asd'] = tf.constant(0, name='asd')
  # print('encoded_inputs', encoded_inputs) # Tensorflow tensor: [[[29], [4341], [6545], [85], [62], ..., [1]]]
  with tfe.restore_variables_on_create(ckpt_path):
    model_output = translate_model.infer(encoded_inputs)["outputs"]
    # Internal:
    # models.Transformer(utils.t2t_model.T2TModel)
    # infer(...):
    #   self.prepare_features_for_infer(features)
    #   self._fill_problem_hparams_features(features)
    #   results = self._beam_decode(features, decode_length, beam_size, top_beams, alpha)

    # _fill_problem_hparams_features():
    #    for k, v in six.iteritems(problem_hparams_to_features(self._problem_hparams)):
    #     features[k] = tf.constant(v, name=k)
    # data_generators.problem.problem_hparams_to_features
  return decode(model_output)

inputs = "The animal didn't cross the street because it was too tired"
outputs = translate(inputs)

print("Inputs: %s" % inputs)
print("Outputs: %s" % outputs)
