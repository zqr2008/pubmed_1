import requests
import re
import csv
rows=['article_name']
date_rows=['the_date']
key=input("请输入你想查找的信息：")
local_url=input("请输入你想存储的名称：")
turl="https://pubmed.ncbi.nlm.nih.gov/"
tdata=requests.get(turl,params={"term":key}).text
pat_allpage='<span class="total-pages">(.*?)</span>'
allpage=re.compile(pat_allpage,re.S).findall(tdata)
num=input("请输入大致想获取的文章数目（总数为"+str(int(allpage[0].replace('\n        ','').replace(',',''))*10)+"):")
for j in range(0,int(num)//10+1):
    url="https://pubmed.ncbi.nlm.nih.gov/"+"?term="+key+"&page="+str(j+1)
    data=requests.get(url,params={"term":key}).text
    pat1_content_url='<div class="docsum-wrap">.*?<.*?href="(.*?)".*?</a>'
    content_url=re.compile(pat1_content_url,re.S).findall(data)
    hd={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400'}
    for i in range(0,len(content_url)):
        curl="https://pubmed.ncbi.nlm.nih.gov/"+content_url[i]
        try:
            cdata=requests.get(curl,headers=hd).text
            pat2_title="<title>(.*?)</title>"
            pat3_content='<div class="abstract-content selected".*?>(.*?)</div>'
            pat4_date='<span class="cit">(.*?)</span>'
            title=re.compile(pat2_title,re.S).findall(cdata)
            print("正则爬取的题目是："+title[0])
            rows.append(title[0])           
            content=re.compile(pat3_content,re.S).findall(cdata)
            date=re.compile(pat4_date,re.S).findall(cdata)
            date_rows.append(date[0])  
            fh=open(local_url+".xlsx","a",encoding="utf-8")
            fh.write(str(title[0])+' ----'+str(date[0])+"<br />"+str(content[0])+"<br /><br />") 
            fh.close
        except Exception as err:
            pass
        if int(num) < 10:
            if i+1 == int(num):
                break
        elif int(num) == 10:
            if i == 9:
                break
        elif (j*10)+i+1 == int(num):
            break

with open('trial.csv','w',encoding='utf-8',newline='') as file:          
    writer = csv.writer(file) 
    for i in range(len(rows)-1):
        writer.writerow([rows[i],date_rows[i]]) 
