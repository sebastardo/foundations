FROM python:3.7.5-slim
VOLUME /script
RUN python -m pip install --upgrade pip
RUN pip install psycopg2-binary &&\
    pip install pandas &&\
    pip install SQLAlchemy
COPY ./script /script
CMD ["python","/script/carga.py"]