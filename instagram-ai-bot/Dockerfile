FROM python:3.11-slim

WORKDIR /app

COPY requirements_render.txt .
RUN pip install --no-cache-dir -r requirements_render.txt

COPY run_bot.py .

CMD ["python", "run_bot.py"]
