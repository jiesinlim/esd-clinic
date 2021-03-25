#You are at /ESDClinic in the yml file
FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt ./
RUN pip install --no-cache-dir -r http.reqs.txt
COPY nurse_microservice/nurse.py .
CMD [ "python", "match.py" ]