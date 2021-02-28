FROM docker.io/library/python:3.7.10-alpine3.12

ENV WORKDIR /usr/src/app
ENV PY_APP rpiwepd

WORKDIR $WORKDIR

COPY ./requirements.txt $WORKDIR
RUN apk update && \
    apk add --no-cache --virtual build-deps libjpeg gcc g++ python3-dev linux-headers musl-dev jpeg-dev zlib-dev freetype-dev && \
    pip install -r requirements.txt
ADD ./$PY_APP $WORKDIR/$PY_APP
ADD ./static $WORKDIR/static
RUN /bin/echo -e "#!/bin/ash\npython $WORKDIR/$PY_APP/app.py" > /exec
RUN chmod a+x /exec

CMD ["/exec"]


