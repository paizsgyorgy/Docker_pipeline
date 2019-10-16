# Dockerfile

FROM python:3.6-slim

WORKDIR /app

COPY requirements.txt /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt


#--- Everything above happens when building the image ---

CMD ["python", "etl.py"]
