```
ssh kdavis@kdavis-webinar-ssb-master1.se-sandb.a465-9q4k.cloudera.site
```

```
cat jaas.conf
...
security.protocol=SASL_SSL
sasl.kerberos.service.name=kafka
sasl.mechanism=GSSAPI
sasl.jaas.config=com.sun.security.auth.module.Krb5LoginModule required \
  useTicketCache=true \
  principal="kdavis@SE-SANDB.A465-9Q4K.CLOUDERA.SITE";

export KAFKA_SERVER_1=kdavis-webinar-ssb-master0.se-sandb.a465-9q4k.cloudera.site:9093
export KAFKA_SERVER_2=kdavis-webinar-ssb-master1.se-sandb.a465-9q4k.cloudera.site:9093

kafka-topics \
  --bootstrap-server ${KAFKA_SERVER_1},${KAFKA_SERVER_2} \
  --command-config jaas.conf \
  --create --topic demo_hurricane_metrics --partitions 8

kafka-topics \
  --list \
  --bootstrap-server ${KAFKA_SERVER_1},${KAFKA_SERVER_2} \
  --command-config jaas.conf 

```

Impala table
```
CREATE TABLE demo.demo_hurricane_metrics
(
  ts STRING NOT NULL,
  county STRING NOT NULL,
  avg_hazard_metric DECIMAL(38, 6),
  PRIMARY KEY (ts, county)
)
PARTITION BY HASH(county) PARTITIONS 10
STORED AS KUDU
TBLPROPERTIES (
'kudu.num_tablet_replicas' = '3'
)
;
```

