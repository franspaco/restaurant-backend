
FROM ubuntu

RUN apt-get update
RUN apt-get install git -y
RUN apt-get install wget -y
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y

RUN pip3 install pymongo
RUN pip3 install flask

RUN cd
RUN wget https://raw.githubusercontent.com/franspaco/restaurant-backend/master/entrypoint.sh
RUN chmod 700 entrypoint.sh

EXPOSE 80
ENTRYPOINT ./entrypoint.sh
 