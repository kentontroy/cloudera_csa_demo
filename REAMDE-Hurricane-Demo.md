## Run Kafka commands for topic maintenance

Create a topic:
```
docker-compose exec kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server kafka:9092 --create \
  --topic demo_hurricane_metrics --partitions 8
```
NOTE: if you're Kafka consumer is running on a node external to the Docker host, you have to resolve the DNS <br>
      name used by Docker -> kafka <br>
From Mac or Linux host:
```
cat /etc/hosts
...
# For customer-facing tests
204.236.149.139 kafka
```

Consume a topic:
```
docker-compose exec kafka /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server kafka:9092 \
  --from-beginning --topic demo_hurricane_metrics
```
Delete a topic:
```
docker-compose exec kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server kafka:9092 --delete \
  --topic demo_hurricane_metrics 
```

## Use SQL Stream Builder (SSB) 

Kafka can serve as a Data Provider using a topic as the source for an SSB table.
Login to the browser-based Console at port 8000.
Wizards in SSB can automate the creation of the DDL in Flink:
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
Start a Kafka Producer (i.e. the weather/hurricane simulator):
```
cd src/hurricane
bokeh serve --show controller.py
```
Run a continuous query against the incoming, unbounded stream:
```
SELECT * FROM demo_hurricane_metrics
;
```
## Build a Materialized View
Create a continuous query to aggregate (by AVG) data into 5-minute intervals
```
SELECT AVG(CAST(hazard_metric AS numeric)) AS avg_hazard_metric,
       CAST(TUMBLE_END(eventTimestamp, interval '5' minute) AS varchar) AS ts,
       us_county || ', ' || us_state AS county 
FROM demo_hurricane_metrics
GROUP BY us_state, us_county, TUMBLE(eventTimestamp, interval '5' minute) 
; 
```
Build a Materialized View from the query.
SSB will create a REST endpoint (static or dynamic) with an embedded API key

```
curl http://localhost:18131/api/v1/query/5196/demo?key=245a51f6-2781-46b9-8db4-42ee1e77c1e0 | jq

[
  {
    "avg_hazard_metric": "21.192308",
    "ts": "2022-03-08 00:30:00.000",
    "county": "Grady, OK"
  },
  {
    "avg_hazard_metric": "20.880000",
    "ts": "2022-03-08 00:30:00.000",
    "county": "Bell, TX"
  },
  ......
]
```
<img src="./images/cloudera_materialized_view.png" alt=""/><br>

