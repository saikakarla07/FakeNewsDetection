# ============================================
# Image preprocessing utilities (FINAL FIXED)
# ============================================

import os
import cv2
import numpy as np


def load_images(size=224, base_path="datasets/images"):

    X = []
    y = []

    classes = {
        "fake": 0,
        "real": 1
    }

    for label_name, label in classes.items():

        class_path = os.path.join(base_path, label_name)

        for root, dirs, files in os.walk(class_path):

            for file in files:

                if file.lower().endswith((".jpg", ".png", ".jpeg")):

                    img_path = os.path.join(root, file)

                    img = cv2.imread(img_path)

                    if img is None:
                        continue

                    img = cv2.resize(img, (size, size))

                    # ✅ DO NOT normalize here
                    X.append(img.astype("float32"))
                    y.append(label)

    X = np.array(X)
    y = np.array(y)

    print("Loaded images:", len(X))
    print("Fake:", sum(y == 0))
    print("Real:", sum(y == 1))

    return X, y