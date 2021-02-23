import numpy as np
import pandas as pd
import torch
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler


def normalize(train, val=None, test=None):
	train_min = train.reshape(-1, train.shape[-1]).min(0)
	train_max = train.reshape(-1, train.shape[-1]).max(0)

	train = (train - train_min) / (train_max - train_min)
	if val is not None:
		val = (val - train_min) / (train_max - train_min)
	if test is not None:
		test = (test - train_min) / (train_max - train_min)

	return train, val, test


def denormalize(normalized_d, min_val, max_val):
	return normalized_d * (max_val - min_val) + min_val


def process_gas_sensor_data(window_size=50, horizon=1, val_size=300, test_size=100):
	"""

	:param window_size: The number of timestamps to use to forecast
	:param horizon: The number of timestamps to forecast following each window
	:param val_size: Number of timestamps used for validation
	:param test_size: Number of timestamps used for test
	:return: dict consisting of feature names, x, and y
	"""
	df = pd.read_csv('datasets/gas_sensor_data.csv', delimiter=',')
	df.drop(['Time', 'Temperature', 'Rel_Humidity'], axis=1, inplace=True)
	df = df[['S4']]

	n = df.shape[0]
	values = df.values
	feature_names = df.columns.tolist()

	values = (values - np.min(values)) / (np.max(values) - np.min(values))

	# Create forecasting dataset
	x, y = [], []
	for i in range(n - window_size - horizon):
		window_end = i + window_size
		horizon_end = window_end + horizon
		x_i = values[i:window_end, :]
		y_i = values[window_end:horizon_end, :]
		x.append(x_i)
		y.append(y_i)

	# Splitting in train, val, test
	train_size = len(x) - val_size - test_size
	train_x = np.array(x[:train_size])
	train_y = np.array(y[:train_size])

	val_x = np.array(x[train_size:train_size+val_size])
	val_y = np.array(y[train_size:train_size+val_size])

	test_x = np.array(x[train_size+val_size:])
	test_y = np.array(y[train_size+val_size:])

	print(train_x.min(), train_x.max())
	print(train_y.min(), train_y.max())
	print(test_x.min(), test_y.max())

	train_x_min = train_x.min()
	train_x_max = train_x.max()

	# Normalize
	# train_x, val_x, test_x = normalize(train_x, val_x, test_x)
	# train_y, val_y, test_y = normalize(train_y, val_y, test_y)


	print("-- Processing done.")

	return {'feature_names': feature_names,
			'train_x': train_x,
			'train_y': train_y,
			'val_x': val_x,
			'val_y': val_y,
			'test_x': test_x,
			'test_y': test_y,
			'train_x_min': train_x_min,
			'train_x_max': train_x_max}


# data = process_gas_sensor_data(window_size=250, horizon=1)
# feature_names = data['feature_names']
# train_x = data['train_x']
# train_y = data['train_y']
#
# val_x = data['val_x']
# val_y = data['val_y']
#
# test_x = data['test_x']
# test_y = data['test_y']
#
# print(train_x.shape)
# print(val_x.shape)
# print(test_x.shape)
#
# s1 = train_x[0, :, 3]
# s1_next = train_y[0, :, 3]
#
# s1_all = np.concatenate((s1, s1_next), axis=0)
#
# plt.plot([i for i in range(len(s1_all))], s1_all)
# plt.title('concated y_hat')
# plt.show()
#
# s2 = train_y[1, :1, 3]
# s1_s2 = np.concatenate((s1, s2), axis=0)
#
# plt.plot([i for i in range(len(s1_s2))], s1_s2)
# plt.show()

