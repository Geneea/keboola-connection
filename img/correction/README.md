# Geneea text correction API

A Docker image used for running the text correction API.

This is an example of integration of [Geneea API](https://api.geneea.com) with [Keboola Connection](https://connection.keboola.com).

## Running a container
This container can be run from the Registry using:

```
sudo docker run \
--volume=/home/ec2-user/data:/data \
--rm \
geneea/keboola-correction:latest
```
Note: `--volume` needs to be adjusted accordingly.

## Sample configuration
Mapped to `/data/config.yml`

```
storage:
  input:
    tables:
      0:
        source: source.csv
  output:
    tables:
      0:
        source: correction.csv
parameters:
  user_key: <ENTER API KEY HERE>
  customer_id: <ENTER CUSTOMER ID HERE>
  id_column: id
  data_column: text
  language: en # OPTIONAL
```

## Sample data

### Input
Read from `/data/in/tables/source.csv`

```
id,text
1,"He won gold and silver medals at the past two Olympic Games, and even has an aquatic arena named after him."
2,"The museum was considered to host one of the world's greatest archaeological collections."
3,"These measurements should allow us to confirm some of the basic features of the greenhouse effect."
```

### Output
Written to `/data/out/tables/correction.csv`

```
id,correctedText,isCorrected,isDiacritized
1,"He won gold and silver medals at the past two Olympic Games, and even has an aquatic arena named after him.","false","false"
2,"The museum was considered to host one of the world's greatest archaeological collections.","false","false"
3,"These measurements should allow us to confirm some of the basic features of the greenhouse effect.","false","false"
```
