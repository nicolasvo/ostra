FROM python:3.7-alpine

WORKDIR /home

COPY . .

ENV PORT 5000

RUN pip install pipenv
RUN pipenv install --system

ENTRYPOINT ["/bin/sh"]
CMD ["run.sh"]
