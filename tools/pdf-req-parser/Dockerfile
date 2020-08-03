FROM ubuntu:16.04

RUN apt-get update && apt-get install python python-pip -y
RUN pip install PyPDF2 simplejson

ENTRYPOINT ["python", "main.py"]
COPY . .
