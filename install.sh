export SLIM=/home/ubuntu/src/serving_tensorflow_p27/tf_models/research/slim
chmod +x get-predict
chmod +x predict
chmod +x site/start-server 
chmod +x site/run-predict
chmod +x site/run-mnist-predict
cp -f get-predict $SLIM/.
cp -f predict $SLIM/.
cp -f *.py $SLIM/.
cp -f mnist-predict-client.py /home/ubuntu/tutorials/TensorFlow/serving/.
npm install express-fileupload
npm install node-uuid

