FROM python:3.7-buster
EXPOSE 8502
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY .. .
RUN bash setup_docker.sh
CMD ["streamlit", "run", "app.py"]
