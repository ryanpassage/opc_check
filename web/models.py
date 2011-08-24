from django.db import models

COLLECTOR_CHOICES =  (
    ('Steel', (
            ('192.168.141.204', 'APCOLLECTCMC'),
            ('192.168.141.205', 'APCOLLECTCMC2'),
        )
    ),
    ('Aluminum', (
            ('192.168.141.203', 'APCOLLECTCLA'),
            ('192.168.141.202', 'APCOLLECTCLA2'),
        )
    ),
)

# Create your models here.
class Asset(models.Model):
    name = models.CharField(max_length=50, blank=False)
    path = models.CharField(max_length=100, blank=False)
    collector = models.CharField(max_length=15, choices=COLLECTOR_CHOICES, blank=False)
    check_tag = models.CharField(max_length=25, blank=False)
    quality = models.CharField(max_length=4, editable=False)
    last_check = models.DateTimeField(auto_now=True, editable=False)

    def full_path(self):
        return "%s.%s.%s" % (self.path, self.name, self.check_tag)

    def __unicode__(self):
        return self.name
