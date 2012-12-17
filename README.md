## OPC Check ##

This is a set of scripts that I wrote to meet a specific need at my company.  You are welcome to use them, but they will need to be tweaked to work for your environment.

> Problem: We monitor assets on our plant floor using OPC software (Kepware) that reads data from PLCs.  When data quality goes bad for some reason (networking issue, PLC address change, power issue, etc), we have no way of knowing until people realize data has stopped flowing to the collection system.  This is a big problem.

Solution: OPC Check

- *perform_check.py*: script that will run every X minutes via cron to read the current data quality for all assets with "EOC" tags, and store their status in a sqlite database.  The assets are loaded from the database, and the script cycles through each OPC server (as defined in the Django project model) to read the assets and update their status.  Emails alerts are sent out if we have bad data to report.

- *fetch_opc.py*: script that initially loads the assets in to our database using the Django "Asset" model.  OpenOPC provides a list of assets from Kepware with "EOC" tags, and these get imported in to the database.  This really only needs to be run once, to pre-load the database.

- *web/**: the django app.  contains model definitions and a little admin tweaking.  eventually this will provide a web interface to view the asset model information (this is why I used Django to manage the database objects).

### Requirements ###
- OpenOPC (http://openopc.sourceforge.net/) is awesome.  The module is provided here in OpenOPC.py, however opening a remote client requires their Gateway service to be installed also.

- Django (http://www.djangoproject.com) for the database ORM and easy web-interface creation down the road.  Also, automatic admin interface is great for managing our asset records.

