FROM python:3.10 as dev

WORKDIR /app

COPY ./build/streamlit/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt


COPY ./src/streamlit /app

CMD ["streamlit", "run", "streamlit_app.py"]
