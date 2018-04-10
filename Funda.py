import json
import requests
import functools
import operator
import time
from prettytable import PrettyTable


def get_objects(url):
    data = requests.get(url) #get access to url
    json_text = data.text    #extract text
    parsed_string = json.loads(json_text)  # from json create Python object
    return parsed_string['Objects'] #extract the object containing required datas


def get_name(object): #note a tag containing key name
    return object['MakelaarNaam']


def add_to_name_count_dict(name_count_dict, name):
    if isinstance(name_count_dict, str): #check type of 1st object
        name_count_dict = {name_count_dict: 1} #change format from string to dictionary

    old_quantity = name_count_dict.get(name) #looking for a name of an agent in a dictionary, and return value by key
    new_quantity = old_quantity + 1 if old_quantity else 1 #if name exist add 1 to value, if not - assigns 1

    name_count_dict[name] = new_quantity #assigns to name  new quantity for current agent

    return name_count_dict

#create function for applay function 'add_to_name_count_dict for each name of agent
def count_names(names):
    return functools.reduce(add_to_name_count_dict, names)

#create a function that changes the address of the link according to the required parameters
def get_all_amsterdam(partlink): #pass info about exist of garden
    names = []
    link_template = "http://partnerapi.funda.nl/feeds/Aanbod.svc/json/ac1b0b1572524640a0ecc54de453ea9f/?type=koop&zo=/" \
                    "amsterdam/{}&page={}&pagesize=25"
    i = 0
    print("Fetching pages: ")
    while True:
        i += 1 #count pages
        objects = get_objects(link_template.format(partlink, i)) #extracts data from each page
        print('|', end='', flush=True)
      #  time.sleep(2) #pause requests but I don't need it because it doesn't exceed the limit
        if not objects:
            break #escape from the loop if not objects
        names += list(map(get_name, objects)) #extract all name of the agents from current page
    print('\n')
    return names #returned list of objects


def get_top(allnames):
    toplist = sorted(allnames.items(), key = operator.itemgetter(1), reverse = True) #sort all agents by the value
    return toplist[:10] #extract first 10 results

def final_table(partadress):
    tenagents = get_top(count_names(get_all_amsterdam(partadress))) #get list of 10 agents
    if partadress =='tuin/': #choose title
        print('Top 10 agents in Amsterdam who sale house with garden')
    else:
        print('Top 10 agents in Amsterdam:')
    f = PrettyTable() #apply PrettyTable from prettytable module
    f.field_names = ['Agent', 'Objects']
    for h in tenagents:
        f.add_row(h)
    print(f)

final_table('') #call a function and pass details about searching parameters
final_table('tuin/')