FROM python:3.11.4

ADD main.py .

RUN pip3 install Flask requests

EXPOSE 5000


CMD ["python", "./main.py"]