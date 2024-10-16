FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false && \
	poetry install --no-dev --no-interaction --no-ansi

COPY . .

EXPOSE 80

CMD ["uvicorn", "warehouse.main:app", "--host", "0.0.0.0", "--port", "80"]
