```
scp ../data/file_stream.txt kdavis@kdavis-webinar-ssb-master1.se-sandb.a465-9q4k.cloudera.site:/home/kdavis
```

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
export KAFKA_TOPIC=demo_hurricane_metrics

kafka-topics \
  --bootstrap-server ${KAFKA_SERVER_1},${KAFKA_SERVER_2} \
  --command-config jaas.conf \
  --create --topic demo_hurricane_metrics --partitions 8

kafka-topics \
  --list \
  --bootstrap-server ${KAFKA_SERVER_1},${KAFKA_SERVER_2} \
  --command-config jaas.conf 

kafka-console-producer \
  --bootstrap-server ${KAFKA_SERVER_1},${KAFKA_SERVER_2} \
  --producer.config jaas.conf \
  --topic ${KAFKA_TOPIC} \
  < file_stream.txt
```

Kafka schema
```
{
  "type": "record",
  "name": "inferredSchema",
  "fields": [
    {
      "name": "us_state",
      "type": "string",
      "doc": "Type inferred from '\"OK\"'"
    },
    {
      "name": "us_county",
      "type": "string",
      "doc": "Type inferred from '\"Pontotoc\"'"
    },
    {
      "name": "hazard_metric",
      "type": "double",
      "doc": "Type inferred from '21.200000000000003'"
    }
  ]
}
```

Kafka topic
```
CREATE TABLE `ssb`.`ssb_default`.`demo_hurricane_metrics` (
  `us_state` VARCHAR(2147483647),
  `us_county` VARCHAR(2147483647),
  `hazard_metric` DOUBLE,
  `eventTimestamp` TIMESTAMP(3) METADATA FROM 'timestamp',
  WATERMARK FOR `eventTimestamp` AS `eventTimestamp` - INTERVAL '60' SECOND
) COMMENT 'demo_hurricane_metrics'
WITH (
  'properties.bootstrap.servers' = 'kafka:9092',
  'properties.auto.offset.reset' = 'earliest',
  'connector' = 'kafka',
  'properties.request.timeout.ms' = '120000',
  'properties.transaction.timeout.ms' = '900000',
  'format' = 'json',
  'topic' = 'demo_hurricane_metrics',
  'scan.startup.mode' = 'earliest-offset'
)
```

Impala table
```
CREATE TABLE demo.demo_hurricane_metrics
(
  us_state STRING NOT NULL,
  us_county STRING NOT NULL,
  eventTimestamp TIMESTAMP NOT NULL,
  hazard_metric DECIMAL(38, 6),
  PRIMARY KEY (us_state, us_county, eventTimestamp)
)
PARTITION BY HASH(us_county) PARTITIONS 10
STORED AS KUDU
TBLPROPERTIES (
'kudu.num_tablet_replicas' = '3'
)
;
```

Kudu Master as Data Provider
```
kdavis-webinar-kudu-master10.se-sandb.a465-9q4k.cloudera.site:7051
```

Run continuous query to insert data into Kudu table from Kafka topic
```
INSERT INTO `Demo Cloudera Data Mart`.`default_database`.`demo.demo_hurricane_metrics` 
VALUES (us_state, us_county, eventTimestamp, hazard_metric)
SELECT us_state, us_county, eventTimestamp, hazard_metric
FROM `ssb`.`ssb_default`.`demo_hurricane_metrics`
```

