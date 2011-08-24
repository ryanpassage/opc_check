####
# FetchOPC
# Connects to an OPC server and fetches a list of assets with valid "EOC" tags for storage in the database.
#
# This script uses Django's models to load the list of assets and tags to check from the database.
# Ryan Passage <rpassage@cmwa.com>
#
# Last Changed: 8/22/11
####

import sys, os
import OpenOPC

kepware = 'KEPware.KEPserverEX.v4'

# hook in to the django project for access to our models
sys.path.append('/home/ryan/virtualenvs/opc/dev')
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
from django.core.management import setup_environ
from project import settings
setup_environ(settings)

# import models and choices
from project.web.models import Asset, COLLECTOR_CHOICES
choices = dict(COLLECTOR_CHOICES)

# loop through the OPC servers, connecting to each one and 
# creating the asset objects we need based off of the data
itemcount = 0

for plant in choices:
    for server in choices[plant]:
        # ('192.168.141.204', 'APCOLLECTCMC')
        try:
            opc = OpenOPC.open_client(server[0])
            opc.connect(kepware)
        except:
            print 'Connection to %s (%s) failed!' % (server[0], kepware)
            break

        eoc_list = opc.list("*.EOC", flat=True)

        for item in eoc_list:
            parts = item.split('.')

            # pop the EOC string off the list and put together our components
            tag = parts.pop()
            name = parts[-1]
            path = '.'.join(parts[:-1])

            # create our new object
            asset = Asset(name=name, path=path, collector=server[0], check_tag=tag)
            asset.save()
            
            print "Created: %s (%s.%s) on %s" % (asset, path, name, server[0])
            itemcount += 1

        opc.close()

print "Created %s total assets!" % itemcount