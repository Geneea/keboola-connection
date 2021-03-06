# Geneea language detection API

A Docker image used for running the language detection API.

This is an example of integration of [Geneea API](https://api.geneea.com) with [Keboola Connection](https://connection.keboola.com).

## Running a container
This container can be run from the Registry using:

```
sudo docker run \
--volume=/home/ec2-user/data:/data \
--rm \
geneea/keboola-language:latest
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
        source: language.csv
parameters:
  user_key: <ENTER API KEY HERE>
  id_column: id
  data_column: text
  domain: "news articles" # OPTIONAL
  use_beta: false # OPTIONAL
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
Written to `/data/out/tables/language.csv`

```
id,language
1,"en"
2,"en"
3,"en"
```
