FROM python:3.7

LABEL maintainer="Askin Ozgur <askin@askin.ws>"

RUN pip install jinja2
RUN apt-get update
RUN apt-get install dnsutils -y
RUN apt-get autoclean
RUN rm -rf /var/lib/apt/lists

WORKDIR /app

COPY main.py /app
COPY hermes_notify.py /app
COPY layout.html /app
COPY config.ini /app

CMD ["python", "main.py"]
