FROM python:3.8

LABEL maintainer="Farid Ahmadian <farid.ahmadian@bonial.com>"

WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt

CMD ["python", "main.py"]