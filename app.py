
import os
import json
import pickle
import datetime
import requests
import numpy as np
import cv2

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, send_file
from flask_socketio import SocketIO

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from ml.text_preprocess import clean_text


# =====================================================
# ENV
# =====================================================
load_dotenv()

HOST = os.getenv("FLASK_HOST", "127.0.0.1")
PORT = int(os.getenv("FLASK_PORT", 5000))
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

MAX_LEN = 200
IMG_SIZE = 224
STATS_FILE = "stats.json"


# =====================================================
# APP
# =====================================================
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


# =====================================================
# LOAD MODELS
# =====================================================
print("Loading models...")

text_model = load_model("models/text_lstm.h5")
image_model = load_model("models/image_cnn.h5")

with open("models/tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

print("Models loaded ✅")


# =====================================================
# STATS
# =====================================================
def load_stats():
    if not os.path.exists(STATS_FILE):
        return {"real": 0, "fake": 0, "history": []}

    with open(STATS_FILE) as f:
        return json.load(f)


def save_stats(data):
    with open(STATS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def update_stats(label, score, typ):

    stats = load_stats()

    if label == "Real":
        stats["real"] += 1
    else:
        stats["fake"] += 1

    stats["history"].append({
        "time": datetime.datetime.now().isoformat(),
        "type": typ,
        "label": label,
        "score": score
    })

    save_stats(stats)
    socketio.emit("stats_update", stats)


# =====================================================
# ✅ FIXED TEXT PREDICTION (IMPORTANT)
# =====================================================

def predict_text(text):

    text = clean_text(text)

    seq = tokenizer.texts_to_sequences([text])
    seq = pad_sequences(seq, maxlen=MAX_LEN)

    prob = float(text_model.predict(seq, verbose=0)[0][0])  # already sigmoid

    print("DEBUG probability:", prob)

    # ✅ label
    label = "Real" if prob >= 0.5 else "Fake"

    # ✅ credibility = probability of being REAL
    confidence = max(prob, 1 - prob)
    score = int(confidence * 100)

    if prob >= 0.75:
        explanation = "Highly credible content"
    elif prob >= 0.5:
        explanation = "Likely real but verify"
    elif prob >= 0.25:
        explanation = "Suspicious content detected"
    else:
        explanation = "High chance of misinformation"

    return label, score, explanation

# =====================================================
# ✅ FIXED IMAGE PREDICTION
# =====================================================
def predict_image(file):

    file_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img.astype("float32")

    img = preprocess_input(img)
    img = np.expand_dims(img, 0)

    prob = float(image_model.predict(img, verbose=0)[0][0])

    print("IMAGE PROB:", prob)

    # =================================================
    # ✅ ONLY CHANGE → labels flipped
    # =================================================
    label = "Fake" if prob >= 0.5 else "Real"
    confidence = max(prob, 1 - prob)
    score = int(confidence * 100)
    # =================================================

    if label == "Real":
        explanation = "Image appears authentic"
    else:
        explanation = "AI generated or fake image suspected"

    return label, score, explanation

# =====================================================
# ROUTES
# =====================================================
@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/overview")
def overview():
    return render_template("Overview.html")


@app.route("/analyze")
def analyze():
    return render_template("analyze.html")


@app.route("/analytics")
def analytics():
    return render_template("analytics.html")


@app.route("/live")
def live_news_page():
    return render_template("live_news.html")


# =====================================================
# ANALYZE API
# =====================================================
@app.route("/api/analyze", methods=["POST"])
def api_analyze():

    text = request.form.get("text")
    image = request.files.get("image")

    if text and text.strip():
        label, score, explanation = predict_text(text)
        typ = "text"

    elif image:
        label, score, explanation = predict_image(image)
        typ = "image"

    else:
        return jsonify({"error": "No input"}), 400

    update_stats(label, score, typ)

    return jsonify({
        "label": label,
        "score": score,
        "explanation": explanation
    })


# =====================================================
# STATS API
# =====================================================
@app.route("/stats-data")
def stats_data():
    return jsonify(load_stats())


# =====================================================
# LIVE NEWS
# =====================================================
@app.route("/api/live-news")
def api_live_news():

    if not NEWS_API_KEY:
        return jsonify([{
            "title": "Demo: Government launches new AI security bill",
            "source": "Demo",
            "url": "#",
            "label": "Real",
            "score": 90
        }])

    try:

        url = f"https://newsapi.org/v2/top-headlines?country=us&pageSize=10&apiKey={NEWS_API_KEY}"
        res = requests.get(url, timeout=6).json()

        articles = []

        for a in res.get("articles", []):
            title = a.get("title", "")

            if not title:
                continue

            label, score, _ = predict_text(title)

            articles.append({
                "title": title,
                "source": a.get("source", {}).get("name", ""),
                "url": a.get("url", "#"),
                "label": label,
                "score": score
            })

        return jsonify(articles)

    except:
        return jsonify([])


# =====================================================
# RUN
# =====================================================
if __name__ == "__main__":
    socketio.run(app, host=HOST, port=PORT, debug=True)