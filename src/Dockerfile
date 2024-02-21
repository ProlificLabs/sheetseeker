FROM docker.io/python:3.12-slim-bullseye

#RUN useradd -ms /bin/bash serverrunner

RUN mkdir /app
WORKDIR /app

#RUN chown -R serverrunner:serverrunner .

#USER serverrunner

RUN python -m pip install --user pipx
RUN python -m pipx ensurepath

RUN $HOME/.local/bin/pipx install poetry

COPY ./pyproject.toml .
COPY ./poetry.lock .

RUN $HOME/.local/bin/poetry install

ENV PATH=$PATH:/root/.local/bin/

COPY . .
