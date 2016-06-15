# Geneea lemmatization API

A Docker image used for running the lemmatization API.

This is an example of integration of [Geneea API](https://api.geneea.com) with [Keboola Connection](https://connection.keboola.com).

## Running a container
This container can be run from the Registry using:

```
sudo docker run \
--volume=/home/ec2-user/data:/data \
--rm \
geneea/keboola-lemmatize:latest
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
        source: lemmatize.csv
parameters:
  user_key: <ENTER API KEY HERE>
  id_column: id
  data_column: text
  language: en # OPTIONAL
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
Written to `/data/out/tables/lemmatize.csv`

```
id,lemma,lemmaIndex
1,HE,0
1,win,1
1,gold,2
1,and,3
1,silver,4
1,medal,5
1,AT,6
1,the,7
1,past,8
1,two,9
1,olympic,10
1,game,11
1,",",12
1,and,13
1,even,14
1,have,15
1,AN,16
1,aquatic,17
1,arena,18
1,name,19
1,after,20
1,him,21
1,.,22
2,The,0
2,museum,1
2,be,2
2,considered,3
2,to,4
2,host,5
2,one,6
2,have,7
2,the,8
2,world's,9
2,great,10
2,archeological,11
2,collection,12
2,.,13
3,These,0
3,measurement,1
3,should,2
3,allow,3
3,US,4
3,to,5
3,confirm,6
3,some,7
3,have,8
3,the,9
3,basic,10
3,feature,11
3,have,12
3,the,13
3,greenhouse,14
3,effect,15
3,.,16
```
