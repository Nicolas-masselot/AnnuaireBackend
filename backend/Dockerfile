FROM python:latest
COPY . /backend
WORKDIR /backend
RUN pip install -r requirements.txt
EXPOSE 5001
ENTRYPOINT [ "python" ]
CMD [ "main.py" ]