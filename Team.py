from evaluator import *
import datetime
import pyrebase
import time
import json
import os


# Initialize the firebase storage config
f = open('storage_config.json', 'r')
storage_config = json.load(f)
f.close()

# Initialize the firebase database config
f = open('database_config.json', 'r')
database_config = json.load(f)
f.close()

storage = pyrebase.initialize_app(storage_config).storage()
database = pyrebase.initialize_app(database_config).database()


class Attempt:
    def __init__(self, submission_number, input_number, code_file_path, output_file_path):
        self.submission_number = submission_number
        self.input_number = chr(ord('A')+input_number-1)
        self.code_file_path = 'code-file/'+code_file_path
        self.output_path = 'output-file/'+output_file_path
        self.submission_verdict = evaluate('input-files/input-%s.txt' % chr(ord('a')+input_number-1), output_file_path)
        self.date_and_time = '%s %s' % (datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), time.tzname[0])

    def get_details(self):
        '''Return a dictionary containing all the information of the submission'''

        return {
            'submission-number': self.submission_number,
            'input-number': self.input_number,
            'code-file-path': self.code_file_path,
            'output-path': self.output_path,
            'submission-verdict': self.submission_verdict,
            'date-and-time': self.date_and_time
        }


class Team:
    def __init__(self, passcode, teamname):
        self.passcode = passcode
        self.teamname = teamname
        self.score = [0, 0, 0, 0, 0]
        self.number_of_attempts = 0
        self.last_time = 0

    def get_details(self):
        '''Return a dictionary containing all the information of the team'''

        return {
            'teamname': self.teamname,
            'score': self.score,
            'total-score': sum(self.score)
        }

    def make_attempt(self, input_number, code_file_path, output_file_path, number_of_attempts):
        current_attempt = Attempt(number_of_attempts, input_number, code_file_path, output_file_path)

        # Write the submission details to firebase
        database.child(self.passcode).child(number_of_attempts).set(current_attempt.get_details())

        f = open(output_file_path, 'r')
        output_text = f.read()
        f.close()

        # Delete file after reading
        os.remove(output_file_path)

        # Write the output file contents to firebase
        database.child('submissions').child(self.passcode).child('output-%d' % number_of_attempts).set(output_text)

        if current_attempt.submission_verdict['result'] == 'AC' and current_attempt.submission_verdict['points'] > self.score[input_number-1]:
            self.score[input_number-1] = current_attempt.submission_verdict['points']
            self.last_time = time.time()
