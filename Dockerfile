FROM python:3.9-alpine

WORKDIR /tmp
# RUN pip-compile -v requirements.in
COPY ./requirements.txt ./
RUN pip install --upgrade -r requirements.txt
# RUN pip install pipenv

# RUN pipenv lock
# RUN pipenv install --system --deploy
# RUN pip install atlassian-python-api
# RUN pip install beautifulsoup4
WORKDIR /action
COPY ./src .

ENTRYPOINT [ "python" ]
CMD [ "/action/main.py" ]
