FROM python:3.9-slim-buster

# Install pipenv
RUN apt-get update && apt-get install -y python3-pip && pip3 install pipenv

# Copy and install the project dependencies
COPY Pipfile* /tmp/
WORKDIR /tmp
RUN pipenv requirements > requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy the application code into the container
COPY . /app/
WORKDIR /app/

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# runs the production server
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
