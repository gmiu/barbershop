FROM python:3.7.3-alpine3.9

RUN adduser -D barbershop

WORKDIR /home/barbershop

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pg8000

COPY app app
COPY migrations migrations
COPY barbershop.py config.py utils.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP barbershop.py

RUN chown -R barbershop:barbershop ./
USER barbershop

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
