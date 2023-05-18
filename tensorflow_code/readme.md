Some of the notes I have made while learning how to use tensorflow basics:
This note includes basic codes and describes what each one of them does
(COPY AND PASTED FROM A texteditor - will not be organized when uploaded to gogs)

Headers:
import tensorflow as tf                 - imports tensorflow in python
from tensorflow import keras                        - imports keras from tensorflow
from tensorflow.keras import layers              - imports layers from keras.

# Helper libraries
import numpy as np                                 - for numpy arrays
import matplotlib.pyplot as plt                  - for histograms and 2d drawings

-----------------------------dataset---------------------------------------------------------------------------
Numpy = arrays (must use this unlike c)
Load dataset (ex: MNIST = 70000 image of 28 by 28 pixel)
mnist = tf.keras.datasets.mnist                                -  allowing access
(x_train, y_train), (x_test, y_test) = mnist.load_data()     - loading dataset
preparing dataset (ex: converting integers to floating point number)
x_train, x_test = x_train / 255.0, x_test / 255.0 – every pixel to values smaller than or equal to 1
x_train = independent variable to train the model
x_test = remaining independent variable that will be used for testing 
y_train = dependent variable which needs to be predicted
y_test = dependent variable that will be used to test the accuracy between actual and predicted
if we put
x_train.shape – output will be : (60000, 28, 28) – 28 by 28 of 60000 number of images
len(train_x) – 60000 as it shows how many number of inputs

train_x – to see what is inside the input (note this is not the pixels inside the image but rather the classification of the dataset (of each image))

------------------------------------ show data (matplotlib) ---------------------------------------------------------------
plt.figure()                     - opens a figure box
plt.imshow(train_images[0])      - shows the train_image[0] image
plt.colorbar()                   - place colorbar
plt.grid(False)                  - no grid on the data
plt.show()                       - show the plot.


This code shows you first 25 images of the datset
plt.figure(figsize=(10,10))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_images[i], cmap=plt.cm.binary)
    plt.xlabel(class_names[train_labels[i]])
plt.show()

There are two ways to build neural network:
Sequential API – layer by layer, 1input 1 output, no sharing of layers
Functional API – sharing of layers, multiple input and output

Lets Build the tf.keras.Sequential model by stacking layers:
model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)), - layer 1
  tf.keras.layers.Dense(128, activation='relu'), - layer 2
  tf.keras.layers.Dropout(0.2), - layer 3
  tf.keras.layers.Dense(10) – layer 4 (must have 10 as we are trying to identify distinguish 0~9 digits!!!)
])

Flatten – gets all the tensors of (28,28) and putting it in one array (0~23) (1d array)
If it was a color image it would be 28 * 28 * 3 because 3 values per pixel
Dense – creates a fully/densely connected layer. 128 nodes in the layer.
Activation function used = “relu” – gets input and spits out a value called logit!
Relu – 0 for negative, leaves any positive logit unchanged.
Softmax – don’t use this as a layer as it is impossible to have stable loss calculation
Dropout – dense has some drawbacks : too much data(overfitting)
Dropout make sure that some of the nides in the a layer do not pass on their information to the next layer – helps with computation time + overfitting.
Dropout probability of 0.2 means that the each node in the first dense has a 0.2 probability of being dropped from the computation for the next layer – making a sparsely connected layer. 
Note that you can remove the latest added layer with :
model.pop()
it is also possible to add names for each layers:
model.add(layers.Dense(2, activation="relu", name="layer1"))

--------------------------------compiling training running neural net------------------------------------
model.compile(optimizer='adam',
loss='sparse_categorical_crossentropy',
metrics=['accuracy'])
To successfully compile in Tensorflow, one must provide a loss function, optimizer and metrics.
Loss function
Quantifies how far off a prediction is from the ground truth.
Sparse_categorial_crossentropy is useful for multiclass classification
Optimizer
Training a model also means minimizing the loss!
Higher loss – more incorrect prediction
Backpropagation – revising mathematics parameters of the nodes of a network based on how effective those parameters were in doing its job
Optimizer parameter specifies a way of making the backpropagation process more faster and effective – adam works fine for this problem.
Metrics
Specifies the metrics it should use in evaluating the model
Training the model:
model.fit(x_train, y_train, epochs=5)
pass the x y training data.
Epochs parameter is the number of times the model sees all of the training data. (one might not be enough for the model to sufficiently update and mark improvements.
Evaluating the model:
model.evaluate(x_test, y_test)
Shows how the model performed with actual test data and compares it to training data.
Verbose is not important
-----------------------------------------make predictions---------------------------------------------------
Predictions – will use softmax which is useful as it changes the output logits into probabilities.
probability_model = tf.keras.Sequential([model, 
                                         tf.keras.layers.Softmax()])

predictions = probability_model.predict(test_images) – test_images is x_test

After this lines of codes
predictions[0]  - will show you the model’s confidence that the image corresponds to the each of the 10 different articles of clothing.
np.argmax(predictions[0]) – to see t he highest confidence value
Example output would be 9