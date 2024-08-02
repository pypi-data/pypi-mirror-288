ARG PROXY_REGISTRY=
FROM ${PROXY_REGISTRY}python:3.10-alpine as base


### Builder ###
FROM base as builder

RUN mkdir /install
WORKDIR /install

COPY ./dist/* /dist/

RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-warn-script-location --prefix=/install /dist/*.whl


### Release ###
FROM base

COPY --from=builder /install /usr/local
RUN mkdir -p /quackamollie/logs
RUN addgroup -S quackamollie && adduser -S -G quackamollie quackamollie
RUN chown quackamollie:quackamollie /quackamollie
RUN chown quackamollie:quackamollie /quackamollie/logs

USER quackamollie:quackamollie

WORKDIR /quackamollie-core
COPY --chown=quackamollie:quackamollie ./migrations/env.py ./migrations/script.py.mako /quackamollie-core/migrations/
COPY --chown=quackamollie:quackamollie ./migrations/versions/*.py /quackamollie-core/migrations/versions/
COPY --chown=quackamollie:quackamollie alembic.ini /quackamollie-core/


ENTRYPOINT ["quackamollie"]
CMD ["-vv", "-l", "/quackamollie/logs ", "serve"]
