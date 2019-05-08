FROM python:3

WORKDIR /parser

COPY . . 

RUN pip install -r requirements.txt

ENV PYTHONPATH="$PYTHONPATH:/parser"
ENV DATABASE_URL="postgresql://localhost/parser"
ENV CHROME_REMOTE_URL="http://127.0.0.1:4444/wd/hub"
