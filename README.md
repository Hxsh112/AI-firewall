# AI-firewall
AI- Powered firewall that detects and blocks harmful prompts and responses using LLM moderation layers. In a nutshell not your traditional firewalls.
# AI Firewall - Prototype
Minimal prototype that demonstrates an ML-driven malware/behavior detector using synthetic network/endpoint features. Designed for portfolio/demo use.
## What this repo contains
- Data generator & training that produces a simple RandomForest classifier
- FastAPI detection endpoint (`/detect`) that accepts JSON feature vectors
- Streamlit dashboard to preview detections and generate samples
## Quick start (Linux / WSL / macOS)
1. Clone repo
```bash
git clone <https://github.com/Hxsh112/AI-firewall>
cd ai-firewall
