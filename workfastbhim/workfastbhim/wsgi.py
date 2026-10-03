import os
import sys

sys.path.append('/home/airbytes/workfastbhim')
sys.path.append('/home/airbytes/dev_apps')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'workfastbhim.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

print("==== DEBUG PATH ====")
for p in sys.path:
    print(p)
print("==== TRY IMPORT ====")
