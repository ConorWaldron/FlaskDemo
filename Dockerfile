# picking a base image
FROM python:3.8

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files, folders and files in those folders to the container,
# needed so app has access to previous_week.csv, teams.csv and subs.csv
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the SECRET_KEY environment variable, note you need to pass the environment variable when you use docker run as shown below
# docker run -d -p 8888:5000 -e FLASK_DEMO_SECRET_KEY=5791628bb0b13ce0c676dfde280ba245 conorwaldron512/flask_webapp:1.0
ENV FLASK_DEMO_SECRET_KEY placeholder_to_be_overwritten

# tell the port number the container should expose
EXPOSE 5000

# Set the working directory to the app folder, this will ensure relative paths work in the same way as if you clicked run on app.py
WORKDIR /usr/src/app

# run the command, run python and then point at the python script for your app
CMD ["python", "./run.py"]