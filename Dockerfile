FROM python:3.8
ENV HOME /root
WORKDIR /root
COPY . /root
# Download dependancies
RUN pip install -r requirements.txt
# Change to other database if we'll use other
RUN python -m pip install pymongo
EXPOSE 8080

# Wait until the database server is connected
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

CMD /wait && python server.py