FROM python:3.13

COPY ./requirements.txt ./requirements.txt

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

COPY ./ ./
