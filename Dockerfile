FROM python:3.8
ENV HOME /root
WORKDIR /root
COPY . /root
# Download dependancies
RUN pip install -r requirements.txt
# Change to other database if we'll use other
#RUN python -m pip install pymongo

# Install mysql python connector in the container. Without this, our mysql.connector libraries won't work
RUN pip install mysql-connector-python
EXPOSE 8080

# Wait until the database server is connected
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait
# CMD /wait && python main.py

CMD ["python", "main.py"]