from json import loads
from secrets import token_hex
import requests
import os

from app.models.basemodels import Person_

API_URL = os.environ['API_URL']
API_KEY = os.environ['API_KEY']
AUTHORIZED_ID = os.environ['AUTHORIZED_ID']

headers = {'api_key': API_KEY, 'id': AUTHORIZED_ID}

# Faz requisiões post
def post_request(endpoint, data):
    return requests.post(f'{API_URL}{endpoint}', data, headers=headers)

# Faz requisições get
def get_request(endpoint):
    return requests.get(f'{API_URL}{endpoint}', headers=headers)

# Faz requisições delete
def delete_request(endpoint):
    return requests.delete(f'{API_URL}{endpoint}', headers=headers)

def alternative_id_generator():
    ''' Gera um alternative_id aleatório'''
    return token_hex(16)

def new_alternative_id():
    ''' Gera um alternative_id aleatório com a função alternative_id_generator,
        consulta se já existe usuário com o alternative_id gerado, e caso não haja,
        retorna o alternative_id gerado'''

    alternative_id = alternative_id_generator()
    response = get_request(f'/persons-service/get-simple-person?type_data=alternative_id&alternative_id={alternative_id}')
    if response.status_code != 200:
        return None
    else:
        person_response_list = loads(response.text)
        if len(person_response_list) > 0:
            new_alternative_id()
        return alternative_id