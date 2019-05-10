FROM python:3

WORKDIR /parser

COPY . . 

RUN pip install -r requirements.txt

ENV PYTHONPATH="$PYTHONPATH:/parser"
ENV DATABASE_URL="postgresql://danberd@host.docker.internal/parser"
ENV CHROME_REMOTE_URL="http://host.docker.internal:4444/wd/hub"

RUN alembic upgrade head

CMD ["python", "src/main.py"]