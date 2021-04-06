#You are at /ESDClinic in the yml file
FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt ./
RUN pip install --no-cache-dir -r http.reqs.txt
COPY notify_patient/notify-patient.py notify_patient/invokes.py ./
CMD [ "python", "notify-patient.py" ]