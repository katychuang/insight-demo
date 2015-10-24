from __future__ import absolute_import

import logging

from pyleus.storm import SimpleBolt
from datetime import datetime
from cassandra.cluster import Cluster

cluster = Cluster(['54.164.65.18'])
session = cluster.connect('spark_pond')
session.default_timeout = 30 # 30 seconds

log = logging.getLogger('topologybolt')

class MyBolt(SimpleBolt):

    OUTPUT_FIELDS = ["finish"]
    
    def process_tuple(self, tup):
        shoe, = tup.values
        s = shoe['1'].split(',')
        fmt = '%Y-%m-%d %H:%M:%S'
        time2 = datetime.now()
        time1 = datetime.strptime(s[1], '%Y-%m-%d %H:%M:%S.%f')
        delta = time2 - time1
          
        t1 = s[1].split(".")[0]
        t2 = datetime.strftime(time2,fmt)
        session.execute("INSERT INTO storm_1m (testid, time1, delta, time2) values ('storm1', %s, %s, %s);", 
                        (s[1], delta.microseconds, str(time2)))
        log.debug("{} x {} >> {}\n".format(time2, shoe, len(shoe)))
        self.emit((str(time2),), anchors=[tup])
        

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.WARNING,
        filename='xtime2_kafka.log',
        format="[%(asctime)s] %(levelname)s %(message)s",
        filemode='a'
    )

    MyBolt().run()
