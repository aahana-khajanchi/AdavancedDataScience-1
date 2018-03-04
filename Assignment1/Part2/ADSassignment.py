
# coding: utf-8

# In[1]:


from lxml.html import parse
import numpy as np
from urllib.request import urlopen
import requests,zipfile,io
import pandas as pd
import math
import seaborn as sns
import re
import matplotlib.pyplot as plt
import os
import time
import datetime


# In[2]:


import boto
import boto.s3
import sys
from boto.s3.key import Key
f=0
def uploadToS3(filePath):
    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''

    bucket_name = AWS_ACCESS_KEY_ID.lower()
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)


    bucket = conn.create_bucket(bucket_name,location=boto.s3.connection.Location.DEFAULT)

    testfile = filePath
    print ('Uploading '+testfile+' to Amazon S3 bucket '+bucket_name)
    def percent_cb(complete, total):
        sys.stdout.write('.')
        sys.stdout.flush()

    print('here1')
    k = Key(bucket)
    k.key = "dump/"+testfile
    k.set_contents_from_filename(testfile,cb=percent_cb, num_cb=10)


# In[3]:

summary_metrics = pd.DataFrame(columns=['Date','Total Records','Most Cik',
	                              'Maximum File Size','Average File size','Most used extention','Most used browser'])
def writeLog(line):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S,%f')
    file = open("logfile.txt","a") 
    file.write('['+st+'] '+line+'\n') 
    file.close()


# In[4]:


def writeObs(line):
    ts = time.time()
    file = open("Obsfile.txt","a") 
    file.write(line) 
    file.close()


# In[9]:


y = "2004"
for y in range(2004,2006):
	y = str(y)
	logString = "The Year Input is "+y
	writeLog(logString)



	# In[10]:


	path = './files/'+y


	# In[11]:


	month=1
	for i in range(12):

	    if month in range(1,4):qtr = 1; month = "0"+str(month)
	    elif month in range(4,7):qtr = 2; month = "0"+str(month)
	    elif month in range(7,10): qtr = 3; month = "0"+str(month)
	    elif month in range(10,13): qtr = 4
	    else :pass
	   
	    r = requests.get("http://www.sec.gov/dera/data/Public-EDGAR-log-file-data/"+y+"/Qtr"+str(qtr)+"/log"+y+str(month)+"01.zip")
	    z =zipfile.ZipFile(io.BytesIO(r.content))
	    z.extractall(path)
	  
	    print(y+"/Qtr"+str(qtr)+"/log"+y+str(month)+"01.zip")
	    month = int(month) + 1
	    

	#http://www.sec.gov/dera/data/Public-EDGAR-log-file-data/2003/Qtr2/log20030501.zip


	# In[15]:


	month = 1
	for i in range(12):
	    if month in range(1, 10) :
	        
	        data = pd.read_csv(path+"/log"+y+"0"+str(month)+"01.csv") 
	        print(y+"/Qtr"+str(qtr)+"/log"+y+"0"+str(month)+"01.csv")
	        
	        print(type(data))
	   #     print(data.head())


	        outputname = 'file.txt'      
	        myfile = open(outputname, 'w')
	        myfile.write(str(data.head()))
	        myfile.write(str(data.isnull().sum()))
	        myfile.close()
	       
	        
	        #data.info()
	    
	    elif month in range(10, 13) :
	        data = pd.read_csv(path+"/log"+y+str(month)+"01.csv")      
	        print(y+"/Qtr"+str(qtr)+"/log"+y+str(month)+"01.csv")
	     
	    month = month + 1
	 


	# In[31]:


	outputname = 'file.txt'      
	myfile = open(outputname, 'w')
	myfile.write(str(data.head()))
	myfile.close()


	# In[16]:


	type(data)


	# In[17]:





	# In[18]:


	if month in range(1, 10) :
	    data = pd.read_csv(path+"/log"+y+"0"+str(month)+"01.csv")
	elif month in range(10, 13) :
	    data = pd.read_csv(path+"/log"+y+str(month)+"01.csv")


	# In[19]:


	data.head()


	# In[20]:


	data.isnull().sum()


	# In[21]:


	data.info()


	# In[22]:


	data['extention'] = data['extention'].apply(lambda x: re.findall("\..*", x)[0][1: ])


	# In[23]:


	print(data['extention'])


	# In[24]:


	data['extention'].value_counts()


	# In[25]:


	data.describe(exclude=[np.number])


	# In[26]:


	data['extention'].unique()


	# In[27]:


	data['extention'].max()


	# In[28]:


	data['extention'].min()


	# In[29]:


	data['browser'].unique()


	# In[30]:


	data.head()


	# In[31]:


	data['size'].isnull().sum()


	# # Data Cleaning

	# In[32]:


	# Filling Null data in 'size' by mean value


	# In[33]:


	data['size'].fillna(data['size'].mean(), inplace = True)


	# In[34]:


	data['size'].isnull().any()


	# In[35]:


	data.isnull().sum()


	# In[36]:


	x=data['browser'].value_counts().max()


	# In[37]:


	data['browser'].value_counts()


	# In[38]:


	x=data['browser'].mode()    # most occuring value


	# In[39]:


	data['browser'].fillna(x[0], inplace = True)


	# In[40]:


	x[0]


	# In[41]:


	data['browser'].value_counts()


	# In[42]:


	data.isnull().any()


	# In[43]:


	data['noagent'].value_counts()


	# In[44]:


	data['norefer'].value_counts()


	# In[45]:


	data['idx'].value_counts()


	# In[48]:


	data['browser'].value_counts()


	# ### Browser's max frequency is in win and min in iem

	# In[49]:


	data.describe()


	# In[50]:


	data['cik'].min()


	# In[51]:


	data['cik'].max()


	# In[52]:


	data['extention'].min()


	# In[53]:


	data['extention'].max()


	# ### Observation
	# #### Max cik is 1274986 and min is 20
	# #### Max Extension value is 16 and Min is 

	# ### Summary Metrics

	# In[54]:


	date = data['date'].max()


	# In[55]:


	date # Computing date of the data


	# In[56]:


	tot_record = len(data)


	# In[57]:


	tot_record# computing total number of records


	# In[58]:


	max_c=data['cik'].value_counts() 


	# In[59]:


	max_cik= max_c.max()


	# In[60]:


	max_cik# Max count value of cik


	# In[61]:


	max_size = data['size'].max()# Computing maximum size


	# In[62]:


	max_size


	# In[63]:


	max_size


	# In[64]:


	sum_size = data['size'].sum()


	# In[65]:


	length_size = len(data)


	# In[66]:


	avg_size= sum_size/length_size# computing average of size


	# In[67]:


	avg_size


	# In[68]:


	max_ext = data['extention'].value_counts()


	# In[69]:


	extention_max = data.extention[max_ext.max()]


	# In[70]:


	extention_max #Computing maximum extention used


	# In[71]:


	max_brw = data['browser'].value_counts()


	# In[72]:


	max_brw.max()


	# In[73]:


	brw_max = data.browser[max_brw.max()]


	# In[74]:


	brw_max # Computing most occur browser


	# In[75]:


	row_entry = pd.Series([date, tot_record, max_cik, max_size, avg_size, extention_max, brw_max])


	# In[76]:


	row_entry


	# In[77]:


	# Creating Summary metrics
	


	# In[78]:


	summary_metrics


	# In[79]:


	import csv


	# In[80]:


	courses_list=[]


	# In[81]:

	if(f==0):
		summary_metrics = summary_metrics.append(
		                   pd.Series([date, tot_record, max_cik, max_size, avg_size, extention_max, brw_max],
		                            index=['Date','Total Records','Most Cik',
		                              'Maximum File Size','Average File size','Most used extention','Most used browser'])
		                   ,ignore_index=True)
		f=1
	else:
		summary_metrics = summary_metrics.append(
		                   pd.Series([date, tot_record, max_cik, max_size, avg_size, extention_max, brw_max],
		                            index=['Date','Total Records','Most Cik',
		                              'Maximum File Size','Average File size','Most used extention','Most used browser'])
		                   ,ignore_index=True)
		f=1



summary_metrics.to_csv("./file_name.csv",mode='a', sep='\t', encoding='utf-8')

