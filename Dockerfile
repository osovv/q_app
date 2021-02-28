FROM python:3.9.2

ADD requirements.txt project/requirements.txt
ADD app/api/config.txt project/app/api/config.txt
ADD app/api/server.py project/app/api/server.py
ADD app/api/utils.py project/app/api/utils.py
ADD app/db/client/client.py project/app/db/client/client.py
ADD app/db/interaction/interaction.py project/app/db/interaction/interaction.py
ADD app/db/models/models.py project/app/db/models/models.py
ADD app/db/exceptions.py project/app/db/exceptions.py

RUN pip3.9 install -r /project/requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:/project/app"
WORKDIR /project


EXPOSE 5005

CMD ["python", "./app/api/server.py", "--config=./app/api/config.txt"]