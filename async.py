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

# async def get_titles_string_by_url_list(url_list):
#     titles_list = []
#     for film_url in url_list:
#         async with session.get(film_url) as response:
#             json_data = await response.json()
#             title = json_data.get('title')
#             titles_list.append(title)
#     titles_str = ','.join(titles_list)
#     return titles_str


def get_titles_string_by_url_list(url_list):
    titles_list = []
    for film_url in url_list:
        response = requests.get(film_url)
        json_data = response.json()
        title = json_data.get('title')
        titles_list.append(title)
    titles_str = ','.join(titles_list)
    return titles_str

def get_names_string_by_url_list(url_list):
    names_list = []
    for film_url in url_list:
        response = requests.get(film_url)
        json_data = response.json()
        name = json_data.get('name')
        names_list.append(name)
    names_str = ','.join(names_list)
    return names_str



async def get_people(session, people_id):
    print(f'{people_id=} started')
    async with session.get(f'https://swapi.dev/api/people/{people_id}/') as response:
        json_data = await response.json()
        print(json_data)
        print(f'{people_id=} finished')
        return json_data


async def paste_to_db(results):
    for item in results:
        id = int(item['url'].split('/')[-2])
        name = item.get('name')
        birth_year = item.get('birth_year')
        films = get_titles_string_by_url_list(item.get('films'))
        species = get_names_string_by_url_list(item.get('species'))
        vehicles = get_names_string_by_url_list(item.get('vehicles'))
        starships = get_names_string_by_url_list(item.get('starships'))
        eye_color = item.get('eye_color')
        gender = item.get('gender')
        hair_color = item.get('hair_color')
        height = item.get('height')
        homeworld = item.get('homeworld')
        mass = item.get('mass')
        skin_color = item.get('skin_color')

        person = SwapiPeople(id=id, name=name, birth_year=birth_year, films=films, species=species, vehicles=vehicles, starships=starships)
        async with Session() as session:
            session.add(person)
            await session.commit()


async def main():
    start = datetime.datetime.now()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session = aiohttp.ClientSession()
    max_range = get_people_qty(session)
    coros = (get_people(session, i) for i in range (1, 10))
    for coros_chunk in chunked(coros, CHUNK_SIZE):
        results = await asyncio.gather(*coros_chunk)
        asyncio.create_task(paste_to_db(results))

    await session.close()
    set_tasks = asyncio.all_tasks()
    for task in set_tasks:
        if task != asyncio.current_task():
            await task
    print(datetime.datetime.now() - start)


asyncio.run(main())
