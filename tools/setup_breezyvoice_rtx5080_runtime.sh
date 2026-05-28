#!/usr/bin/env bash
set -euo pipefail

# Local-only BreezyVoice runtime setup for RTX 5080 / sm_120.
# This keeps the official BreezyVoice repo and Python environment under .local/.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

BREEZYVOICE_REPO="${BREEZYVOICE_REPO:-.local/BreezyVoice}"
VENV_DIR="${BREEZYVOICE_VENV:-.local/breezyvoice/runtime/v1/venv}"
PYTHON_BIN="$VENV_DIR/bin/python"

if [[ ! -d "$BREEZYVOICE_REPO/.git" ]]; then
  git clone --recurse-submodules https://github.com/mtkresearch/BreezyVoice.git "$BREEZYVOICE_REPO"
else
  git -C "$BREEZYVOICE_REPO" fetch --all --prune
fi

uv venv -p 3.10 "$VENV_DIR"

# openai-whisper 20231117 still imports pkg_resources during build.
uv pip install --python "$PYTHON_BIN" 'setuptools<81' wheel

uv pip install \
  --python "$PYTHON_BIN" \
  -r "$BREEZYVOICE_REPO/requirements.txt" \
  --index-strategy unsafe-best-match \
  --no-build-isolation

# HyperPyYAML 1.2.2 is not compatible with the newest ruamel.yaml loader API.
uv pip install --python "$PYTHON_BIN" 'ruamel.yaml==0.17.40' 'ruamel.yaml.clib==0.2.8'

# Official BreezyVoice pins torch 2.3.1+cu118. RTX 5080 requires an sm_120
# capable wheel; CUDA 12.8 PyTorch wheels satisfy that on this machine.
UV_HTTP_TIMEOUT="${UV_HTTP_TIMEOUT:-600}" uv pip install \
  --python "$PYTHON_BIN" \
  --index-url https://download.pytorch.org/whl/cu128 \
  --upgrade \
  'torch==2.11.0+cu128' \
  'torchaudio==2.11.0+cu128'

# Prompt-audio rendering uses BreezyVoice ONNX frontend components. The CPU
# wheel shadows the GPU wheel when both are installed, so replace it explicitly
# and keep NumPy on the 1.x ABI required by the local audio stack.
uv pip uninstall --python "$PYTHON_BIN" onnxruntime onnxruntime-gpu || true
UV_HTTP_TIMEOUT="${UV_HTTP_TIMEOUT:-600}" uv pip install \
  --python "$PYTHON_BIN" \
  'onnxruntime-gpu==1.23.2' \
  'numpy==1.26.4' \
  'protobuf==4.25.0' \
  'packaging==24.2'

"$PYTHON_BIN" - <<'PY'
import onnxruntime as ort
import torch
import torchaudio

print("torch", torch.__version__)
print("torchaudio", torchaudio.__version__)
print("onnxruntime", ort.__version__)
print("onnxruntime_providers", ort.get_available_providers())
print("cuda_available", torch.cuda.is_available())
if torch.cuda.is_available():
    print("device", torch.cuda.get_device_name(0))
    print("capability", torch.cuda.get_device_capability(0))
    value = (torch.ones((32, 32), device="cuda") @ torch.ones((32, 32), device="cuda"))[0, 0].item()
    print("cuda_smoke", value)
PY
