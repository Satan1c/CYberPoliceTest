FROM python:3.12.7

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["celery", "-A", "CyberPoliceTest", "worker", "--loglevel=info"]