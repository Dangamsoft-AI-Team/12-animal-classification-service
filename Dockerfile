FROM python:3.8

RUN mkdir /app
COPY ./requirements.txt /app
WORKDIR /app

RUN apt-get update -y
RUN pip install --upgrade pip
RUN pip install --upgrade pillow
RUN apt-get install -y python3-opencv
RUN pip install -r requirements.txt

ENV EUREKA_HOST "172.17.0.7"
EXPOSE 30001
CMD ["python", "app.py"]

# docker build . -t di-12-animal-classification
# [dev]
#   docker run -d -p 30001:30001 -v ~/services/logs:/logs -v ~/services/12-animal-classification-service:/app -e EUREKA_HOST=172.17.0.7 --name di-12-animal-classification-service di-12-animal-classification
# [office]
#   docker run -d -p 30001:30001 -v ~/services/logs:/logs -v ~/services/12-animal-classification-service:/app -e EUREKA_HOST=172.17.0.2 -e SERVER_HOST=192.168.35.61 --name di-12-animal-classification-service di-12-animal-classification
#   docker run -d --network host -v ~/services/logs:/logs -v ~/services/12-animal-classification-service:/app -e EUREKA_HOST=172.17.0.2 -e SERVER_HOST=192.168.35.61 --name di-12-animal-classification-service di-12-animal-classification
