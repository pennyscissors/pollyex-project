FROM python:3.7

WORKDIR /api

COPY ./api /api

COPY ./requirements.txt ./

RUN pip --no-cache-dir install -r requirements.txt

CMD [ "python", "main.py" ]
