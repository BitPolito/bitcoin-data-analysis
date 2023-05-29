FROM python:3.10-slim
RUN apt-get update
RUN apt-get install -y curl python3-dev autoconf 
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false
RUN poetry install  --no-dev --no-root

COPY . .
EXPOSE 8501

CMD ["poetry", "run", "streamlit", "run", "dashboard/On-chain.py"]