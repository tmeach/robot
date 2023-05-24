import requests
import json
from datetime import timedelta, date 
import datetime
import logging

from jinja2 import Template 
from jinja2 import Environment, FileSystemLoader, select_autpescape

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from config.py import SENDER_EMAIL, EMAIL_PASSWORD



logging.basicConfig(filename = 'robots_logs.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(funcName)s || %(message)s')


def get_week(day=None):
    if day == None:
        start_date = date.today()
    else:
        start_date = datetime.datetime.strptime(day, "%d.%m.%Y")

    end_date = start_date - timedelta(weeks=1)
    date_range = f"{end_date.strftime('%d.%m.%Y')}-{start_date.strftime('%d.%m.%Y')}"
    return date_range


def get_contracts(**kwargs):
    url= f'http://openapi.clearspending.ru/restapi/v3/contracts/search/'
    params = {**kwargs}
    logging.info('The function get_contracts is started ' + url, params)
    
    try:
        req = requests.get(url, params)
        logging.info(req)
    except Exception as e:
        logging.error('Links error')
        logging.exception(e)
    
    try:
        data = req.json()
        logging.info(data)
        return data
    except Exception as e:
        logging.error('Error change to JSON')
        logging.exception(e)


result = get_contracts(daterange=get_week())
print(result)


try: 
    with open('result.json', 'w') as json_file:
        json.dump(result, json_file)
    logging.info('result.json ' + 'is saved')
except Exception as e: 
    logging.error('result.json ' + 'is not saved')
    logging.exception(e)

def get_top_contracts(json_data):

data = json_data['contracts']['data']

top_contracts = []


for contracts in data: 
    contract_dict = {}
    contract_url = recurs_find_key('contractUrl', contract)
    contract_dict['contract_url'] = contract_url
    
    sign_date = recurs_find_key('signDate', contract)
    contract_dict['sign_date'] = sign_date

    num_reg = recurs_find_key('regNum', contract)
    contract_dict['num_reg'] = num_reg

    price = recurs_find_key('price', contract)
    contract_dict['price'] = price

    region_code = recurs_find_key('regionCode', contract)
    contract_dict['region_code'] = region_code

    customer = recurs_find_key('customer', contract)
    customer_inn = recurst_
    asdas

    customer_name = recurs_find_key('fullName', customer)
    contract_dict['customer_name'] = customer_name

    suppliers = recurs_find_key('supliers', contract)
    suppliers_dict = {}
    if suppliers != None:
        for supplier in supliers:

            supplier_inn = recurs_find_key('inn', supplier)
            supplier_name = recurs_find_key('organizationName', supplier)
            supplier_dict[supplier_inn] = supplier_name
            suppliers_data = '\n'.join([f"{v} ИНН: {k}" for k,v in suppliers_dict.items()])

    else:
        suppliers_data = 'Нет данных'

    contract_dict['suppliers_data'] = suppliers_data

    products = recurs_find_key('products', contract)

    subjects = ';'.join([recurs_find_key('name', product) for product in products])
    contract_dict['subjects'] = subjects
    top_contracts.append(contract_dict)

return top_contracts[:10]


def create_message(top_contracts):

    env = Environment(
        loader = FileSystemLoader('templates')
        autoescape = select_autpescape(['html', 'xml'])
    )

    template = env.get_template('table.html')

    message = template.render(items=top_contracts)
    with open('/Users/Pizzu/work_studio/robot/robor_code/my_new_table.html', 'w') as fh:
        fh.write(message)

    return message

result = get_contracts(daterange=get_week(), sort='-price')

message = create_message(ger_top_contracts(result))

email_list = ['tpitsuev@yandex.ru']


def send_email_with_contracts(message, email_list): 

    msg = MIMEmultipart('alternative')
    msg['Subject'] = 'Топ-10 контрактов'
    msg['From'] = SENDER_EMAIL
    msg['To'] = ', '.join(email_list)

    # указываю, что буду передавать в письму, и тип данных - html
    part1 = MIMEText(message, 'html')
    
    #прикрепляю к письму таблицу html
    msg.attach(part1)


    # с помощью сервисов google захожу в почту через безопасный протокол и отправляю сообщение
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smpt:

        smtp.login(SENDER_EMAIL, EMAIL_PASSWORD)
        smtp.send_message(msg)

send_email_with_contracts(message, email_list)