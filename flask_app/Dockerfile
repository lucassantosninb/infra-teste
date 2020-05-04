FROM python:2.7

EXPOSE 5000

COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "app.py" ]