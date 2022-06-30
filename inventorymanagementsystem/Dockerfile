FROM python:3.10

EXPOSE 8000

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

#CMD ["python", "./manage.py", "runserver"]

COPY ./entrypoint.sh /

ENTRYPOINT ["sh", "/entrypoint.sh"]





