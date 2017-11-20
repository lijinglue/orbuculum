FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install -r /app/requirements.txt
ENTRYPOINT ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
