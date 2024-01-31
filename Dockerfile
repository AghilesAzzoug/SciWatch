FROM python:3.10

WORKDIR /usr/src/sci_watch

COPY . .

RUN pip install poetry==1.6.1

RUN make install-dev

RUN make reports

# TODO: configure crontab

ENTRYPOINT ["python", "main.py"]