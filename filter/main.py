import sys
import logging as log
import json

import config


def m_filter(listings, query_filters):
    for l in listings:
        f = query_filters[l['query']]
        if f(l): yield l


def main(argv):
    with open('data.jsonl', 'r') as f:
        data = [json.loads(l) for l in f.read().split('\n') if l]

    results = m_filter(data, config.query_filters)

    with open('flt_data.jsonl', 'w') as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii = True))
            f.write('\n')

if __name__ == '__main__':
    log.getLogger().setLevel(log.INFO)
    main(sys.argv)

