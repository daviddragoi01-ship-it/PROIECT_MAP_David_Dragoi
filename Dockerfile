FROM python:3.10-slim
WORKDIR /app
COPY word_analyzer.py .
ENTRYPOINT ["python", "word_analyzer.py"]