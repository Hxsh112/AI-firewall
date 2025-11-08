from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.model_infer import ModelWrapper

app = FastAPI(title="AI Firewall - Demo")
model = ModelWrapper()


class Features(BaseModel):
    src_port: int
    dst_port: int
    pkt_count: int
    byte_count: int
    duration: float
    entropy: float
    uncommon_dst_ip: int
    process_spawn_count: int


@app.post("/detect")
def detect(features: Features):
    payload = features.dict()
    try:
        result = model.predict(payload)
        return {"ok": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    return {"ok": True}
