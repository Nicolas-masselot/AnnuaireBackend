FROM python:latest
COPY . /administration
WORKDIR /administration
RUN pip install -r requirements.txt
EXPOSE 7001
ENTRYPOINT [ "python" ]
CMD [ "main.py" ]