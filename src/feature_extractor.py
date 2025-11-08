import numpy as np
import pandas as pd

FEATURE_COLUMNS = [
    "src_port",
    "dst_port",
    "pkt_count",
    "byte_count",
    "duration",
    "entropy",
    "uncommon_dst_ip",
    "process_spawn_count",
]


def simulate_sample(n=1, random_state=None):
    rng = np.random.RandomState(random_state)
    src_port = rng.randint(1024, 65535, size=n)
    dst_port = rng.choice([80, 443, 22, 445, 8080, 53, 0], size=n, p=[0.25,0.25,0.05,0.05,0.1,0.2,0.1])
    pkt_count = rng.poisson(20, size=n)
    byte_count = pkt_count * rng.randint(40, 1500, size=n)
    duration = rng.exponential(scale=1.0, size=n)
    entropy = rng.uniform(1.0, 8.0, size=n)
    uncommon_dst_ip = rng.choice([0,1], size=n, p=[0.95,0.05])
    process_spawn_count = rng.poisson(1, size=n)

    df = pd.DataFrame({
        "src_port": src_port,
        "dst_port": dst_port,
        "pkt_count": pkt_count,
        "byte_count": byte_count,
        "duration": duration,
        "entropy": entropy,
        "uncommon_dst_ip": uncommon_dst_ip,
        "process_spawn_count": process_spawn_count,
    })
    return df


def features_from_json(payload: dict):
    # expects keys matching FEATURE_COLUMNS
    # convert to DataFrame with a single row
    row = {k: payload.get(k, 0) for k in FEATURE_COLUMNS}
    return pd.DataFrame([row])
