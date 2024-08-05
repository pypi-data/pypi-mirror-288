---
title: lisa + gradio + fastapi + ZeroGPU
emoji: ⚡
colorFrom: red
colorTo: purple
sdk: gradio
sdk_version: 4.40.0
app_file: app.py
pinned: true
---

# LISA (Reasoning Segmentation via Large Language Model) on cuda, now with huggingface ZeroGPU support!

## Update requirements.txt, needed on HuggingFace demo

```bash
python -m samgis_core.utilities.update_requirements_txt \
  --req_no_version_path requirements_no_versions.txt \
  --req_output_path requirements.txt
```

Pay attention about any unnecessary dependency, e.g. gradio_client==1.2.0 (it's installed with gradio).

## Exec jupyter on the remote server with port forwarding on localhost

1. checkout repo, install venv with jupyter
2. port forwarding in localhost wiht private key: `ssh -i /path/to/private_key name@endpoint.com -L 8889:localhost:8889 -N -f`
3. start the jupyter-lab server
4. connect to page in localhost

## Commands to work on remote virtual machines (e.g. SaturnCloud) after clone and git lfs install

```bash
cd ~/workspace/lisa-on-cuda/
rm -rf lisa_venv 
python3 -m venv lisa_venv
ln -s lisa_venv/ venv
source  venv/bin/activate
pip --version
which python
python -m pip install pip wheel --upgrade
python -m pip install pytest pytest-cov jupyterlab
python -m pip install -r requirements.txt
nohup jupyter-lab &
tail -F nohup.out
```

# Jupyterlab Howto

To run the `test.ipynb` notebook you should already:
- cloned project https://huggingface.co/spaces/aletrn/lisa-on-cuda with active git lfs
- created and activated a virtualenv
- installed jupyterlab dependencies from requirements_jupyter.txt
- installed dependencies from requirements.txt

## Hardware requirements for local usage

- an nvidia gpu with 10 or 12GB of memory (a T4 should suffice)
- at least 16GB of system ram

## Hardware requirements on huggingface ZeroGPU

Right now (July 2024) huggingface let use ZeroGPU Nvidia A100 GPUs.

[![Gradio](https://img.shields.io/badge/Gradio-Online%20Demo-blue)](http://103.170.5.190:7860/)
[![Open in OpenXLab](https://cdn-static.openxlab.org.cn/app-center/openxlab_app.svg)](https://openxlab.org.cn/apps/detail/openxlab-app/LISA)

See [LISA](https://github.com/dvlab-research/LISA) for details on the original project.
Note that the authors don't keep the project updated anymore.
