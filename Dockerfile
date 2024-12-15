FROM python

ENV CALC_PORT=8888

COPY server.py ./

ENTRYPOINT ["python","server.py"]