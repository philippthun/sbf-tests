FROM python:3.10

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY sbf sbf
COPY app.py .
COPY sidecar.sh .
COPY task.sh .

CMD ["python", "app.py"]
EXPOSE 8080
