
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
  
kafka-console-consumer \
  --bootstrap-server ${KAFKA_SERVER_1},${KAFKA_SERVER_2} \
  --consumer.config jaas.conf \
  --topic ${KAFKA_TOPIC} \
  --from-beginning
```



