import asyncio
import aiohttp
import datetime
from more_itertools import chunked
from models import engine, Session, Base, SwapiPeople
import requests
import json


CHUNK_SIZE = 10

def get_people_qty(session):
    response = requests.get(f'https://swapi.dev/api/people/')
    json_data = response.json()
    max_range = json_data.get('count') + 1
    return max_range

# async def get_titles_string_by_url_list(session, url_list):
#     titles_list = []
#     print(titles_list)
#     for film_url in url_list:
#         async with session.get(film_url) as response:
#             json_data = await response.json()
#             title = json_data.get('title')
#             print(title)
#             titles_list.append(title)
#     print(titles_list)
#     titles_str = ','.join(titles_list)
#     print(titles_str)
#     return titles_str

def get_titles_string_by_url_list(url_list):
    titles_list = []
    print(titles_list)
    for film_url in url_list:
        response = requests.get(film_url)
        json_data = response.json()
        title = json_data.get('title')
        print(title)
        titles_list.append(title)
    print(titles_list)
    titles_str = ','.join(titles_list)
    print(titles_str)
    return titles_str

response = requests.get('https://swapi.dev/api/people/1')
json_data = response.json()
url_list = json_data.get('films')
print(url_list)
get_titles_string_by_url_list(url_list)

# async def main():
#     start = datetime.datetime.now()
#     response = requests.get('https://swapi.dev/api/people/1')
#     json_data = response.json()
#     url_list = json_data.get('films')
#     print(url_list)
#
#     session = aiohttp.ClientSession()
#
#     await get_titles_string_by_url_list(session, url_list)
#
#
#     await session.close()
#
# asyncio.run(main())

