FROM python:latest
COPY . /authentification
WORKDIR /authentification
RUN pip install -r requirements.txt
EXPOSE 6001
ENTRYPOINT [ "python" ]
CMD [ "main.py" ]