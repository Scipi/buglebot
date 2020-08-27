FROM python:3.8

WORKDIR /bugle_bot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY bugle_bot/ .
COPY bugle_bot.py .

CMD ["python", "./bugle_bot.py"]
