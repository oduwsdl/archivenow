FROM python:3.6
MAINTAINER Mohamed Aturban <mohsci1@yahoo.com>

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./archivenow/archivenow.py .
COPY ./archivenow/__init__.py .
ADD ./archivenow/handlers/* ./handlers/  
ENTRYPOINT ["python3", "archivenow.py"]

