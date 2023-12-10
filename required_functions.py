# -*- coding: utf-8 -*-
"""required_functions.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16poHN9kJKvsD3b5nFxbkR-Te5D0f0ay1
"""

def build_model(df,col1,col2,model_name):
  required_data = df.iloc[:, [ col1, col2, 30]].copy()
  required_data.dropna(inplace=True)

  Img_paths = required_data.iloc[:, -1]
  y = required_data.iloc[:, :2]

  X = []

  for i in Img_paths:
    itensor = tf.image.rgb_to_grayscale(tf.convert_to_tensor(Image.open(i),dtype=tf.float32))
    X.append(itensor/255)
  X = np.array(X)

  model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32,3,activation='relu',input_shape=(96,96,1)),
    tf.keras.layers.MaxPool2D(2),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Conv2D(64,3,activation='relu'),
    tf.keras.layers.MaxPool2D(2),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Conv2D(128,3,activation='relu'),
    tf.keras.layers.MaxPool2D(2),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Conv2D(256,3,activation='relu'),
    tf.keras.layers.MaxPool2D(2),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128,activation='relu'),
    tf.keras.layers.Dense(2,activation='linear'),
    tf.keras.layers.Lambda(lambda x: x * 96)
  ])

  model.compile(loss = 'mae',
                optimizer = tf.keras.optimizers.SGD(learning_rate=0.0001,momentum=0.9),
                metrics = ['mae','mse'])
  model.fit(X,y,epochs=50)

  model.save(model_name)
  return 0