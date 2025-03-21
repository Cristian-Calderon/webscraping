"""
    Copyright (c) 2013 Joshua Machol
    MIT, see LICENSE for more details.
"""

import concurrent.futures
import urllib.request
import operator
import random
import json
import bs4
import re


MAX_WORKERS = 8

import urllib.request

def soupify(url):
    print("soupifying '{}'".format(url))
    
    # Definir una cabecera con User-Agent de un navegador real
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
    
    req = urllib.request.Request(url, headers=headers)
    
    with urllib.request.urlopen(req) as response:
        page = response.read()

    soup = bs4.BeautifulSoup(page, "html.parser")
    
    if not soup:
        raise ValueError("soup is '{}'", soup)
    
    return soup



def get_hero_urls(sample_size=None, hero_url=None):
    soup = soupify("http://www.dota2.com/heroes/")
    tags = soup(href=re.compile("http://www.dota2.com/hero/"))
    if hero_url:
        tags = [t for t in tags if t['href'].find(hero_url) > 0]
    if sample_size:
        tags = random.sample(tags, sample_size)
    return [t['href'] for t in tags]


def get_hero_soups(sample_size=None, hero_url=None):
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as e:
        future_soups = [e.submit(soupify, url) for url in get_hero_urls(sample_size, hero_url)]
        for future in concurrent.futures.as_completed(future_soups):
            yield future.result()


class Hero:
    def __init__(self, hero_id=''):
        self.hero_id = hero_id
        self.img_url = ''
        self.portrait_img_url = ''
        self.name = ''
        self.title = ''
        self.description = ''
        self.lore = ''
        self.allegiance = ''
        self.primary_attribute = ''
        self.atk_type = ''
        self.roles = ''
        self.int = ''
        self.agi = ''
        self.str = ''
        self.dmg = ''
        self.move_spd = ''
        self.armor = ''
        self.sight_range = ''
        self.atk_range = ''
        self.missile_spd = ''
        self.abilities = []  # list of type Ability


class Ability:
    def __init__(self, hero_id):
        self.ability_id = ''
        self.hero_id = hero_id
        self.img_url = ''
        self.vid_url = ''
        self.name = ''
        self.description = ''
        self.lore = ''
        self.mana_cost = ''
        self.cooldown = ''
        self.details = []  # list of type AbilityDetail


class AbilityDetail:
    def __init__(self, ability_id):
        self.ability_id = ability_id
        self.name = ''
        self.detail = ''


def _scrape_hero_ability(ability_soup, hero_id):
    a = Ability(hero_id)
    a.img_url = ability_soup.find(class_='overviewAbilityImg')['src']
    vid_soup = ability_soup.find(class_='abilityVideoContainer')
    if vid_soup:
        iframe = vid_soup.find('iframe')
        a.vid_url = iframe['src']
    ability_row_description = (ability_soup.find(class_='abilityHeaderRowDescription') or
                               ability_soup.find(class_='overviewAbilityRowDescription'))
    a.name = ability_row_description.find('h2').string
    a.description = ability_row_description.find('p').text.rstrip()
    lore_soup = ability_soup.find(class_='abilityLore')
    if lore_soup:
        a.lore = lore_soup.string
    mana_soup = ability_soup.find(class_='mana')
    if mana_soup:
        a.mana_cost = list(mana_soup.stripped_strings)[1]
    cooldown_soup = ability_soup.find(class_='cooldown')
    if cooldown_soup:
        a.cooldown = list(cooldown_soup.stripped_strings)[1]
    details_soup = ability_soup.find(class_='abilityFooterBoxRight')
    details = list(details_soup.stripped_strings)
    for name, detail in zip(details[::2], details[1::2]):
        d = AbilityDetail(a.ability_id)
        d.name = name[:-1]
        d.detail = detail
        a.details.append(d)
    return a


def _scrape_hero_abilities(soup_, hero_id):
    divs = soup_(class_='abilitiesInsetBoxContent')
    return [_scrape_hero_ability(d, hero_id) for d in divs]


def _scrape_hero(soup_):
    print(("scraping '{}'"
           .format(soup_.find(id='centerColContent').find('h1').string)))
    h = Hero()
    h.img_url = soup_.find(id='heroTopPortraitIMG')['src']
    h.portrait_img_url = soup_.find(id='heroPrimaryPortraitImg')['src']
    h.name = soup_.find(id='centerColContent').find('h1').string
    h.title = ''
    h.lore = list(soup_.find(id='bioInner').stripped_strings)[0]
    prim_style = soup_.find(id='overviewIcon_Primary')['style']
    if prim_style == 'top:83px':
        h.primary_attribute = 'str'
    elif prim_style == 'top:43px':
        h.primary_attribute = 'agi'
    elif prim_style == 'top:1px':
        h.primary_attribute = 'int'
    h.atk_type = soup_.find(class_='bioTextAttack').string
    roles_soup = soup_.find(id='heroBioRoles')
    if len(roles_soup.contents) > 1:
        h.roles = roles_soup.contents[1].strip(' - ')
    h.int = soup_.find(id='overview_IntVal').string
    h.agi = soup_.find(id='overview_AgiVal').string
    h.str = soup_.find(id='overview_StrVal').string
    h.dmg = soup_.find(id='overview_AttackVal').string
    h.move_spd = soup_.find(id='overview_SpeedVal').string
    h.armor = soup_.find(id='overview_DefenseVal').string
    misc_stats = soup_(class_='statRowCol2W')
    h.sight_range = misc_stats[0].string
    h.atk_range = misc_stats[1].string
    h.missile_spd = misc_stats[2].string
    h.abilities = _scrape_hero_abilities(soup_, h.hero_id)
    return h


def scrape_heroes(sample_size=None, hero_url=None):
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as e:
        future_heros = [e.submit(_scrape_hero, h) for h in get_hero_soups(sample_size, hero_url)]
        for future in concurrent.futures.as_completed(future_heros):
            yield future.result()


if __name__ == '__main__':
    print('scraping heroes')
    heroes = list(scrape_heroes())
    print('encoding heroes to JSON')
    json = json.dumps(heroes, separators=(',', ':'),
                      default=operator.attrgetter("__dict__"))
    f = open('heroes_json.txt', 'w')
    print('writing JSON to file "heroes_json.txt')
    f.write(json)
    f.close()
    print('done')