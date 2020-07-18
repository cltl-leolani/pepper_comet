FROM tensorflow/tensorflow:1.15.2

WORKDIR /

COPY requirements.txt ./

RUN apt-get update && apt-get install -y \
    git wget \
    && rm -rf /var/lib/apt/lists/* \
    \
    && pip install --no-cache-dir -r requirements.txt \
    && python -m spacy download en \
    \
    && git clone --single-branch https://github.com/atcbosselut/comet-commonsense.git comet \
    && cd comet \
    && git checkout 070aad114600b36296ef8420325e3d4cef0be470 \
    && rm -rf .git \
    \
    && bash scripts/setup/get_atomic_data.sh \
    && bash scripts/setup/get_conceptnet_data.sh \
    && bash scripts/setup/get_model_files.sh \
    && python scripts/data/make_atomic_data_loader.py \
    && python scripts/data/make_conceptnet_data_loader.py \
    \
    && pip install --no-cache-dir gdown \
    && gdown https://drive.google.com/uc?id=1FccEsYPUHnjzmX-Y5vjCBeyRt1pLo8FB \
    && tar -xvzf pretrained_models.tar.gz \
    && rm pretrained_models.tar.gz

WORKDIR /pepper_comet

COPY rest ./

ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_APP="/pepper_comet/inference_endpoint.py"
ENV PYTHON_PATH="/comet:/pepper_comet:${PYTHON_PATH}"

WORKDIR /comet
CMD flask run

EXPOSE 5000
