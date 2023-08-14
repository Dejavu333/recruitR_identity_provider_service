FROM python:3.9-slim

RUN pip install schemathesis

ENTRYPOINT ["schemathesis", "run"]
#

# docker build -t schematest:latest -f ./schematest.dockerfile /.

# docker run -v /absolute/path/on/host/docs:/docs schematest run /docs/OAS.json --base-url=http://service_url:port
# docker run -v ${PWD}\docs:/docs schematest:latest /docs/OAS.json --base-url=http://host.docker.internal:6000
