FROM python:3.8

LABEL maintainer="Farid Ahmadian <farid.ahmadian@bonial.com>"

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "main.py"]
