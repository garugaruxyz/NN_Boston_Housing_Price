# -*- coding: utf-8 -*-
"""David_Gargaro_845738_assignment1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1W7j42HJ0EjhUJPFCPqOHVRAGDKMtH2iP

# Seeding and Dataset
"""

from tensorflow import keras
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from keras.utils import plot_model

keras.utils.set_random_seed(42)

(x_train, y_train), (x_test, y_test) = keras.datasets.boston_housing.load_data()

dframe_x = pd.DataFrame(x_train)
dframe_y = pd.DataFrame(y_train)

dframe_x.describe()

dframe_y.describe()

mean = x_train.mean(axis=0)
std = x_train.std(axis=0)
x_train = (x_train - mean) / std

mean = x_test.mean(axis=0)
std = x_test.std(axis=0)
x_test = (x_test - mean) / std

"""# Models and Training

Model 1:

*   **Layers**: 1 hidden layer
*   **Activation**: Relu in Hidden Layer, Linear in Output Layer
*   **Loss Function**: Mean Squared Error
*   **Optimizer**: Adam
*   **Regularization**: None

Model 2:

*   **Layers**: 2 hidden layers
*   **Activation**: Relu in Hidden Layer, Linear in Output Layer
*   **Loss Function**: Mean Squared Error
*   **Optimizer**: RMSprop
*   **Regularization**: L2 with regularization 0.001

Model 3:

*   **Layers**: 3 hidden layers
*   **Activation**: Relu in Hidden Layer, Linear in Output Layer
*   **Loss Function**: Mean Squared Error
*   **Optimizer**: Adam
*   **Regularization**: None

All the models are trained for epochs=300 and with validation_split=0.2
"""

## MODELLO 1 ##

model1 = keras.Sequential()

# Input layer + 1st hidden layer
model1.add(keras.layers.Dense(units=16, activation='relu', input_shape=(13,)))

# output layer
model1.add(keras.layers.Dense(1, activation = "linear"))

model1.summary()

# Impostazioni di ottimizzazione
optimizer = keras.optimizers.Adam(learning_rate=0.001)
loss = "mse"
model1.compile(optimizer=optimizer, loss=loss, metrics=[keras.metrics.RootMeanSquaredError()])

plot_model(model1, show_shapes=True)

from keras.src.regularizers import l2
## MODELLO 2 ##

model2 = keras.Sequential()

# Input layer + 1st hidden layer
model2.add(keras.layers.Dense(units=64, activation='relu', input_shape=(13,), kernel_regularizer=l2(0.001)))

# 2nd hidden layer
model2.add(keras.layers.Dense(units=32, activation='relu', kernel_regularizer=l2(0.001)))

# output layer
model2.add(keras.layers.Dense(1, activation = "linear"))

model2.summary()

# Impostazioni di ottimizzazione
optimizer = keras.optimizers.RMSprop(learning_rate=0.001)
loss = "mse"
model2.compile(optimizer=optimizer, loss=loss, metrics=[keras.metrics.RootMeanSquaredError()])

plot_model(model2, show_shapes=True)

from keras.api._v2.keras.layers import Dropout
## MODELLO 3 ##

model3 = keras.Sequential()

# Input layer + 1st hidden layer
model3.add(keras.layers.Dense(units=64, activation='relu', input_shape=(13,)))

# 2nd hidden layer
model3.add(keras.layers.Dense(units=32, activation='relu'))

# 3rd hidden layer
model3.add(keras.layers.Dense(units=16, activation='relu'))

# output layer
model3.add(keras.layers.Dense(1, activation = "linear"))

model3.summary()

# Impostazioni di ottimizzazione
optimizer = keras.optimizers.Adam(learning_rate=0.001)
loss = "mse"
model3.compile(optimizer=optimizer, loss=loss, metrics=[keras.metrics.RootMeanSquaredError()])

plot_model(model3, show_shapes=True)

history1 = model1.fit(x_train, y_train, epochs=300, validation_split=0.2)

history2 = model2.fit(x_train, y_train, epochs=300, validation_split=0.2)

history3 = model3.fit(x_train, y_train, epochs=300, validation_split=0.2)

"""# Results"""

def plot_performance(history):
  start_point = 5
  x = np.arange(5, len(history.history['loss']))
  print(len(x), len(history.history['loss'][start_point:]))
  plt.plot(x, history.history['loss'][start_point:], label='train')
  plt.plot(x, history.history['val_loss'][start_point:], label='validation')
  best_epoch_train = np.argmin(history.history['loss'])
  best_epoch_val = np.argmin(history.history['val_loss'])
  best_mse_val = np.min(history.history['val_loss'])
  best_mse_train = np.min(history.history['loss'])
  plt.scatter(best_epoch_train, (history.history['loss'][best_epoch_train]))
  plt.scatter(best_epoch_val, (history.history['val_loss'][best_epoch_val]))
  plt.title('Loss')
  plt.xlabel('Epochs')
  plt.ylabel('MSE')
  plt.annotate(f'Epoch {best_epoch_val + 1}', (best_epoch_val, best_mse_val))
  plt.annotate(f'Epoch {best_epoch_train + 1}', (best_epoch_train, best_mse_train))
  plt.legend()
  plt.show()
  print(f'Best MSE on validation is {best_mse_val} at epoch {best_epoch_val + 1}')

plot_performance(history1)

plot_performance(history2)

plot_performance(history3)

mse1, rmse1 = model1.evaluate(x_test, y_test)

mse2, rmse2 = model2.evaluate(x_test, y_test)

mse3, rmse3 = model3.evaluate(x_test, y_test)

predictions1 = model1.predict(x_test)
predictions2 = model2.predict(x_test)
predictions3 = model3.predict(x_test)

def compare_predictions(pred, gt):
  plt.plot(pred)
  plt.plot(gt)
  plt.scatter(np.arange(0, len(pred)),pred, label='Predictions')
  plt.scatter(np.arange(0, len(gt)), gt, label='GT')
  plt.ylabel('Price')
  plt.xlabel('Dataset records')
  plt.legend()
  plt.show()

compare_predictions(predictions1, y_test)

compare_predictions(predictions2, y_test)

compare_predictions(predictions3, y_test)

"""### Conclusion
In the quest to predict house prices with accuracy and precision, three distinct neural network architectures were designed and trained, ranging from the simplicity of Model 1 to the complexity of Model 3.

*   Model 1: loss: 20.9481 - root_mean_squared_error: 4.5769
*   Model 2: loss: 19.1986 - root_mean_squared_error: 4.3663
*   Model 3: loss: 15.0474 - root_mean_squared_error: 3.8791

Model 3, the deep network with more layers and complexity, appears to be the most promising for predicting house prices
"""