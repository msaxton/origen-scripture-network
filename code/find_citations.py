import requests
from bs4 import BeautifulSoup
import re
import itertools
import pandas as pd

def find_citations(url, auth_name, text_name):

    # reference abbreviations
    abbrs = {'Gen': 'Gen', 'Exod': 'Exod', 'Lev': 'Lev', 'Num': 'Num', 'Deut': 'Deut', 'Jos': 'Josh', 'Jud': 'Judg',
             'I Sam': '1 Sam', 'II Sam': '2 Sam', 'I Kön': '1 Kgs', 'II Kön': '2 Kgs', 'I Chron': '1 Chr',
             'II Chron': '2 Chr', 'Psal': 'Ps', 'Prov': 'Prov', 'Job': 'Job', 'Jes': 'Isa', 'Jerem': 'Jer',
             'Ezech': 'Ezek', 'Dan': 'Dan', 'Matth': 'Matt', 'Mark': 'Mark', 'Luk': 'Luke', 'Joh': 'John', 'Act': 'Acts',
             'Rom': 'Rom', 'I Kor': '1 Cor', 'II Cor': '2 Cor', 'Gal': 'Gal', 'Eph': 'Eph', 'Phil': 'Phil', 'Kol': 'Col',
             'I Tim': '1 Tim', 'II Tim': '2 Tim', 'Tit': 'Titus', 'Hebr': 'Heb', 'I Petr': '1 Pet', 'II Petr': '2 Pet',
             'I Joh': '1 John', 'II Joh': '2 John', 'III Joh': '3 John', 'Apok Joh': 'Rev'}

    # get list of german abbreviations
    ger_abbrs = []
    for k in abbrs.keys():
        ger_abbrs.append(k)

    # build regex pattern for later use
    re_pattern = ''
    for abbr in ger_abbrs:
        pattern = abbr + '. \d+|' + abbr + ' \d+|'
        re_pattern = re_pattern + pattern
    re_pattern = re_pattern[:-1]  # remove final |

    # create lists for later use
    master_list = []  # list of all references
    relation_lists = []  # list of relation lists

    response = requests.get(url)
    xml = response.text
    soup = BeautifulSoup(xml, 'xml')
    notes = soup.find_all('note')
    for note in notes:
        refs = re.findall(re_pattern, note.text)
        master_list.extend(refs)
        relation_lists.append(refs)

    master_list = list(set(master_list))  # get only unique values

    id2label = {}
    label2id = {}
    i = 1
    for ref in master_list:
        id2label[i] = ref
        label2id[ref] = i
        i+=1

    # Create csv files

    file_name = auth_name + '_' + text_name + '_'

    nodes_df = pd.DataFrame.from_dict(id2label, orient='index')
    nodes_df['Id'] = nodes_df.index
    nodes_df = nodes_df.rename(columns={0: 'Label'})
    nodes_df = nodes_df[['Id', 'Label']]
    nodes_df.to_csv(file_name + '_nodes.csv', index=False)

    relations_id_lists = []
    for list_ in relation_lists:
        if len(list_) > 1:  #ignore lists with 0 or 1 items
            id_list = []
            for ref in list_:
                id_ = label2id[ref]
                id_list.append(id_)
                comb_list = list(itertools.combinations(id_list, 2))
            relations_id_lists.append(comb_list)

    edges_list = []
    for l in relations_id_lists:
        for t in l:
            edges_list.append(t)

    data = list(set(edges_list))
    edges_df = pd.DataFrame(data, columns=['Source', 'Target'])
    edges_df.to_csv(file_name + '_edges.csv', index=False)

if __name__ == '__main__':
    url = 'https://raw.githubusercontent.com/OpenGreekAndLatin/First1KGreek/master/data/tlg2042/tlg016/tlg2042.tlg016.opp-grc1.xml'
    auth_name = 'org'
    text_name = 'homLuke'
    find_citations(url=url, auth_name=auth_name, text_name=text_name)