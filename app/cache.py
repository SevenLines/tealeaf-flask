import os
from flask.ext.cache import Cache
from app.load_app import app

cache = Cache(app, config={
    'CACHE_TYPE': os.environ.get('CACHE_TYPE', 'filesystem'),
    'CACHE_DIR': os.path.join(app.config['BASE_DIR'], 'cache')
})

