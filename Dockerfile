FROM python:3.7-alpine

RUN mkdir /app
WORKDIR /app
COPY rest_app.py requirements.txt db_connector.py /app/
RUN pip install -r requirements.txt
RUN chmod 644 rest_app.py

EXPOSE 5000
CMD ["python3", "/app/rest_app.py"]
