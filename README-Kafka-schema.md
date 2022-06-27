Kafka schema for Hurricane Data
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
