from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import smtplib
import ssl
from email.mime.text import MIMEText

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "gradscraper@gmail.com"
receiver_email = "michaelorawe@btinternet.com"
#password = input("What is the password?")#gradscraper33
password = "gradscraper33"
email_text = ''

def job_search():
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

        with open(f'Job files/{index}.txt','w') as f:
            f.write(f'Company Name:   {company}')
            f.write(f'Title:          {title}')
            f.write(f'Location/s:     {location}')
            f.write(f'Length:         {length}')
            f.write(f'Deadline:      {deadline}')
            f.write(f'Link:           {link}')

        print(f'''
           Company Name:   {company}
           Title:          {title}
           Location/s:     {location}
           Length:         {length}
           Deadline:      {deadline}
           Link:           {link}
        ''')


if __name__ ==  '__main__':
    while True:
        job_search()
        time.
