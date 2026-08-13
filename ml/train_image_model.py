# ============================================
# FINAL IMAGE MODEL (Stable + Accurate)
# Transfer Learning with MobileNetV2
# ============================================

import numpy as np
from sklearn.model_selection import train_test_split

import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

from image_preprocess import load_images


IMG_SIZE = 224

print("Loading images...")
X, y = load_images(size=IMG_SIZE)

# ✅ CRITICAL
X = preprocess_input(X)


print("Splitting dataset...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    stratify=y,
    random_state=42
)


datagen = ImageDataGenerator(
    rotation_range=20,
    zoom_range=0.2,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True
)


base_model = MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,
    weights="imagenet"
)

# freeze most layers
for layer in base_model.layers[:-20]:
    layer.trainable = False


x = GlobalAveragePooling2D()(base_model.output)
x = Dense(128, activation="relu")(x)
x = Dropout(0.4)(x)
output = Dense(1, activation="sigmoid")(x)

model = Model(base_model.input, output)


model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)


print("Training model...")

model.fit(
    datagen.flow(X_train, y_train, batch_size=32),
    epochs=15,
    validation_data=(X_test, y_test)
)


loss, acc = model.evaluate(X_test, y_test)

print("FINAL IMAGE ACCURACY:", acc)

model.save("models/image_cnn.h5")

print("✅ Image model saved successfully")