# Optimization Contest

## Overview

- The repository contains the logisitics required for conducting an optimization contest which is similar to Google Hash Code.
- The code is written using Python, and uses [bottle](https://bottlepy.org/docs/dev/) framework, which is a lightweight WSGI micro web-framework for Python.

## Instructions for Setup

### Firebase 

- Create a Firebase project and create a realtime database and storage.
- Write the config JSON data of the Firebase realtime database to the file "database_config.json".
- Write the config JSON data of the Firebase storage to the file "storage_config.json".

### Passcodes

- For each team, a passcode must be generated.
- In the Python file, "gen_passcode.py", enter comma seperated teamnames into the list on line 26 and run the code.
- The passcodes for each team will be generated randomly and is written to the file "team-passcode-mapping.json".

### Problem Statement

- Write the problem statement and save it in a PDF file named "problem-statement.pdf".
- Replace the file in the repository with the PDF file containing the problem statment.

### Evaluator

- The "evaluator.py" contains the code which evaluates the score for an output file.
- The code to evaluate the score must be written in the section which is indicated by comment.

### Deployment

- The app must be deployed in Heroku.
- Documentation for deploying Bottle web app in Heroku: [https://github.com/chucknado/bottle_heroku_tutorial](https://github.com/chucknado/bottle_heroku_tutorial)

