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
Currently, this is a single tag `B-action` for all tagged events.
