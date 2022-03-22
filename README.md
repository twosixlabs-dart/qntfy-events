# Qntfy Event Analytic

Python-powered RESTful web service that provides event annotations on
incoming CDR data.

[Paper with description of the model](https://www.aclweb.org/anthology/D17-1035/).

## Swagger-rendered HTML documentation

Can be found [here](https://worldmodelers.pages.qntfy.com/event-analytic/).

## Build


### Installation

```shell
conda create -n bilstm python=3.7
conda activate bilstm
sh dependencies.sh
```

## Usage

```
from model import detect_events

In [5]: detect_events('hi bob, I am hitting you with a stick.')
Out[5]:
[{'offset_start': 0, 'offset_end': 2, 'tag': 'O'},
 {'offset_start': 3, 'offset_end': 6, 'tag': 'O'},
 {'offset_start': 6, 'offset_end': 7, 'tag': 'O'},
 {'offset_start': 8, 'offset_end': 9, 'tag': 'O'},
 {'offset_start': 10, 'offset_end': 12, 'tag': 'O'},
 {'offset_start': 13, 'offset_end': 20, 'tag': 'B-action'},
 {'offset_start': 21, 'offset_end': 24, 'tag': 'O'},
 {'offset_start': 25, 'offset_end': 29, 'tag': 'O'},
 {'offset_start': 30, 'offset_end': 31, 'tag': 'O'},
 {'offset_start': 32, 'offset_end': 37, 'tag': 'O'},
 {'offset_start': 37, 'offset_end': 38, 'tag': 'O'}]
```

offsets correspond to character spans

```
In [6]: 'hi bob, I am hitting you with a stick.'[13:20]
Out[6]: 'hitting'
```

## Delivery information

### Source Code

#### Service or integration code such as REST APIs or web applications

Contained [in this repository](./analytic.py).

#### Source code for model training

See [this file](./neuralnets/BiLSTM.py).

spacy: Available at the [spacy website][spacy-training].

### Models

#### Inventory of any open source / public models that were used

- [pre-trained model](https://drive.google.com/file/d/1jCcNCnH-7ymSBZ_F4uddfFBZCq7yakBn/view?usp=sharing)
- [S3](s3://qntfy-artifacts/EN_Events.h5)

Additionally, consult information on the [spacy models][spacy-models]
used for sentence splitting.

#### Information for how to obtain these models

Use a google drive client such as [gdrive](https://github.com/prasmussen/gdrive)
and download the above link.

Additionally, consult [this script](./dependencies.sh) or above
spacy site to download the spacy models.

### Documentation

#### Reference information on the model or algorithm that is used for each analytic

[Paper with description of the model](https://www.aclweb.org/anthology/D17-1035/).

#### Documentation on how to train and deploy new models

Training: see [this file](./neuralnets/BiLSTM.py).

Deployment: Use the `MODEL_PATH` environment variable to point the
application to other models.

#### Information on data cleaning, preparation, or formatting that is required for each model

Available [here](./model.py).

spacy: available at the [spacy website][spacy-models].

### Data

This model was not trained on data provided by TwoSix.

[spacy-training]: https://spacy.io/usage/training
[spacy-models]: https://spacy.io/models/en
# Qntfy event analytic

Simple python-based analytic for tagging events in documents. Complies
with CDR schema.

## Introduction

This project uses Python, Flask and gunicorn in order to respond to incoming
RESTful (HTTP) requests. Generally, the service takes in CDR-schema JSON and
returns CDR-compliant annotations.

By default it binds to `0.0.0.0` and uses port `45000`. This port can
be overriden by setting the environment variable `ANALYTIC_PORT` to a
port-like integer in the docker run command.

Currently all logging is done via standard out.

The health of the service can be interrogated by issuing an `HTTP GET`
request to:

```
hostname:port/api/v1/health
```

which should return a JSON object containing the string `healthy` if
everything is OK, or an error if not.

## About the analytic

This analytic provides extraction of temporal expressions according to
a reduced `TimeML` ontology
([reference](https://www.aclweb.org/anthology/S13-2001.pdf)),
providing a single annotation type `B-action` for all expressions of
this type.

The output of the model is an `offset` (containing a `start`, inclusive,
and an `end`, exclusive) that can be used to extract the exact text from
the document. Because this can balloon document size, this extraction
is not included in the analytic, but could be included in a post-processing
step, which TwoSix is currently doing.

The offsets also contain a `tag`, which is a description of the segment of text.

