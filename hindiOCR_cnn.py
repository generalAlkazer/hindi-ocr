import tensorflow as tf
import pickle
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D
from keras.callbacks import EarlyStopping

trainDataGen = ImageDataGenerator(
    rotation_range=5,
    width_shift_range=0.1,
    height_shift_range=0.1,
    rescale=1.0 / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=False,
    fill_mode='nearest')

test_datagen = ImageDataGenerator(rescale=1. / 255)
train_generator = trainDataGen.flow_from_directory(
    "DevanagariHandwrittenCharacterDataset/Train",
    target_size=(32, 32),
    batch_size=32,
    color_mode="grayscale",
    class_mode="categorical")
prev = ""
labels = ["ka", "kha", "ga", "gha", "kna", "cha", "chha", "ja", "jha", "yna", "t`a", "t`ha", "d`a", "d`ha", "adna",
          "ta", "tha", "da", "dha", "na", "pa", "pha", "ba", "bha", "ma", "yaw", "ra", "la", "waw", "sha", "shat", "sa",
          "ha", "aksha", "tra", "gya", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
count = 0;

validation_generator = test_datagen.flow_from_directory(
    "DevanagariHandwrittenCharacterDataset/Test",
    target_size=(32, 32),
    batch_size=32,
    color_mode="grayscale",
    class_mode='categorical')

model = Sequential()
model.add(Conv2D(filters=32,
                 kernel_size=(3, 3),
                 strides=1,
                 padding='same',
                 activation="relu",
                 input_shape=(32, 32, 1)))

model.add(Conv2D(filters=32,
                 kernel_size=(3, 3),
                 strides=1,
                 padding='same',
                 activation="relu",
                 input_shape=(32, 32, 1)))

model.add(MaxPool2D(pool_size=(2, 2),
                    strides=(2, 2),
                    padding="same"))

model.add(Conv2D(filters=64,
                 kernel_size=(3, 3),
                 padding='same',
                 strides=1,
                 activation="relu"))

model.add(Conv2D(filters=64,
                 kernel_size=(3, 3),
                 strides=1,
                 padding='same',
                 activation="relu"))

model.add(MaxPool2D(pool_size=(2, 2),
                    strides=(2, 2),
                    padding="same"))

model.add(Dropout(0.2))

model.add(Flatten())

model.add(Dense(128,
                activation="relu",
                kernel_initializer="uniform"))

model.add(Dense(64,
                activation="relu",
                kernel_initializer="uniform"))

model.add(Dense(46,
                activation="softmax",
                kernel_initializer="uniform"))

model.compile(optimizer="adam",
              loss="categorical_crossentropy",
              metrics=["accuracy"])

print(model.summary())

early_stopping_monitor = EarlyStopping(patience=2)

with tf.device('/gpu:0'):
    history = model.fit_generator(train_generator, epochs=10, validation_data=validation_generator,
                                  steps_per_epoch=2444, validation_steps=432, use_multiprocessing=True,
                                  callbacks=[early_stopping_monitor])

model.save("hindi_OCR_cnn_model_tf2.h5")
pickle.dump(model, open('hindi_OCR_cnn_model_pickle.pkl2', 'wb'))
