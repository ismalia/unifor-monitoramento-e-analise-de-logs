FROM python:3.13-slim

WORKDIR /app

COPY airport_log_generator.py /app/

RUN mkdir -p /app/logs && \
    chmod +x /app/airport_log_generator.py

CMD ["python", "airport_log_generator.py"]
