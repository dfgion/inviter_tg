FROM python:3.11-slim

WORKDIR /bot

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

ENV BOT_TOKEN=6976926882:AAG2l5K2dcc8MpICsUrYrU_1na-2i_95V-Q
ENV DATABASE_DSN=postgresql+asyncpg://postgres:jwt123@inviter_postgres/inviter_db

CMD ["python", "main.py"]