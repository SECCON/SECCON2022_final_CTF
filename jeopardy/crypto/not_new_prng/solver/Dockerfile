FROM sagemath/sagemath:latest

RUN sage -pip install pycryptodome

WORKDIR /app
USER root
ADD . /app

CMD ["sage", "exploit.sage"]