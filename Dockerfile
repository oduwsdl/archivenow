FROM python:3
LABEL maintainer "Mohamed Aturban <mohsci1@yahoo.com>"

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./
RUN chmod a+x ./archivenow/archivenow.py

ENTRYPOINT ["./archivenow/archivenow.py"]
