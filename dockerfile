FROM python:3.8
WORKDIR /app
COPY . /app
RUN pip install Flask pyjwt
CMD ["python", "main.py"]