####
# OPC Data Quality Monitor
# Runs every so often by cron and checks the status of each asset's data quality.
#
# This script uses Django's models to load the list of assets and tags to check from the database.
# Ryan Passage <rpassage@cmwa.com>
#
# Last Changed: 8/19/11
####

import sys, os, time
import OpenOPC

start_time = time.time()
kepware = 'KEPware.KEPserverEX.v4'

# hook in to the django project for access to our models
sys.path.append('/home/ryan/virtualenvs/opc/dev')
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
from django.core.management import setup_environ
from project import settings
setup_environ(settings)

# import models
from project.web.models import Asset

last_collector = ''
num_checked = 0
for asset in Asset.objects.order_by('collector'):
    if asset.collector != last_collector:
        print "Creating a new OPC client for %s... " % asset.collector,
        try:
            opc = OpenOPC.open_client(asset.collector)
            opc.connect(kepware)
        except:
            print "failed to connect to %s!" % asset.collector
            break
        print "success!"

    print "Retrieving properties for %s... " % asset.full_path(),
    status = opc.properties(asset.full_path(), id=3)
    print status
    
    asset.quality = status
    asset.save()
    
    last_collector = asset.collector
    num_checked += 1

opc.close()
print "Checked %d assets in %d seconds" % (num_checked, time.time() - start_time)