FROM ubuntu:16.04


RUN mkdir -p /usr/src/team1assignment2
WORKDIR /usr/src/team1assignment2

RUN apt-get update -y
RUN apt-get install python3 python3-pip -y


COPY EDA.ipynb /usr/src/team1assignment2/EDA.ipynb
COPY Assignment2-EDA-clean.ipynb /usr/src/team1assignment2/Assignment2-EDA-clean.ipynb
COPY Dataset/. /usr/src/team1assignment2/Dataset
RUN pip3 install jupyter
RUN pip3 install folium
RUN pip3 install pivottablejs
RUN pip3 install pandas
RUN pip3 install matplotlib
RUN pip3 install seaborn
RUN pip3 install plotly
RUN pip3 install missingno
RUN pip3 install pandas_profiling
RUN pip3 install mpld3
RUN pip3 install sklearn
RUN pip3 install pandas-profiling

#ENV ck 1
#ENV ac 1
#ENV akey 1
#ENV skey 1
#ENV sl 1

CMD jupyter notebook --ip=0.0.0.0 --no-browser --allow-root
#CMD ["sh","-c","python /usr/src/team5assignment1/Research_paper_1.py --cik ${ck} --acn ${ac} --akey ${akey} --skey ${skey} --s3loc ${sl}"] 