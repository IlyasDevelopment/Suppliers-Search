FROM python:3
ENV PYTHONUNBUFFERED 1

RUN mkdir /opt/dash

WORKDIR /opt/dash

COPY requirements.txt /opt/dash/

RUN pip install -r requirements.txt

COPY . /opt/dash/

CMD ["streamlit", "run", "app.py", "--server.port", "8080"]
