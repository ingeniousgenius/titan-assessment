FROM python:3.9.2-alpine

RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev
RUN apk add curl

RUN adduser -D nonroot
RUN mkdir /home/app/ && chown -R nonroot:nonroot /home/app
RUN mkdir -p /var/log/flask-app && touch /var/log/flask-app/flask-app.err.log && touch /var/log/flask-app/flask-app.out.log
RUN chown -R nonroot:nonroot /var/log/flask-app
WORKDIR /home/app
USER nonroot

COPY --chown=nonroot:nonroot . .

ENV VIRTUAL_ENV=/home/app/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONPATH=/home/app:$PYTHONPATH
ENV FLASK_APP=app.py

RUN $VIRTUAL_ENV/bin/pip install --upgrade pip
RUN $VIRTUAL_ENV/bin/pip install --no-cache-dir -r requirements.txt
EXPOSE 3025

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=3025"]