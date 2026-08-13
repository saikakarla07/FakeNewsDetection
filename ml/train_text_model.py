# ============================================
# BETTER TEXT MODEL (FIXED)
# ============================================

import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.utils import resample
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, Bidirectional
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.utils import shuffle
from combine_dataset import combine_datasets
from text_preprocess import clean_text


MAX_WORDS = 15000
MAX_LEN = 200

combine_datasets()

df = pd.read_csv("datasets/text/combined_news.csv")

df["text"] = df["text"].apply(clean_text)


# =================================================
# 🔥 BALANCE DATASET (VERY IMPORTANT)
# =================================================
min_len = df["label"].value_counts().min()

df = (
    df.groupby("label")
      .apply(lambda x: x.sample(min_len, random_state=42))
      .reset_index(drop=True)
)

df = shuffle(df, random_state=42)

print("Balanced counts:")
print(df["label"].value_counts())


texts = df["text"]
labels = df["label"]


tokenizer = Tokenizer(num_words=MAX_WORDS, oov_token="<OOV>")
tokenizer.fit_on_texts(texts)

X = tokenizer.texts_to_sequences(texts)
X = pad_sequences(X, maxlen=MAX_LEN)

y = labels.values


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y
)


# =================================================
# 🔥 STRONGER MODEL (BiLSTM + Dropout)
# =================================================
model = Sequential([
    Embedding(MAX_WORDS, 128, input_length=MAX_LEN),

    Bidirectional(LSTM(64, return_sequences=True)),
    Dropout(0.3),

    Bidirectional(LSTM(32)),
    Dropout(0.3),

    Dense(64, activation="relu"),
    Dense(1, activation="sigmoid")
])


model.compile(
    loss="binary_crossentropy",
    optimizer="adam",
    metrics=["accuracy"]
)


model.fit(
    X_train,
    y_train,
    epochs=8,
    batch_size=64,
    validation_split=0.2
)


loss, acc = model.evaluate(X_test, y_test)
print("Accuracy:", acc)


model.save("models/text_lstm.h5")

with open("models/tokenizer.pkl", "wb") as f:
    pickle.dump(tokenizer, f)

print("✅ TEXT MODEL TRAINED CORRECTLY")