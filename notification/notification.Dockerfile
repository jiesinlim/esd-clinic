#You are at /ESDClinic in the yml file
FROM python:3-slim
WORKDIR /usr/src/app
COPY amqp.reqs.txt ./
RUN pip install --no-cache-dir -r amqp.reqs.txt
COPY notification/notification.py notification/amqp_setup.py ./
CMD [ "python", "notification.py" ]