import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from src.helpers.is_saas import is_saas

if __name__ == "__main__":
    df = pd.read_json("files/company-dataset.json")
    df["is_saas"] = df["description"].apply(is_saas)

    # NOTE(lfacciolo) huge train_size sample but given limited amount of companies, will prioritize training. will lead to overfitting
    x_train, x_test, y_train, y_test = train_test_split(
        df["description"], df["is_saas"], test_size=0.1
    )

    # NOTE(lfacciolo) term frequency - inverse document frequency to evaluate important words in text, pass as a matrix of importance to log reg
    """
    further understanding of class weights, n_grams (number of words to be considered as a feature), and other tweaks necessary in order to make a decent model. this will work fine for the given example. would need more data to test and validate.
    """
    pipeline = Pipeline([("tfidf", TfidfVectorizer()), ("clf", LogisticRegression())])

    # Train
    pipeline.fit(x_train, y_train)
    # NOTE(lfacciolo) save pkl in order to use it later
    joblib.dump(pipeline, "files/saas_classifier.pkl")

    # Evaluate
    y_pred = pipeline.predict(x_test)
    print(classification_report(y_test, y_pred))
