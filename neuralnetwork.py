from numpy import loadtxt                                      # used to grab the data from csv files
from keras.models import Sequential                            # used for the model
from keras.layers import Dense                                 # used for the layers
import numpy as np                                             # used for arrays
from PIL import Image
import glob

# function prints out the custom photos and what the program predicted they were doing
def print_pred():
    count = 0
    for filename in glob.glob('custom/*.jpg'):                 # print out the predictions for our custom images
        print('Prediction for custom photo', count+1, 'is:', end='')
        if predictions[count] == 0:
           print(' No smile')
        else:
           print(' Smile')
        image = Image.open(filename)                           # opens and prints out each image
        image.show()
        input()                                                # waits for enter to be pressed
        count+=1

dataset_train = loadtxt('train.csv', delimiter=',')            # take the training from the csv file
dataset_test = loadtxt('test.csv', delimiter=',')              # take the test data
dataset_customdata = loadtxt('customdata.csv', delimiter=',')  # take the custom data

X_train = dataset_train[:, 1:]                                 # the training data
X_test = dataset_test[:, 1:]                                   # the test data
y_train = dataset_train[:, 0:1]                                # labels for the train data
y_test = dataset_test[:, 0:1]                                  # labels for the test data
X_custom = dataset_customdata[:, 1:]                           # the custom data
y_custom = dataset_customdata[:, 0:1]                          # labels for the custom data

model = Sequential()
model.add(Dense(2500, input_dim=2304, activation='relu'))      # first layer
model.add(Dense(2000, activation='relu'))                      # second layer
model.add(Dense(1000, activation='relu'))                      # third layer
model.add(Dense(100, activation='relu'))                       # fourth layer
model.add(Dense(1, activation='sigmoid'))                      # fifth layer

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])   # combine the layers into full model
model.fit(X_train, y_train, epochs=15, batch_size=1000)                             # fit the training data to the model

model.summary()                                                # prints summary of the neural network

predictions = (model.predict(X_test) > 0.5).astype("int32")    # using the test data, predicts the labels
accuracy = sum(np.array(predictions == y_test)) / len(X_test)  # checks the accuracy of the predictions
print(accuracy * 100)                                          # prints out the accuracy

predictions = (model.predict(X_custom) > 0.5).astype("int32")  # using the test data, predicts the labels of custom
print_pred()                                                   # prints photos for comparison with smiling prediction
