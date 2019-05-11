FROM python:3.7-alpine
COPY . /usr/src/FlaskTemplateSite
#RUN ls -la /usr/src/FlaskTemplateSite/*
WORKDIR /usr/src/FlaskTemplateSite
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
