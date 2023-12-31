FROM python:latest

WORKDIR /project

COPY requirements.txt /project/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /project/

CMD ["gunicorn", "SocialMedia.wsgi", ":8000"]