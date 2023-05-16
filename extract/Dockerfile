FROM python:3.11-slim-buster 

ARG CREDENTIALS  
ENV CREDENTIALS=$CREDENTIALS
ENV GOOGLE_APPLICATION_CREDENTIALS=/usr/app/$CREDENTIALS 

COPY ./ /usr/app/
WORKDIR /usr/app
RUN pip install --upgrade pip \
    && pip install requests==2.30.0 \
    && pip install google-cloud-storage==2.9.0 \
    && pip install google-cloud-bigquery==3.10.0 \
    && pip install pandas==2.0.1 \
    && pip install db-dtypes==1.1.1 \
    && pip install google-cloud-secret-manager==2.16.1
ENTRYPOINT ["python", "extract.py"]





