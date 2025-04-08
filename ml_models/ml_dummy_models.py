import pandas as pd
from src.helpers.is_saas import is_saas
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

if __name__ == "__main__":
    df = pd.read_json("files/company-dataset.json")
    df["is_saas"] = df["description"].apply(is_saas)
    # Split into train/test
    x_train, x_test, y_train, y_test = train_test_split(
        df["description"], df["is_saas"], test_size=0.2, random_state=42
    )
    # Build pipeline
    pipeline = Pipeline([("tfidf", TfidfVectorizer()), ("clf", LogisticRegression())])

    # Train
    pipeline.fit(x_train, y_train)
    joblib.dump(pipeline, "files/saas_classifier.pkl")

    # Evaluate
    y_pred = pipeline.predict_proba(x_test)
    print(classification_report(y_test, y_pred))
