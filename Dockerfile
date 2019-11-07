FROM python:3.7
EXPOSE 5000
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
ENV FLASK_ENV='development'
CMD python app.py --host=0.0.0.0 --port=5000