Kafka Schema for Hurricane Topic
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

Kafka Schema for syslog RFC5424 Topic
```
{
  "type": "record",
  "name": "inferredSchema",
  "fields": [
    {
      "name": "priority",
      "type": "string",
      "doc": "Type inferred from '\"62\"'"
    },
    {
      "name": "severity",
      "type": "string",
      "doc": "Type inferred from '\"6\"'"
    },
    {
      "name": "facility",
      "type": "string",
      "doc": "Type inferred from '\"7\"'"
    },
    {
      "name": "version",
      "type": "string",
      "doc": "Type inferred from '\"1\"'"
    },
    {
      "name": "eventtimeOccurred",
      "type": "long",
      "doc": "Type inferred from '1656364567814'"
    },
    {
      "name": "hostname",
      "type": "string",
      "doc": "Type inferred from '\"host10.example.com\"'"
    },
    {
      "name": "body",
      "type": "string",
      "doc": "Type inferred from '\"application7 has exited cleanly\"'"
    },
    {
      "name": "appName",
      "type": "string",
      "doc": "Type inferred from '\"application7\"'"
    },
    {
      "name": "procid",
      "type": "string",
      "doc": "Type inferred from '\"1674\"'"
    },
    {
      "name": "messageid",
      "type": "string",
      "doc": "Type inferred from '\"ID25\"'"
    },
    {
      "name": "structuredData",
      "type": {
        "type": "record",
        "name": "structuredData",
        "fields": [
          {
            "name": "SDID",
            "type": {
              "type": "record",
              "name": "SDID_structuredData",
              "fields": [
                {
                  "name": "eventId",
                  "type": "string",
                  "doc": "Type inferred from '\"9\"'"
                },
                {
                  "name": "eventSource",
                  "type": "string",
                  "doc": "Type inferred from '\"python\"'"
                },
                {
                  "name": "iut",
                  "type": "string",
                  "doc": "Type inferred from '\"4\"'"
                }
              ]
            },
            "doc": "Type inferred from '{\"eventId\":\"9\",\"eventSource\":\"python\",\"iut\":\"4\"}'"
          }
        ]
      },
      "doc": "Type inferred from '{\"SDID\":{\"eventId\":\"9\",\"eventSource\":\"python\",\"iut\":\"4\"}}'"
    }
  ]
}
```

DDL for Flink Table
```
CREATE TABLE `ssb`.`ssb_default`.`demo_syslog` (
  `priority` VARCHAR(2147483647),
  `severity` VARCHAR(2147483647),
  `facility` VARCHAR(2147483647),
  `version` VARCHAR(2147483647),
  `eventtimeOccurred` BIGINT,
  `hostname` VARCHAR(2147483647),
  `body` VARCHAR(2147483647),
  `appName` VARCHAR(2147483647),
  `procid` VARCHAR(2147483647),
  `messageid` VARCHAR(2147483647),
  `structuredData` ROW<`SDID` ROW<`eventId` VARCHAR(2147483647), `eventSource` VARCHAR(2147483647), `iut` VARCHAR(2147483647)>>,
  `eventTimestamp` TIMESTAMP(3) METADATA FROM 'timestamp',
  WATERMARK FOR `eventTimestamp` AS `eventTimestamp` - INTERVAL '3' SECOND
) COMMENT 'demo_syslog'
WITH (
  'properties.bootstrap.servers' = 'kdavis-trace3-ssb-demo-master0.se-sandb.a465-9q4k.cloudera.site:9093,kdavis-trace3-ssb-demo-master1.se-sandb.a465-9q4k.cloudera.site:9093',
  'properties.auto.offset.reset' = 'earliest',
  'connector' = 'kafka',
  'properties.request.timeout.ms' = '120000',
  'properties.ssl.truststore.location' = '/var/lib/cloudera-scm-agent/agent-cert/cm-auto-global_truststore.jks',
  'properties.transaction.timeout.ms' = '900000',
  'format' = 'json',
  'topic' = 'demo-syslog-5424',
  'properties.security.protocol' = 'SASL_SSL',
  'scan.startup.mode' = 'earliest-offset',
  'properties.sasl.kerberos.service.name' = 'kafka',
  'deserialization.failure.policy' = 'fail'
)
```
