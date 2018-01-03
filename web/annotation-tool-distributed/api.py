from eve import Eve
import json
import numpy as np
from flask_cors import CORS
from collections import defaultdict

bbs = defaultdict(list)

images = {
'schema': {
    'url':{
        'type': 'string',
        'required': True
        },

    'x': {
        'type':'integer',
        'required': True
    },

    'y': {
        'type':'integer',
        'required': True
    },

    'w': {
        'type':'integer',
        'required': True
    },

    'h': {
        'type':'integer',
        'required': True
    }
    
},
    'resource_methods':['GET','POST'],
}

settings = {
    'IF_MATCH': False,
    'DOMAIN': {
        'images' : images
}
}       

app = Eve(settings=settings)

CORS(app)             
def do_work(resource, docs):
    if resource == 'images':
        for doc in docs:
            #print json.dumps(doc['tests'], indent = 4, sort_keys = True)
            print doc['url']
            print doc['x'], doc['y'], doc['w'], doc['h']
            bbs[doc['url']].append((doc['x'], doc['y'], doc['w'], doc['h']))

app.on_insert += do_work

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 9011)
