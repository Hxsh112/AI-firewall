import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
import joblib
import pandas as pd
from src.feature_extractor import simulate_sample

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
os.makedirs(MODEL_DIR, exist_ok=True)


def make_synthetic_dataset(n_samples=5000, random_state=42):
    # create balanced-ish dataset with engineered rule for "malicious"
    df = simulate_sample(n=n_samples, random_state=random_state)
    # simple rule to assign malicious label for training: high entropy + uncommon dst ip + many process spawns
    score = (df['entropy'] > 6.0).astype(int) + (df['uncommon_dst_ip'] == 1).astype(int) + (df['process_spawn_count'] >= 2).astype(int)
    y = (score >= 2).astype(int)
    return df, y


if __name__ == "__main__":
    X, y = make_synthetic_dataset(n_samples=8000)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

    clf = RandomForestClassifier(n_estimators=200, max_depth=8, random_state=1, n_jobs=-1)
    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    probs = clf.predict_proba(X_test)[:,1]

    print(classification_report(y_test, preds))
    try:
        auc = roc_auc_score(y_test, probs)
        print("AUC:", auc)
    except Exception:
        pass

    model_path = os.path.join(MODEL_DIR, "model.pkl")
    joblib.dump(clf, model_path)
    print("Saved model to", model_path)
