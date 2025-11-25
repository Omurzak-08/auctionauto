FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /auto_app

COPY req.txt /auto_app/
RUN pip install --upgrade pip && \
    pip install -r req.txt

COPY nginx/nginx.conf /etc/nginx/conf.d/

COPY . /auto_app/