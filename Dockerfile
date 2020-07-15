FROM python:3.6
ENV PYTHONUNBUFFERED=1
RUN mkdir /performance
WORKDIR /performance
COPY Pipfile /performance
RUN pip3 install pipenv && pipenv install
COPY . /performance

