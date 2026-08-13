# ============================================
# Combine datasets (ROOT SAFE VERSION)
# ============================================
import pandas as pd
import os

def combine_datasets():

    base = os.path.dirname(os.path.dirname(__file__))  # go to root

    fake_path = os.path.join(base, "datasets/text/fake_news.csv")
    real_path = os.path.join(base, "datasets/text/real_news.csv")
    out_path  = os.path.join(base, "datasets/text/combined_news.csv")

    fake = pd.read_csv(fake_path)
    real = pd.read_csv(real_path)

    # ✅ ONLY use title + text
    fake["text"] = fake["title"].fillna("") + " " + fake["text"].fillna("")
    real["text"] = real["title"].fillna("") + " " + real["text"].fillna("")

    fake["label"] = 0
    real["label"] = 1

    df = pd.concat([fake[["text","label"]], real[["text","label"]]], ignore_index=True)

    df = df.sample(frac=1, random_state=42)

    print(df["label"].value_counts())

    df.to_csv(out_path, index=False)

    print("✅ combined_news.csv created at:", out_path)


if __name__ == "__main__":
    combine_datasets()