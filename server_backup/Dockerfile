FROM python:3.13

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install  -r requirements.txt

COPY . .
#RUN cd app
# RUN alembic upgrade head

RUN pip freeze > requirements.txt
EXPOSE 8000

CMD ["/bin/bash","./startup.sh"]
