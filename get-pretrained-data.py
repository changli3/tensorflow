import tensorflow as tf
import os
from datasets import dataset_utils

url_inception_v1 = "http://download.tensorflow.org/models/inception_v1_2016_08_28.tar.gz"
url_vgg = "http://download.tensorflow.org/models/vgg_16_2016_08_28.tar.gz"
checkpoints_dir = '/tmp/checkpoints'

if not tf.gfile.Exists(checkpoints_dir):
   tf.gfile.MakeDirs(checkpoints_dir)

if not tf.gfile.Exists(os.path.join(checkpoints_dir, 'inception_v1.ckpt')):
   dataset_utils.download_and_uncompress_tarball(url_inception_v1, checkpoints_dir)
if not tf.gfile.Exists(os.path.join(checkpoints_dir, 'vgg_16.ckpt')):
   dataset_utils.download_and_uncompress_tarball(url_vgg, checkpoints_dir)
