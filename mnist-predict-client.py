#!/usr/bin/env python2.7

from __future__ import print_function

import sys
import threading
from PIL import Image
from grpc.beta import implementations
import numpy
import tensorflow as tf

from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2

tf.app.flags.DEFINE_string('server', '', 'PredictionService host:port')
FLAGS = tf.app.flags.FLAGS

class _ResultWaiter(object):

  def __init__(self):
    self._done = False
    self._condition = threading.Condition()

  def mark_done(self):
    with self._condition:
      self._done = True
      self._condition.notify()

  def wait_done(self):
    with self._condition:
      while not self._done:
        self._condition.wait()


def _create_rpc_callback(label, result_waiter):
  def _callback(result_future):
    exception = result_future.exception()
    if exception:
      print(exception)
    else:
      response = numpy.array(result_future.result().outputs['scores'].float_val)
      prediction = numpy.argmax(response)
      print("The predicted result is digit: {0}".format(prediction))
      result_waiter.mark_done()
  return _callback


def do_predict(hostport, image, label):
  host, port = hostport.split(':')
  channel = implementations.insecure_channel(host, int(port))
  stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)
  result_waiter = _ResultWaiter()
  request = predict_pb2.PredictRequest()
  request.model_spec.name = 'mnist'
  request.model_spec.signature_name = 'predict_images'
  request.inputs['images'].CopyFrom(tf.contrib.util.make_tensor_proto(image, shape=[1, len(image)]))
  result_future = stub.Predict.future(request, 5.0)  # 5 seconds
  result_future.add_done_callback(_create_rpc_callback(label, result_waiter))
  #print('done with calling predict ' + label + ', waiting for result...')
  return result_waiter.wait_done()
  
def main(_):
    im = Image.open(sys.argv[1]).convert('L')
    width = float(im.size[0])
    height = float(im.size[1])
    newImage = Image.new('L', (28, 28), (255)) #creates white canvas of 28x28 pixels
    if width > height:
        nheight = int(round((20.0/width*height),0))
        if (nheight == 0):
            nheight = 1
        img = im.resize((20,nheight), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wtop = int(round(((28 - nheight)/2),0))
        newImage.paste(img, (4, wtop))
    else:
        nwidth = int(round((20.0/height*width),0))
        if (nwidth == 0):
            nwidth = 1
        img = im.resize((nwidth,20), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wleft = int(round(((28 - nwidth)/2),0))
        newImage.paste(img, (wleft, 4))

    tv = list(newImage.getdata()) #get pixel values
    normvals = [ (255-x)*1.0/255.0 for x in tv] 
    do_predict(FLAGS.server, normvals, sys.argv[1])


if __name__ == '__main__':
  tf.app.run()

