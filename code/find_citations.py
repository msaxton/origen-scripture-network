import requests
from bs4 import BeautifulSoup
import re
import itertools
import json

def find_citations(urls, title):

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

    for url in urls:
        response = requests.get(url)
        xml = response.text
        soup = BeautifulSoup(xml, 'xml')
        notes = soup.find_all('note')
        for note in notes:
            refs = re.findall(re_pattern, note.text)
            master_list.extend(refs)
            relation_lists.append(refs)

    master_list = list(set(master_list))  # get only unique values

    # create nodes list
    nodes = [dict.fromkeys(['id', 'label']) for d in range(len(master_list))]
    i = 1
    for d, ref in zip(nodes, master_list):
        d['id'] = i
        d['label'] = ref
        i += 1


    id2label = {}
    label2id = {}
    i = 1
    for ref in master_list:
        id2label[i] = ref
        label2id[ref] = i
        i += 1

    relations_id_lists = []
    for list_ in relation_lists:
        if len(list_) > 1:  # ignore lists with 0 or 1 items
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

    edges_set = list(set(edges_list))

    # create edges list
    edges = [dict.fromkeys(['source', 'target']) for d in range(len(edges_set))]
    i =1
    for d, edge in zip(edges, edges_set):
        d['source'] = edge[0]
        d['target'] = edge[1]
        i += 1

    data = dict.fromkeys(['nodes', 'edges'])
    data['nodes'] = nodes
    data['edges'] = edges

    with open('data/' + title + '.json', 'w') as fp:
        json.dump(data, fp)


if __name__ == '__main__':
    urls = ['https://raw.githubusercontent.com/OpenGreekAndLatin/First1KGreek/master/data/tlg2042/tlg009/tlg2042.tlg009.opp-grc1.xml',
            'https://raw.githubusercontent.com/OpenGreekAndLatin/First1KGreek/master/data/tlg2042/tlg021/tlg2042.tlg021.opp-grc1.xml']
    title = 'HomJer'

    find_citations(urls=urls, title=title)