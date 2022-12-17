FROM python:3.10-slim-bullseye

LABEL org.opencontainers.image.source=https://github.com/jacksonisiah/yaris
LABEL org.opencontainers.image.description="Chloe"
LABEL org.opencontainers.image.licenses=ISC

RUN python -m ensurepip --upgrade \
    && apt-get update \
    && apt-get install -y --no-install-recommends curl=7.74.0-1.3+deb11u3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="${PATH}:/root/.local/bin"

COPY . /app/
WORKDIR /app

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --only main

ENTRYPOINT ["python", "./main.py"]
