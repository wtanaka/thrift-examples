FROM wtanaka/trusty32
ENV THRIFT_VERSION 0.9.2
RUN \
   apt-get update -q \
   && apt-get remove -qy python3 python3-minimal \
   && apt-get install -qy wget build-essential \
   && apt-get install -qy python2.7 python2.7-dev \
   && wget -O - \
      http://mirrors.ibiblio.org/apache/thrift/$THRIFT_VERSION/thrift-$THRIFT_VERSION.tar.gz \
      | gzip -d -c | tar xvf - \
   && cd thrift-$THRIFT_VERSION \
   && ./configure \
   && make \
   && make install \
   && cd .. \
   && rm -rf thrift-$THRIFT_VERSION \
   && apt-get remove -y wget build-essential python2.7-dev \
   && apt-get autoremove -y \
   && apt-get clean \
   && apt-get purge
WORKDIR /tmp
COPY typecheck.thrift /tmp/
RUN thrift -r --gen py typecheck.thrift
COPY tcheck.py /tmp/
CMD ["env", \
  "PYTHONPATH=/usr/lib/python2.7/site-packages:/tmp/gen-py:/tmp", \
  "python2.7"]
