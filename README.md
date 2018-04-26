# TensorFlow Environment & TensorFlow Serving
Please refer to [Simple MxNet Server Lab](https://github.com/changli3/ml-mxnet) for starting an AWS Deep Learning instance.

### Step 1. Lauch AWS VM
I have an AWS CF template file [cf.json](https://github.com/changli3/ml-mxnet/blob/master/cf.json) here. You can launch it in the AWS console, or use AWS CLI like below. Remember to download the tempalte file to your computer and change parameters to proper values -
```
aws cloudformation deploy --template-file cf.json --stack-name test-ml --parameter-overrides InstanceSubnet=subnet-2b976000 InstanceSecurityGroup=sg-58e1fc3d KeyPairName=TreaEBSLab
```

### Step 2. SSH to the VM
Once the CF template completed, SSH to it with username "ubuntu" and the key used to launch the template.

### Step 3. Test TensorFlow Environment
For starters, you can clone Udacity's Deep Learning site and go through it with JupyterLab (see [ML Notebooks](https://github.com/changli3/ml-notebooks) for reference).

Run the following command -
```
cd ~
git clone https://github.com/udacity/deep-learning.git
```
And then start JupyterLab and brwose to the lessons. Note that you have select environment to be "conda_tensorflow_p27" 

### Step 4. Run More Tests with Pre-trained Models
Run the following commands to setup the environment
```
git clone https://github.com/changli3/tensorflow.git
cd tensorflow
bash install.sh
```

Now we are ready to run some test on pre-trained data.
```
# use slim
source activate tensorflow_p27
cd /home/ubuntu/src/serving_tensorflow_p27/tf_models/research/slim

# fetch pretrained check point
python get-pretrained-data.py

# check downloaded chkp files
ls /tmp/checkpoints

# open browser to find an images file (e.g. http://wolfweb.com/wp-content/uploads/2012/11/wolfpck2.jpg)
URL=http://wolfweb.com/wp-content/uploads/2012/11/wolfpck2.jpg

# test vgg model
./get-predict vgg $URL

# test inception_v1 model
./get-predict inception_v1 $URL

# test both
./get-predict both $URL
```

### Step 5. Test Serving Tensorflow with Saved Model
To make a TensorFlow model serverable (as a predict service) via the TensorFlow Serving architect, the key task is to write the saved model function with TensorFlow's SavedModelBuilder module.

```
# set environment
source activate tensorflow_p27
cd /home/ubuntu/tutorials/TensorFlow/serving

# Save model 
python mnist_saved_model.py /tmp/mnist_model

# check the saved model
ls /tmp/mnist_model/1
```

The file /tmp/mnist_model/1/saved_model.pb is a binary file. To make it a text/json format:

```
sed 's/builder.save()/builder.save(as_text=True)/' mnist_saved_model.py > mnist_saved_model2.py
python mnist_saved_model2.py /tmp/mnist_model2

# check the saved model, you can see the pbtxt file
ls /tmp/mnist_model2/1
```

The saved model not only exports the model snapshot, it defines the serving signature (input/output variables) as well. You can use _saved_model_cli_ to exam the model:

```
saved_model_cli show --all --dir /tmp/mnist_model/1
```

You can there are two methods defined "predict" and "classify" and predict method takes a 28x28 grayscale image as input, and so on.
![model info](https://raw.githubusercontent.com/changli3/tensorflow/master/model_info.JPG "model info")

To start TensorFlow serving with the model -
```
# Start the service
tensorflow_model_server --port=9000 --model_name=mnist --model_base_path=/tmp/mnist_model
```


### Step 5. Use Serving Tensorflow

Now try to use the service with client call. Open another termminal and login as ubuntu. Then -

```
source activate tensorflow_p27
cd /home/ubuntu/tutorials/TensorFlow/serving
```

Run the example came with Google -

```
# run Google original test
python mnist_client.py --num_tests=1000 --server=localhost:9000
```

Since Tensorflow Serving uses gRPC as protocol so it is quite difficult to figure out how to use it. Look at the _mnist-predict-client.py_ you can have a feeling of tasks you need to do in order to use the service:

* You need to understand the model methods well and know how to prepare the inputs. In this case form mnist model, need to translate the input image to a 28x28 greyscale array and normalize the value from [0..255] to [0..1].
* You need to understand that since the call is async, you have to wait for the results to come back, implemented here "_ResultWaiter" class.
* Need to implement the call back function and singnal between waiter and callback.

```
# run the client to predict one image file - I have them as: _digit-X.JPG_
python mnist-predict-client.py digit-2.jpg --server=localhost:9000 
```

### Step 6. Do HTTP Bridge with Nodejs

A lot people are too familiar with the normal "browser-enabled" APIs, so they rather want to use a web server to bridge the grpc calls. There are standard ways, and there are projects that can direct host TensorFlow as both grpc and http services. Here I just put together a nodejs web server and do some samll tests.

Open another terminal, do -

```
cd /home/ubuntu/tensorflow/site
./start-server
```

To test use the pre-trained vgg and inception_v1 model, in the old terminal, do -
```
cd ~/tensorflow

# call the web service with the image file wolfpck2.jpg. Optionally, you can download other images
curl -XPOST http://localhost:9999/predict -F "file=@wolfpck2.jpg"
```

Make sure your Tensorflow Serving is still running on port 9000, now test it with -

```
# digit number 2
curl -XPOST http://localhost:9999/mnist-predict  -F "file=@digit-2.JPG"


# digit number 9
curl -XPOST http://localhost:9999/mnist-predict  -F "file=@digit-9.JPG"
```



### Pictures Used

* Digit 2
![digit 2](https://raw.githubusercontent.com/changli3/tensorflow/master/digit-2.JPG "digit 2")

* Digit 9
![digit 9](https://raw.githubusercontent.com/changli3/tensorflow/master/digit-9.JPG "digit 9")

* Wolves
![wolfpck2](https://raw.githubusercontent.com/changli3/tensorflow/master/wolfpck2.jpg "wolfpck2")
