FROM python:3.9-alpine

LABEL maintainer="Farid Ahmadian <farid.ahmadian@bonial.com>"

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["python", "main.py"]
