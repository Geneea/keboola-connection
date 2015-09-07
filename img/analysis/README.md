# Geneea general-purpose NLP analysis API

A Docker image used for running the general-purpose NLP analysis API.

The supported NLP analysis types are: `language`, `lemmatize`, `correction`, `topic`, `sentiment`, `entities`, `hashtags`.

This is an example of integration of [Geneea API](https://api.geneea.com) with [Keboola Connection](https://connection.keboola.com).

## Running a container
This container can be run from the Registry using:

```
sudo docker run \
--volume=/home/ec2-user/data:/data \
--rm \
geneea/keboola-analysis:latest
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
parameters:
  output: result.
  user_key: <ENTER API KEY HERE>
  id_column: id
  data_column: text
  analysis_types: [topic, sentiment, hashtags]
  language: en # OPTIONAL
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
Written to `/data/out/tables/result.topic.csv`

```
id,topic,confidence
1,Sports,0.467843459155
2,Science,0.373045280015
3,Other,NaN
```

Written to `/data/out/tables/result.sentiment.csv`

```
id,sentiment
1,0.29192017968
2,0.160356745147
3,0.0485071250073
```

Written to `/data/out/tables/result.hashtags.csv`

```
id,hashtag,score
1,win,10.3495449282
1,game,8.48926969186
1,past,6.38180877737
1,even,4.67190659034
2,collection,10.4650221456
2,host,9.20198773978
2,consider,7.44710023762
2,great,6.87007555632
3,basic,9.01436073661
3,effect,7.87605771434
3,feature,6.52016369981
3,allow,5.74803125121
3,confirm,4.9806691518
```
