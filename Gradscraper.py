import pandas as pd
from bs4 import BeautifulSoup
import requests
import time

#testchangegit
#idk what i am doing
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "gradscraper@gmail.com"
receiver_email = "michaelorawe@btinternet.com"
#password = input("What is the password?")#gradscraper33
password = "gradscraper33"
email_text = ''
joblist=[]
def job_search():
    global joblist
    html_text = requests.get("https://www.gradcracker.com/search/electronic-electrical/engineering-work-placements-internships?order=dateAdded&duration=Summer").text
    soup = BeautifulSoup(html_text,'lxml')
    jobs = soup.find_all('div',class_='tw-relative tw-mb-4 tw-border-2 tw-border-gray-200 tw-rounded')
    print(f"There are {len(jobs)} jobs available")
    for index,job in enumerate(jobs):
        #print(len(jobs))
        company=job.find('img')['alt']
        title=job.find('a',class_='tw-block tw-text-base tw-font-semibold').text.replace('				','').replace('\n','')
        link = job.find('a')['href']

        item = job.find_all('li',class_='tw-text-xs tw-font-semibold')
        info = []
        for individual in item:
            info.append(individual.text)

        salary=info[0]
        location=info[1]
        length = info[-2]
        deadline=info[-1].split(':',1)[1]


        #print(f'''
           #Company Name:   {company}
           #Title:          {title}
           #Location/s:     {location}
           #Length:         {length}
           #Deadline:      {deadline}
           #Link:           {link}
        #''')

        joblist.append([company,title,salary,location,length,deadline,link])
        #print(joblist)

    job_list=pd.DataFrame(joblist)
    job_list.set_axis(['Company','Title','Salary','Location','Length','Deadline','Link'],axis=1,inplace=True)
    job_list.to_csv('joblist.csv')
    comparison = pd.read_csv('ComparisonFile.csv')
    new_jobs = pd.merge(job_list,comparison,on=['Company','Title','Salary','Location','Length','Deadline','Link'],how="outer",indicator=True).query('_merge=="left_only"')
    new_jobs.to_csv('new_jobs.csv')
    comparison=job_list

if __name__ ==  '__main__':
    while(True):
        job_search()
        time.sleep(60)
        
