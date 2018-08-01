FROM python:3.6.6-slim

COPY ./requirements.txt /requirements.txt
COPY ./frontedge/* /frontedge/
COPY ./stream_counter/* /stream_counter/
COPY ./stream_register/* /stream_register/
COPY ./docker_entrypoint.sh /docker_entrypoint.sh

RUN pip3 install -r requirements.txt
RUN python3 /stream_register/setup.py install
RUN python3 /stream_counter/setup.py install

CMD ./docker_entrypoint.sh
