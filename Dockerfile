FROM python:3.11

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir poetry==1.8.0  # Ensure Poetry version matches your setup
RUN poetry install --no-root

COPY . /app  

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
