FROM python:3.9
COPY ./ workflow_backend
WORKDIR /workflow_backend
RUN pip install -r requirements.txt