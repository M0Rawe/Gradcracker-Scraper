import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import smtplib
import ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "gradscraper@gmail.com"
receiver_email = "michaelorawe@btinternet.com"
# password = input("What is the password?")#gradscraper33
password = "gradscraper33"
joblist = []
comparison = pd.read_csv('ComparisonFile.csv')
flag = True
time_spent = 0

while (True):

    html_text = requests.get(
        "https://www.gradcracker.com/search/electronic-electrical/engineering-work-placements-internships?order=dateAdded&duration=Summer").text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('div', class_='tw-relative tw-mb-4 tw-border-2 tw-border-gray-200 tw-rounded')

    for index, job in enumerate(jobs):

        company = job.find('img')['alt']
        title = job.find('a', class_='tw-block tw-text-base tw-font-semibold').text.replace('				',
                                                                                            '').replace('\n', '')
        link = job.find('a')['href']

        item = job.find_all('li', class_='tw-text-xs tw-font-semibold')
        info = []

        for individual in item:
            info.append(individual.text)

        salary = info[0]
        location = info[1]
        length = info[-2]
        deadline = info[-1].split(':', 1)[1]

        if flag:
            joblist.append([company, title, salary, location, length, deadline, link])

    flag = False
    job_list = pd.DataFrame(joblist)
    job_list.set_axis(['Company', 'Title', 'Salary', 'Location', 'Length', 'Deadline', 'Link'], axis=1, inplace=True)
    job_list.to_csv('joblist.csv')
    new_jobs = pd.merge(job_list, comparison,
                        on=['Company', 'Title', 'Salary', 'Location', 'Length', 'Deadline', 'Link'], how="outer",
                        indicator=True).query('_merge=="left_only"')
    if not new_jobs.empty:
        new_jobs = new_jobs.drop(new_jobs.index[0])
    new_jobs.to_csv('new_jobs.csv')
    comparison = job_list
    comparison.to_csv("ComparisonFile.csv")

    for index, row in new_jobs.iterrows():
        new_company, new_title, new_salary, new_location, new_length, new_deadline, new_link = row['Company'], row[
            'Title'], row['Salary'], row['Location'], row['Length'], row['Deadline'], row['Link']
        message = (f'''
        Company Name:   {new_company}
        Title:          {new_title}
        Salary:         {new_salary}
        Location/s:     {new_location}
        Length:         {new_length}
        Deadline:       {new_deadline}
        Link:           {new_link}
        ''')
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.encode("utf8"))
    print(f"Time spent searching is {time_spent} seconds")
    print(f"There are {len(new_jobs.index)} new jobs found!")
    print()
    time_spent+=30
    time.sleep(30)

   
