FROM ubuntu:16.04


RUN mkdir -p /usr/src/team1assignment2
WORKDIR /usr/src/team1assignment2/

RUN apt-get update -y
RUN apt-get install python3 python3-pip -y


COPY final_pipeline.py /usr/src/team1assignment2/
COPY energydata_complete.csv /usr/src/team1assignment2/

#RUN pip3 install jupyter
#RUN pip3 install pandas
#RUN pip3 install boto3
#RUN pip3 install numpy
#RUN pip3 install boto
#RUN pip3 install urllib3
#RUN pip3 install requests
#RUN pip3 install html5lib
#RUN pip3 install bs4
#RUN pip3 install lxml


CMD ["sh","-c","python /usr/src/team1assignment2/final_pipeline.py "] 