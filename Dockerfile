ARG BUILD_FROM
FROM $BUILD_FROM

# Install requirements for add-on
RUN apk add --no-cache \
    python3 \
    py3-pip

RUN pip3 install --no-cache-dir \
    pillow

# Copy data for add-on
COPY run.sh /
COPY metadata_remover.py /

RUN chmod a+x /run.sh

CMD ["/run.sh"]
