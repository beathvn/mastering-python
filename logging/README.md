# Logging

This directory contains info about logging and how to log to azure - therefore we build a mini logging framework that can be easily extended and used across different services.

build the docker image

>[!note]
> make sure you are inside the logging directory before running the following command

```shell
docker build -t logging:latest .
```

```shell
docker run --network host logging:latest
```
