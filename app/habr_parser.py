import requests
from lxml import html
import json
import psycopg2
from psycopg2 import sql
from models import *

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}

response = requests.get('https://career.habr.com/resumes', headers=headers)

tree = html.fromstring(response.content)

resumes_json = tree.xpath('//script[@type="application/json"]/text()')[0]
if resumes_json:
    resumes_json = json.loads(str(resumes_json))


resumes = resumes_json.get('resumes', {}).get('list', [])

results = []

for resume in resumes:
    resume_id = resume.get('id')
    href = f"https://career.habr.com{resume.get('href')}"
    salary = resume.get('salary')
    if salary:
        salary = resume.get('salary', {}).get('value')
    results.append(
        {'resume_id': resume_id ,
         'href': href,
         'salary': salary
         })

connection = psycopg2.connect(host='db',
                             port='5432',
                             dbname='resumes_db',
                             user='postgres',
                             password='postgres')

for result in results:
    item = MainData(resume_id=result.get('resume_id'),
                     url=result.get('href'),
                     salary=result.get('salary'),
                     )
    try:
        curscor = connection.cursor()
        insert_resume = sql.SQL("INSERT INTO main_data (resume_id, url, salary) VALUES (%s,%s,%s)")

        curscor.execute(insert_resume, (item.resume_id, item.url, item.salary))

        connection.commit()
    except Exception as err:
        print(err)
        connection.rollback()

connection.close()
