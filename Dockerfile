FROM python:3.9.2

ADD requirements.txt project/requirements.txt
ADD app/api/config.txt project/app/api/config.txt
ADD app/api/server.py project/app/api/server.py
ADD app/api/utils.py project/app/api/utils.py
ADD app/api/db/client/client.py project/app/api/db/client/client.py
ADD app/api/db/interaction/interaction.py project/app/api/db/interaction/interaction.py
ADD app/api/db/models/models.py project/app/api/db/models/models.py
ADD app/api/db/exceptions.py project/app/api/db/exceptions.py

RUN pip3.9 install -r /project/requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:/project/app"
WORKDIR /project


EXPOSE 5005

CMD ["python", "./app/api/server.py", "--config ./app/api/config.txt"]