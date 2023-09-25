FROM ubuntu:latest
# Install corn
RUN apt-get update && apt-get -y install cron && apt-get -y install python3.11 && apt-get -y install pip && apt-get -y install python3-dev libpq-dev
# Create the log file to be able to run tail
RUN touch /var/log/cron.log
# Install python
RUN apt-get -y install python3.11
# Setup cron job
RUN (crontab -l ; echo "* * * * * echo "Hello world" >> /var/log/cron.log") | crontab
# Run the command on container startup
CMD cron && tail -f /var/log/cron.log

WORKDIR /usr/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /usr/app/requirements.txt
RUN pip install -r requirements.txt