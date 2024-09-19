FROM python

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

VOLUME /app/instance

ENV APP_NAME=app \
  HOST=0.0.0.0 \
  PORT=5000

EXPOSE $PORT

CMD gunicorn --bind $HOST:$PORT "$APP_NAME:create_app()"
