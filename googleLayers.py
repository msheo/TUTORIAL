# Copyright 2015 Google Inc. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Utility functions for adding layers to a Model.
NB: This is used by PrettyTensor, but it will be deprecated.  Please do not use!
"""
import math

import tensorflow as tf

# Implementation note: this takes a tuple for an activation instead of
# encouraging lambdas so that we can inspect the actual function and add
# appropriate summaries.

def add_l2loss(books, params, l2loss, name='weight_decay'):
  if l2loss:
    books.add_loss(
        tf.multiply(tf.nn.l2_loss(params), l2loss, name=name),
        regularization=True)


def xavier_init(n_inputs, n_outputs, uniform=True):
  """Set the parameter initialization using the method described.
  This method is designed to keep the scale of the gradients roughly the same
  in all layers.
  Xavier Glorot and Yoshua Bengio (2010):
           Understanding the difficulty of training deep feedforward neural
           networks. International conference on artificial intelligence and
           statistics.
  Args:
    n_inputs: The number of input nodes into each output.
    n_outputs: The number of output nodes for each input.
    uniform: If true use a uniform distribution, otherwise use a normal.
  Returns:
    An initializer.
  """
  if uniform:
    # 6 was used in the paper.
    init_range = math.sqrt(6.0 / (n_inputs + n_outputs))
    return tf.random_uniform_initializer(-init_range, init_range)
  else:
    # 3 gives us approximately the same limits as above since this repicks
    # values greater than 2 standard deviations from the mean.
    stddev = math.sqrt(3.0 / (n_inputs + n_outputs))
    return tf.truncated_normal_initializer(stddev=stddev)


def spatial_slice_zeros(x):
  """Experimental summary that shows how many planes are unused for a batch."""
  return tf.cast(tf.reduce_all(tf.less_equal(x, 0.0), [0, 1, 2]),
                 tf.float32)