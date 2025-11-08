import os
import joblib
from src.feature_extractor import features_from_json, FEATURE_COLUMNS

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "model.pkl")


class ModelWrapper:
    def __init__(self, model_path=MODEL_PATH):
        self.model = joblib.load(model_path)

    def predict(self, payload: dict):
        df = features_from_json(payload)
        proba = float(self.model.predict_proba(df)[:,1][0])
        pred = int(self.model.predict(df)[0])
        return {"malicious": bool(pred), "score": proba}


# quick local test
if __name__ == "__main__":
    mw = ModelWrapper()
    sample = {
        "src_port": 40000,
        "dst_port": 445,
        "pkt_count": 120,
        "byte_count": 120000,
        "duration": 0.5,
        "entropy": 7.2,
        "uncommon_dst_ip": 1,
        "process_spawn_count": 3,
    }
    print(mw.predict(sample))
