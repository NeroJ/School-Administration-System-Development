import sys
import os.path
 
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
sys.path.append(os.path.join(os.path.dirname(__file__), 'project'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'site-packages')) 

import sae
from project import wsgi

application = sae.create_wsgi_app(wsgi.application)

