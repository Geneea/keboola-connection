# Geneea API integration with Keboola Connection

Integration of the [Geneea API](https://api.geneea.com) with [Keboola Connection](https://connection.keboola.com).

This project servers as a base Docker container for the individual images in `img` folder which
provide a concrete functionality, i.e. calling of a particular API method.

## Building a container
To build this container manually one can use:

```
git clone https://github.com/Geneea/keboola-connection.git
cd keboola-connection
sudo docker build --no-cache -t geneea/keboola-connection .
```

## Configuration
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
        source: result.csv
parameters:
  user_key: <ENTER API KEY HERE>
  id_column: id
  data_column: text
  language: en # OPTIONAL
  use_beta: false # OPTIONAL
```
