# TruthFinder — Fake News Detection System

TruthFinder is an AI-powered web application that analyzes **news text and images** to identify potentially fake or real content.

The system combines a **Bidirectional LSTM (BiLSTM) model for text classification** with a **MobileNetV2-based image classification model** and provides an interactive Flask web interface.

## Features

### 📰 Text News Analysis

- Accepts pasted news content.
- Cleans and preprocesses the text.
- Uses a trained BiLSTM model to classify content as **Real** or **Fake**.
- Displays a credibility/confidence score and explanation.

### 🖼️ Image Verification

- Allows users to upload news-related images.
- Resizes and preprocesses images automatically.
- Uses a MobileNetV2 transfer-learning model.
- Detects whether an image is likely **Real** or **Fake/AI-generated**.

### 📊 Analytics Dashboard

- Tracks total analyses.
- Displays real vs. fake detection counts.
- Shows hourly activity and content distribution.
- Displays recent analysis history.
- Uses Socket.IO for live statistics updates.

### 🔴 Live News Feed

- Fetches current headlines using NewsAPI.
- Automatically analyzes news headlines using the text model.
- Displays predicted labels and confidence scores.
- Includes search and category filtering.

### 🎨 Interactive Web Interface

- Flask-based web application.
- Responsive pages for:
  - Landing
  - Overview
  - Analysis
  - Analytics
  - Live News
- Dynamic JavaScript interactions and charts.

---

## Technology Stack

### Backend

- Python
- Flask
- Flask-SocketIO
- REST API

### Machine Learning

- TensorFlow
- Keras
- Bidirectional LSTM
- MobileNetV2 Transfer Learning
- Scikit-learn
- NumPy
- Pandas
- OpenCV

### Frontend

- HTML5
- CSS3
- JavaScript
- Chart.js
- Socket.IO

### External Services

- NewsAPI for live news headlines

---

## Project Structure

```text
FakeNewsDetection/
│
├── app.py
├── requirements.txt
├── stats.json
│
├── ml/
│   ├── combine_dataset.py
│   ├── image_preprocess.py
│   ├── text_preprocess.py
│   ├── train_image_model.py
│   └── train_text_model.py
│
├── templates/
│   ├── base.html
│   ├── landing.html
│   ├── Overview.html
│   ├── analyze.html
│   ├── analytics.html
│   └── live_news.html
│
└── static/
    ├── css/
    │   └── style.css
    │
    └── js/
        ├── analytics.js
        ├── analyze.js
        └── live_news.js

Machine Learning Approach
1. Text Classification

The text pipeline combines the title and body of fake and real news articles.

Processing Steps
1.Load fake and real news datasets.
2.Combine title and article text.
3.Clean the text.
   -Convert text to lowercase.
   -Remove URLs.
   -Remove non-alphabetic characters.
   -Remove extra whitespace.
4.Balance the two classes.
5.Tokenize the text using a Keras tokenizer.
6.Convert text into padded sequences.
7.Train a Bidirectional LSTM neural network.
8.Save the trained model and tokenizer.
Text Model Architecture:
Embedding
    ↓
Bidirectional LSTM (64)
    ↓
Dropout
    ↓
Bidirectional LSTM (32)
    ↓
Dropout
    ↓
Dense (64, ReLU)
    ↓
Dense (1, Sigmoid)

2. Image Classification
The image classification model uses MobileNetV2 with ImageNet pre-trained weights.

Processing Steps:
1.Load images from fake and real categories.
2.Resize images to 224 × 224.
3.Apply MobileNetV2 preprocessing.
4.Split the dataset into training and testing sets.
5.Apply image augmentation.
6.Freeze most MobileNetV2 layers.
7.Fine-tune the final layers.
8.Use the trained model for image classification.
Image Model Architecture:
MobileNetV2
    ↓
Global Average Pooling
    ↓
Dense (128, ReLU)
    ↓
Dropout
    ↓
Dense (1, Sigmoid)

Installation
1. Clone the Repository
git clone <your-repository-url>
cd FakeNewsDetection
2. Create a Virtual Environment
Windows:
python -m venv venv
venv\Scripts\activate
Linux/macOS:
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt

Environment Variables:

The application can use environment variables for configuration and the NewsAPI key.
Create a .env file in the project root:
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
NEWS_API_KEY=your_newsapi_key
Use a placeholder such as:
NEWS_API_KEY=your_newsapi_key

Running the Application

From the FakeNewsDetection directory:
python app.py
The application will normally be available at:
http://127.0.0.1:5000
Open the address in your browser.

Application Workflow:
                 ┌─────────────────────┐
                 │      User Input     │
                 └──────────┬──────────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
          News Text                    Image
              │                           │
              ▼                           ▼
    Text Preprocessing          Image Preprocessing
              │                           │
              ▼                           ▼
       Tokenizer + BiLSTM          MobileNetV2 Model
              │                           │
              └─────────────┬─────────────┘
                            ▼
                    Prediction Result
                            │
                  ┌─────────┴─────────┐
                  │                   │
               Real/Fake          Confidence
                  │                   │
                  └─────────┬─────────┘
                            ▼
                     Analytics / UI

Analyze Image:
Send a POST request to:
/api/analyze
with an image file using the image form field.
The image is preprocessed and passed through the image classification model to generate a prediction.


Training the Models:

The machine learning training scripts are available in the ml/ directory.
-Train the Text Model
   python ml/train_text_model.py
-Train the Image Model
   python ml/train_image_model.py
The generated trained models should be stored locally in the models/ directory.
Large trained model files are not included in this GitHub repository.

Important Notes:

-The predictions are model-based estimates, not definitive proof that a news article or image is true or false.
-A high confidence score does not guarantee factual accuracy.
-The system is intended as a fake-news detection and research/educational tool.
-Prediction quality depends heavily on the training datasets and model performance.
-NewsAPI requires a valid API key for live headline retrieval.
-API keys and other secrets should never be committed to GitHub.

Future Enhancements:

-Add transformer-based NLP models such as BERT.
-Improve image detection using larger and more diverse datasets.
-Add source credibility verification.
-Combine text, image, and source metadata into a multimodal model.
-Add explainable AI features.
-Add user authentication and personalized analysis history.
-Deploy the application using Docker and a cloud platform.
-Add automated model evaluation reports.
-Improve multilingual fake-news detection.

Use Cases:

-News credibility screening
-Academic projects and demonstrations
-Fake-news awareness systems
-Media-literacy applications
-AI/ML research projects
-Image authenticity experimentation

License:
This project is intended for educational and research purposes.
An appropriate open-source license such as MIT can be added if the project is intended for public distribution.

