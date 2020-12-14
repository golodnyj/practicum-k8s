FROM python:3.7-slim-buster

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG COLOR_SCHEME=light
ENV COLOR_SCHEME "$COLOR_SCHEME"
CMD ["python", "./app.py"]
