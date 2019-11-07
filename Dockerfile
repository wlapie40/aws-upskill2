FROM python:3.6

COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3"]

CMD ["app.py"]