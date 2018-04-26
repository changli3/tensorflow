export SLIM=/home/ubuntu/src/serving_tensorflow_p27/tf_models/research/slim
chmod +x get-predict
chmod +x predict
chmod +x site/start-server 
chmod +x site/run-predict
cp -f get-predict $SLIM/.
cp -f predict $SLIM/.
cp -f *.py $SLIM/.
cp -f test_mnist /home/ubuntu/tutorials/TensorFlow/serving/.
