FROM python:3-slim as builder
WORKDIR /pipfiles

# INSTALL THE BUILD DEP.
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev gcc libc-dev && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -U setuptools wheel

# INSTALL PIPENV
RUN set -ex && pip install pipenv --upgrade

# INSTALL DEPENDENCIES
COPY Pipfile* ./
RUN set -ex && pipenv lock -r > req.txt && pip install --no-cache-dir -r req.txt

FROM builder as final
ENV PYTHONUNBUFFERED=1
WORKDIR /

# COPY APP SOURCE CODE
COPY . /api

CMD ["hypercorn", "api.main:app", "-b", "0.0.0.0:3000"]