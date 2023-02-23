FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y netcat && \
    apt-get clean

WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/
# Copy Nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Create the media folder
RUN mkdir /code/media

# Set permissions for the media folder
RUN chown -R www-data:www-data /code/media

# Expose port 80 for Nginx
EXPOSE 80