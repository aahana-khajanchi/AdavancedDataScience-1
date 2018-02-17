
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
#For logs
import time
import datetime
get_ipython().run_line_magic('matplotlib', 'inline')


# In[6]:


import boto
import boto.s3
import sys
from boto.s3.key import Key

def uploadToS3(filePath):
    AWS_ACCESS_KEY_ID = 'AKIAJ7NCU2JC2YSJNKYA'
    AWS_SECRET_ACCESS_KEY = '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'

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


# In[5]:


def writeLog(line):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S,%f')
    file = open("logfile.txt","a") 
    file.write('['+st+'] '+line+'\n') 
    file.close()


# In[3]:


y = input("Enter the year")

logString = "The Year Input is "+y
writeLog(logString)


# In[27]:


path = './files/'+y


# In[28]:


month=1
path = './files/'+y
for i in range(12):
    if month in range(1,4):qtr = 1; month = "0"+str(month)
    elif month in range(4,7):qtr = 2; month = "0"+str(month)
    elif month in range(7,10): qtr = 3; month = "0"+str(month)
    elif month in range(10,13): qtr = 4
    else :pass
    r = requests.get("http://www.sec.gov/dera/data/Public-EDGAR-log-file-data/"+y+"/Qtr"+str(qtr)+"/log"+y+str(month)+"01.zip")
    z =zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(path)
    month = int(month) + 1
    print(y+"/Qtr"+str(qtr)+"/log"+y+str(month)+"01.zip")


# In[30]:


data = pd.read_csv(path+"/log20040101.csv")


# In[31]:


data.head()


# In[32]:


data.info()


# In[33]:


data.describe()


# In[34]:


data.info()


# In[35]:


data.isnull().sum()


# In[37]:


data['extention'] = data['extention'].apply(lambda x: re.findall("\..*", x)[0][1:])


# In[38]:


print(data['extention'])


# In[14]:


data.describe(exclude=[np.number])


# In[15]:


data['extention'].unique()


# In[16]:


sns.countplot(data['extention'])


# In[17]:


data['browser'].unique()


# In[18]:


sns.countplot(data['browser'])


# In[20]:


sns.boxplot(x='extention', y='size', data=data);


# In[21]:


sns.countplot(data['crawler'])


# In[23]:


sns.countplot(data['code'])


# In[24]:


sns.boxplot(data = data['size'])


# In[ ]:


data['time'].hist(bins=1000)


# # Data Cleaning

# In[ ]:


# Filling Null data in 'size' by mean value


# In[ ]:


data['size'].fillna(data['size'].mean(), inplace = True)


# In[ ]:


data['size'].isnull().any()


# In[ ]:


data.isnull().sum()


# In[ ]:


x=data['browser'].value_counts().max()


# In[ ]:


data['browser'].value_counts()


# In[ ]:


x=data['browser'].mode()


# In[ ]:


#most_occuring = x[0]


# In[ ]:


#most_occuring


# In[ ]:


data['browser'].fillna(x[0], inplace = True)


# In[ ]:


x[0]


# In[ ]:


data['browser'].value_counts()


# In[ ]:


# Encoding categorical data

from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder = LabelEncoder()
for i in ['ip','date','time','accession','extention','browser']:
    data[i] = labelencoder.fit_transform(data[i])
data.head()


# In[ ]:


# matplotlib.figure.Figure(figsize= (w,h)) tuple in inches

from matplotlib import pyplot as plt
plt.figure(figsize=(10,5))


# seaborn.countplot - Show the counts of observations in each categorical bin using bars.
# A count plot can be thought of as a histogram across a categorical, instead of quantitative, variable

sns.countplot(data['browser'])
plt.xticks(rotation = 'vertical')
#plt.title('Manufacturers distribution in dataset')
#plt.ylabel('Number of vehicles')
plt.show()


# In[ ]:


# matplotlib.figure.Figure(figsize= (w,h)) tuple in inches

from matplotlib import pyplot as plt
plt.figure(figsize=(10,5))


# seaborn.countplot - Show the counts of observations in each categorical bin using bars.
# A count plot can be thought of as a histogram across a categorical, instead of quantitative, variable

sns.countplot(data['browser'])
plt.xticks(rotation = 'vertical')
#plt.title('Manufacturers distribution in dataset')
#plt.ylabel('Number of vehicles')
plt.show()


# In[ ]:


data1 = pd.read_csv("log20040201.csv")


# In[ ]:


data1.head()


# In[ ]:


data1.isnull().sum()


# In[ ]:


data1['size'].fillna(data['size'].mean(), inplace = True)


# In[ ]:


data1.head()


# In[ ]:


data1.isnull().sum()


# In[ ]:


data1['browser'].value_counts()


# In[ ]:


x=data1['browser'].mode()


# In[ ]:


x[0]


# In[ ]:


data1['browser'].fillna(x[0], inplace = True)


# In[ ]:


data1.isnull().sum()


# In[ ]:


# matplotlib.figure.Figure(figsize= (w,h)) tuple in inches

from matplotlib import pyplot as plt
plt.figure(figsize=(10,5))


# seaborn.countplot - Show the counts of observations in each categorical bin using bars.
# A count plot can be thought of as a histogram across a categorical, instead of quantitative, variable

sns.countplot(data['browser'])
plt.xticks(rotation = 'vertical')
#plt.title('Manufacturers distribution in dataset')
#plt.ylabel('Number of vehicles')
plt.show()


# In[ ]:


# matplotlib.figure.Figure(figsize= (w,h)) tuple in inches

from matplotlib import pyplot as plt
plt.figure(figsize=(10,5))


# seaborn.countplot - Show the counts of observations in each categorical bin using bars.
# A count plot can be thought of as a histogram across a categorical, instead of quantitative, variable

sns.countplot(data1['browser'])
plt.xticks(rotation = 'vertical')
#plt.title('Manufacturers distribution in dataset')
#plt.ylabel('Number of vehicles')
plt.show()


# In[ ]:


# matplotlib.figure.Figure(figsize= (w,h)) tuple in inches

from matplotlib import pyplot as plt
plt.figure(figsize=(10,5))


# seaborn.countplot - Show the counts of observations in each categorical bin using bars.
# A count plot can be thought of as a histogram across a categorical, instead of quantitative, variable

sns.countplot(data['size'])
plt.xticks(rotation = 'vertical')
#plt.title('Manufacturers distribution in dataset')
#plt.ylabel('Number of vehicles')
plt.show()


# ### Correlation Analysis

# In[ ]:


import seaborn as sns
correlation = data.corr()
sns.set_context("notebook", font_scale = 1.0, rc = {"lines.linewidth" : 2.5})
plt.figure(figsize=(13, 7))
a = sns.heatmap(correlation,annot = True, fmt = '.2f')

rotx = a.set_xticklabels(a.get_xticklabels(), rotation=90)
roty = a.set_yticklabels(a.get_yticklabels(), rotation=30)

