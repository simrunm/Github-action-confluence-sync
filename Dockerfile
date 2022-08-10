FROM python:3.9-alpine

WORKDIR /tmp
COPY ./requirements.txt ./
RUN pip install --upgrade -r requirements.txt
WORKDIR /action
COPY ./src .

ENTRYPOINT [ "python" ]
CMD [ "/action/main.py" ]
