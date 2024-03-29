FROM python:3.9-slim as python
ENV PYTHONUNBUFFERED=true
WORKDIR /app

FROM python as poetry
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN apt-get update
RUN apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python -
COPY . ./
RUN poetry install --no-interaction --no-ansi --only main
RUN apt-get --purge remove -y \
    build-essential

FROM python as runtime
ENV PATH="/app/.venv/bin:$PATH"
COPY --from=poetry /app /app
RUN find /app | grep -E "(__pycache__|\.pyc$)" | xargs rm -rf
RUN rm -rf htmlcov .coverage .vscode
ENV FLASK_APP="run.py"
EXPOSE 8080
# ENTRYPOINT [ python3" ]
CMD ["/app/.venv/bin/flask", "run", "--host=0.0.0.0", "--port=8080"]
