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

### Step 4. Run More Test
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

Run the example came with Google 

```
# run Google original test
python mnist_client.py --num_tests=1000 --server=localhost:9000
```



# run the slightly modified test file to 
python test_mnist --server=localhost:9000

### Step 6. Test HTTP Bridge with Nodejs
Tensorflow Serving uses gRPC as protocol so it is a little difficult to call from a web browser

