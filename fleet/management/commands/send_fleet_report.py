from django.core.management.base import BaseCommand
import smtplib
import datetime

from fleet.models import UnitProfile


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        
        date = datetime.datetime.today()
        operational = UnitProfile.objects.filter(status='Operational').count()
        under_repair = UnitProfile.objects.filter(status='Under Repair').count()
        idle = UnitProfile.objects.filter(status='Idle').count()
        for_disposal = UnitProfile.objects.filter(status='For Disposal').count()
        
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("aip911dispatch@gmail.com", "giantbaby")
        server.sendmail("aip911dispatch@gmail.com", "trigger@applet.ifttt.com",
        """Equipment Monitoring
Date: %s
-------------
Operational: %s
Under Repair: %s
Idle: %s
For Disposal: %s
-------------
Note: System generated, replies are not received. For details visit our site!
""" % (str(date), str(operational), str(under_repair), str(idle), str(for_disposal))
        )
        server.quit()