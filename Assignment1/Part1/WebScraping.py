
# coding: utf-8

# In[1]:


import bs4
import urllib.parse
import csv
import lxml
import re
import os
import logging
import time
import datetime
import zipfile
import boto
import boto.s3
import sys


# In[2]:


from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as soup
from lxml import html, etree
from boto.s3.key import Key


# In[43]:


def uploadToS3(destinationPath,filePath,ACCESS_KEY_ID,SECRET_ACCESS_KEY):
    AWS_ACCESS_KEY_ID = ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = SECRET_ACCESS_KEY

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
    k.key = destinationPath+"/"+testfile
    
    k.set_contents_from_filename(testfile,cb=percent_cb, num_cb=10)


# In[36]:


def zip_dir(path_dir, path_file_zip=''):
    print("ZIP process started")
    if not path_file_zip:
        path_file_zip = os.path.join(
            os.path.dirname(path_dir), os.path.basename(path_dir) + '.zip')
    with zipfile.ZipFile(path_file_zip, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(path_dir):
            for file_or_dir in files + dirs:
                zip_file.write(
                    os.path.join(root, file_or_dir),
                    os.path.relpath(os.path.join(root, file_or_dir),
                                    os.path.join(path_dir, os.path.pardir)))
    print("ZIP process Ended")


# In[5]:


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


# In[6]:


def checktag(param):
    flag = "false"
    datatabletags = ["background", "bgcolor", "background-color"]
    for x in datatabletags:
        if x in param:
            flag = "true"
    return flag


# ## Fetching the 10Q link

# In[7]:

def main():
   
    base_url = 'https://www.sec.gov'
    cik = sys.argv[1]
    acc_num = sys.argv[2]
    acc_num_index = acc_num[0:10]+"-"+acc_num[10:12]+"-"+acc_num[12:]+"-index.html"
    url_rendered = base_url + "/Archives/edgar/data/" + cik + "/" + acc_num +"/" + acc_num_index
    form_url = base_url + "/" + cik + "/" + acc_num
    print(url_rendered)


    # ## Fetching tables

    # In[8]:


    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S')
    logfilename = 'log_Edgar_'+ cik + '_' + st + '.txt' 
    logging.basicConfig(filename=logfilename, level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')
    logging.debug('Program Start')
    logging.debug('CIK Number : '+cik+'  and Accession number : '+acc_num+ '  Url :'+ url_rendered)


    # In[9]:


    uCLient = ureq(url_rendered)
    page_html=uCLient.read()


    # In[10]:


    page_soup = soup(page_html, 'html.parser')
    divs = page_soup.find('table',summary="Document Format Files")
    url2=divs.find_all('tr')[1].find_all('td')[2].find('a')['href']


    # In[11]:


    my_url2=urllib.parse.urljoin(base_url, url2)
    my_url2


    # In[12]:


    uCLient2 = ureq(my_url2)
    page_html2=uCLient2.read()
    page_soup2 = soup(page_html2, 'html.parser')


    # In[13]:


    link_list=[]
    link_text=[]

    for link in page_soup2.find_all('a'):
        href_link=link.get('href')
        href_text=link.get_text()
        if href_link is not None:
            href_link=str(href_link).strip('#')
            is_Exists = page_soup2.find("a",{'name':href_link})
            if (is_Exists is not None):
                link_list.append(href_link)
                link_text.append(href_text)
    logging.debug('List of all Href tags : '+str(link_list))


    # In[53]:


    path2 = ""
    for item in range(0, (len(link_list)-1)):
        next2 = item + 1
        item1=link_list[item]
        item2=link_list[next2]
        first = '<a name="' + item1 +'">'
        last = '<a name="' + item2 +'">'
        print("elements",first,last)
        new_soup = find_between( page_soup2.prettify(), first, last )
        new_bs = soup(new_soup, 'html.parser')
        tables = new_bs.find_all("table")
        if(len(tables)>0):    
            table_all_rows=[]
            for table in tables:
                table_row = table.select('tr')
                tds = table.select('td')
                flag=0
                for td in tds:
                    if checktag(str(td.get('style'))) == "true" or checktag(str(td)) == "true":
                        flag=1
                        break
                for tr in table_row:
                    if(flag==1):
                        table_column = tr.select('font')
                        row = []
                        for k in table_column:
                            k_text = k.text.replace(u'\xa0',u'')
                            k_text = k_text.replace(u'\n',u'')
                            if(k_text!='\n' ):
                                row.append(k_text)
                        table_all_rows.append(row)
                if(flag==1):
                    dirname = './files/'+cik+ '/'+acc_num+'/'
                    path = './files/'+cik
                    path2 = 'files/'+cik+'.zip'
                    if not os.path.exists(dirname):
                        os.makedirs(dirname)
                    try:
                       # path=dirname+item1
                        with open((dirname+item1+'.csv'),"a",newline='') as my_csv:
                            csvWriter = csv.writer(my_csv,delimiter=',')
                            try:
                                csvWriter.writerows(table_all_rows) 
                            except:
                                print("no")
                    except:
                        print("file open error")
                        logging.error('file open error')
    zip_dir(path)
    print(path2)
    uploadToS3("Part1",path2,sys.argv[3],sys.argv[4])
    time.sleep(5)
    print("yaayyy"+logfilename)
    uploadToS3("Part1",logfilename,sys.argv[3],sys.argv[4])


    # In[ ]:


    logging.debug('End of Program')

if __name__ == '__main__':
    main()