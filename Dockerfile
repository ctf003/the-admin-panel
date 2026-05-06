FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

RUN useradd -m -u 1001 ctfuser && chown -R ctfuser:ctfuser /app

USER ctfuser

ENV FLAG=""

EXPOSE 5000

CMD ["./entrypoint.sh"]
