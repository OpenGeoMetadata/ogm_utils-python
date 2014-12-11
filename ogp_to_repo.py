__author__ = 'chrissbarnett'

import urllib
import urlparse
import json
from repo_utils import write_to_repository
from repo_dir import get_hash_dir

SOLR_URL = 'http://geodata.tufts.edu/solr/select'
# number of rows returned per request
ROWS = 100
FIELDS = ['LayerId', 'FgdcText']


def get_params(institution, start, rows):
    return {'wt': 'json', 'q': "Institution:" + institution,
            'fl': ",".join(FIELDS), 'start': str(start),
            'rows': str(rows)}


def get_response(url):
    print url
    j = urllib.urlopen(url)
    r = json.load(j)
    return r["response"]


def add_query(base, params):
    url_parts = list(urlparse.urlparse(base))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)

    url_parts[4] = urllib.urlencode(query)

    return urlparse.urlunparse(url_parts)


def get_count(inst, solrurl=SOLR_URL):
    url = add_query(solrurl, get_params(inst, 0, 0))
    return get_response(url)["numFound"]


def get_docs(inst, start, solrurl=SOLR_URL, rows=ROWS):
    url = add_query(solrurl, get_params(inst, start, rows))
    return get_response(url)["docs"]


def get_info_from_doc(doc):
    value = doc["FgdcText"]
    value = value.encode('utf-8');
    layerid = doc["LayerId"]

    return {'metadata': value,
            'layerid': layerid}


def add_all_results_to_repo(inst):
    total = get_count(inst)
    start = 0
    while total > 0:
        total -= ROWS
        start += ROWS
        docs = get_docs(inst, start)
        for d in docs:
            i = get_info_from_doc(d)
            write_to_repository(i.get("layerid"), i.get("metadata"))


def test_hash(inst):
    test_collisions(inst)


def test_collisions(inst):
    total = get_count(inst)
    start = 0
    hashlist = []
    dups = []
    while total > 0:
        total -= ROWS
        start += ROWS
        docs = get_docs(inst, start)
        for d in docs:
            i = get_info_from_doc(d)
            layerid = i.get("layerid")
            hash = get_hash_dir(layerid)
            print hash
            if hash in hashlist:
                dups.append({layerid: hash})
            else:
                hashlist.append(hash)
    print dups
    print "finished collision test!"

