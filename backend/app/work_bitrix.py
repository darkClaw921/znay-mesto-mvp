import traceback
from fast_bitrix24 import Bitrix
from pprint import pprint 
from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()
WEBHOOK=os.getenv("WEBHOOK")

bit=Bitrix(WEBHOOK, ssl=False)

async def get_all_products():
    # products=await bit.call("crm.product.list", 
    products1=await bit.get_all("crm.product.list",
                params={"select":["NAME",
                              "DESCRIPTION",
                              "NAME","CODE",
                              "PROPERTY_107",
                              'DATE_CREATE','DATE_MODIFY',
                              'TIMESTAMP_X',
                              'PREVIEW_PICTURE','DETAIL_PICTURE',
                              'SECTION_ID']})
            # params={"select":["name"]})
    pprint(products1)
    # 1/0
    return products1

@dataclass
class Catalog:
    ohota: int = 31
    rybalka: int = 33 
    kulturniy_turizm: int = 39
    priklyuchenie: int = 41
    eko_turizm: int = 43
    plazh_turizm: int = 45
    gastronomic_turizm: int = 47
    medical_turizm: int = 49
    sport_turizm: int = 51
    religioznyy_turizm: int = 53
    business_turizm: int = 55
    agroturizm: int = 57
    zimniye_vidy_sporta: int = 59
    bеg_i_marafony: int = 61
    parakliniizm_i_deltaplanirizm: int = 63
    yogi_i_fitnes: int = 65
    gribnictvo: int = 67
    orekhodstvo: int = 69
    sbir_dikorastuyushchikh_plodov: int = 71
    travnictvo: int = 73
    yagodnictvo: int = 75
    
# 31 - Охота
# 33 - Рыбалка
# 39 - Культурный туризм и пеший туризм
# 41 - Приключенческий туризм и альпинизм
# 43 - Экотуризм и кемпинг
# 45 - Пляжный туризм и водные виды спорта
# 47 - Гастрономический туризм
# 49 - Медицинский туризм
# 51 - Спортивный туризм и спортивные игры
# 53 - Религиозный туризм
# 55 - Деловой туризм
# 57 - Агротуризм и велосипедный спорт
# 59 - Зимние виды спорта
# 61 - Бег и марафоны
# 63 - Парапланеризм и дельтапланеризм
# 65 - Йога и фитнес на свежем воздухе
# 67 - Грибничество
# 69 - Ореховодство
# 71 - Сбор дикорастущих плодов
# 73 - Травничество
# 75 - Ягодничество



async def create_new_product(product:dict):
    """Создает новый товар в Битрикс24"""
    # try:
    print(product)
    result = await bit.call(
        'crm.product.add',
        {
            'fields': {
                'NAME': product['NAME'],
                'DESCRIPTION': product['DESCRIPTION'],
                'CATALOG_ID': product['SECTION_ID'],
                'PROPERTY_107': product['COORDINATES'],
            }
        }
    )
    return result
    # except Exception as e:
    #     print(traceback.format_exc())
    #     print(f"Ошибка при создании товара: {e}")
    #     return None

async def parse_and_create_products():
    """Парсит файл tovar.txt и создает товары"""
    catalog = Catalog()
    section_mapping = {
        'Охота': catalog.ohota,
        'Рыбалка': catalog.rybalka,
        'Культурный туризм и пеший туризм': catalog.kulturniy_turizm,
        'Приключенческий туризм и альпинизм': catalog.priklyuchenie,
        'Экотуризм и кемпинг': catalog.eko_turizm,
        'Пляжный туризм и водные виды спорта': catalog.plazh_turizm,
        'Гастрономический туризм': catalog.gastronomic_turizm,
        'Медицинский туризм': catalog.medical_turizm,
        'Спортивный туризм и спортивные игры': catalog.sport_turizm,
        'Религиозный туризм': catalog.religioznyy_turizm,
        'Деловой туризм': catalog.business_turizm,
        'Агротуризм и велосипедный спорт': catalog.agroturizm,
        'Зимние виды спорта': catalog.zimniye_vidy_sporta,
        'Бег и марафоны': catalog.bеg_i_marafony,
        'Парапланеризм и дельтапланеризм': catalog.parakliniizm_i_deltaplanirizm,
        'Йога и фитнес на свежем воздухе': catalog.yogi_i_fitnes,
        'Грибничество': catalog.gribnictvo,
        'Ореховодство': catalog.orekhodstvo,
        'Сбор дикорастущих плодов': catalog.sbir_dikorastuyushchikh_plodov,
        'Травничество': catalog.travnictvo,
        'Ягодничество': catalog.yagodnictvo,
    }

    products = []
    current_product = {}
    
    with open('tovar.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
        # Пропускаем заголовок
        for line in lines[1:]:
            fields = line.strip().split('\t')
            if len(fields) >= 11:  # Проверяем, что строка содержит все необходимые поля
                section = fields[0].strip()
                coordinates = fields[3].strip()
                name = fields[10].strip()
                description = fields[11].strip() if len(fields) > 11 else ""
                print(f"section: {section}, name: {name}, description: {description}, coordinates: {coordinates}") 
                if section in section_mapping:
                    product = {
                        'NAME': name,
                        'DESCRIPTION': description,
                        'SECTION_ID': section_mapping[section],
                        'COORDINATES': coordinates,
                        'section': section,
                    }
                    products.append(product)
    # 1/0
    # Создаем товары
    for product in products:
        result = await create_new_product(product)
        if result:
            print(f"Создан товар: {product['NAME']}")
        else:
            print(f"Ошибка при создании товара: {product['NAME']}")

if __name__=="__main__":
    import asyncio
    products=asyncio.run(get_all_products())
    pprint(products)
    # asyncio.run(parse_and_create_products())









