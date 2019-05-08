FROM python:3

WORKDIR /parser

COPY . . 

RUN pip install -r requirements.txt

ENV PYTHONPATH="$PYTHONPATH:/parser"
ENV DATABASE_URL="postgresql://localhost/parser"
