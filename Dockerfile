FROM docker.io/library/python:3.7.10-alpine3.12

ENV WORKDIR /usr/src/app
ENV PY_APP rpiwepd

WORKDIR $WORKDIR

COPY ./requirements.txt $WORKDIR
RUN apk update && \
    apk add --no-cache --virtual build-deps gcc python3-dev linux-headers musl-dev jpeg-dev zlib-dev libjpeg && \
    pip install -r requirements.txt && \
    apk del build-deps
ADD ./$PY_APP $WORKDIR/$PY_APP
RUN /bin/echo -e "#!/bin/ash\npython $WORKDIR/$PY_APP/app.py" > /exec
RUN chmod a+x /exec

USER 1001

CMD ["/exec"]


