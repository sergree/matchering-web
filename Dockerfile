FROM python:3-slim

RUN apt update && apt -y install libsndfile1 ffmpeg redis-server supervisor

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["./init.sh"]
