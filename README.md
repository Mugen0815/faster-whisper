# Faster Whisper Docker Stack

Docker Compose stack for running a local `faster-whisper` API with NVIDIA GPU support.

The stack builds the API container locally, uses CUDA for inference, and keeps Whisper models persistent on the host.

## Features

- Local speech-to-text API based on `faster-whisper`
- NVIDIA GPU / CUDA support
- Default model: `large-v3`
- Default compute type: `float16`
- Persistent model cache
- Simple Docker Compose setup

## Requirements

- Docker
- Docker Compose v2
- NVIDIA GPU
- NVIDIA driver
- NVIDIA Container Toolkit

You can verify GPU access from Docker with:

```bash
docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi
```

## Setup

Clone the repository:

```bash
git clone git@github.com:YOUR_USER/faster-whisper-stack.git
cd faster-whisper-stack
```

Create local runtime directories:

```bash
mkdir -p models tmp
```

Build and start the stack:

```bash
docker compose up -d --build
```

Show logs:

```bash
docker compose logs -f whisper-api
```

Stop the stack:

```bash
docker compose down
```

## Service

The API container is exposed on the host at:

```text
http://localhost:10300
```

Internally, the container listens on port `8000`.

## Configuration

The default configuration is defined in `docker-compose.yml`:

```yaml
environment:
  - WHISPER_MODEL=large-v3
  - WHISPER_DEVICE=cuda
  - WHISPER_COMPUTE_TYPE=float16
```

### Environment variables

| Variable | Description | Default |
|---|---|---|
| `WHISPER_MODEL` | Whisper model to use | `large-v3` |
| `WHISPER_DEVICE` | Inference device | `cuda` |
| `WHISPER_COMPUTE_TYPE` | Compute type for inference | `float16` |

Example CPU configuration:

```yaml
environment:
  - WHISPER_MODEL=small
  - WHISPER_DEVICE=cpu
  - WHISPER_COMPUTE_TYPE=int8
```

## Volumes

```yaml
volumes:
  - ./models:/models
  - ./tmp:/tmp/audio
```

| Host path | Container path | Purpose |
|---|---|---|
| `./models` | `/models` | Persistent Whisper model cache |
| `./tmp` | `/tmp/audio` | Temporary audio files |

Model files can be several gigabytes in size and should not be committed to Git.

## GPU Selection

By default, the stack uses GPU `0`:

```yaml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          device_ids: ['0']
          capabilities: [gpu]
```

To use another GPU, change `device_ids`.

Example:

```yaml
device_ids: ['1']
```

## Useful Commands

Rebuild the image:

```bash
docker compose build --no-cache
```

Restart the API container:

```bash
docker compose restart whisper-api
```

Open a shell inside the container:

```bash
docker exec -it whisper-api sh
```

## Suggested `.gitignore`

```gitignore
.env
*.env

models/
tmp/
logs/
cache/

__pycache__/
*.pyc
.DS_Store
```

## License

MIT — see [LICENSE](LICENSE).
