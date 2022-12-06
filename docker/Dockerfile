FROM python:3.10-slim-bullseye

RUN pip install -U --no-cache-dir --no-install-recommends pip \
    && apt-get update \
    && apt-get install -y curl netcat \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="${PATH}:/root/.local/bin"

COPY . /app/
WORKDIR /app

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --only main

ENTRYPOINT ["python", "./main.py"]
