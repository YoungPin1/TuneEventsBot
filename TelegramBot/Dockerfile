FROM python:3.12

RUN mkdir /app
WORKDIR /app


COPY app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY .. .

ENV PYTHONPATH=/app

EXPOSE 8000:8000

CMD ["python", "app/main.py"]
