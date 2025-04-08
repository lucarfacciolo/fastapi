import joblib


def predict_saas(description: str, threshold: float = 0.5) -> bool:
    pipeline = joblib.load("src/ml_models/saas_classifier.pkl")
    saas_prob = pipeline.predict_proba([description])
    prob_true = saas_prob[:, 1][0]
    return True if prob_true > threshold else False
