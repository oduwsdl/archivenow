FROM python:3-onbuild
LABEL maintainer "Mohamed Aturban <mohsci1@yahoo.com>"

ENTRYPOINT ["python", "./archivenow/archivenow.py"]
