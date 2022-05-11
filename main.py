from bottle import run, get, post, route, request, static_file, template
from threading import Thread
from leaderboard import *
from submissions import *
from Team import Team
import datetime
import pyrebase
import time
import json
import os


# Initialize time keeper dictionary
f = open('time-keeper.json', 'r')
time_keeper = json.load(f)
f.close()

# Initialize the start time and duration of the contest
contest_start_time = time_keeper['contest-start-time']
contest_duration = time_keeper['contest-duration']

# Initialize the firebase storage config
f = open('storage_config.json', 'r')
storage_config = json.load(f)
f.close()

# Initialize the firebase database config
f = open('database_config.json', 'r')
database_config = json.load(f)
f.close()

# Intialize firebase storage and database
storage = pyrebase.initialize_app(storage_config).storage()
database = pyrebase.initialize_app(database_config).database()

# Retrieve all the team and passcode mappings
f = open('teams-passcode-mapping.json', 'r')
team_passcodes = json.load(f)
f.close()

# Create dictionary with team entity mapped to passcodes
teams = {}

for passcode in team_passcodes:
    teams[passcode] = Team(passcode, team_passcodes[passcode])


@route('/')
def index():
    return template('index.html')


@route('/user-manual')
def index():
    return template('user-manual.html')


@route('/styles/<filename>.css')
def style(filename):
    return static_file(filename+'.css', root='.')


@route('/scripts/<filename>.js')
def style(filename):
    return static_file(filename+'.js', root='.')


@route('/re-init')
def re_init():
    '''Endpoint which re-initialises the server'''

    if 'passcode' not in request.query:
        return {'error': 'Passcode not present'}

    passcode = request.query['passcode']

    if not passcode == 'EaQTc0DP3PhnXCnIuto9':
        return {'error': 'not authorized for this task'}

    full_db = database.get().val()

    for team in teams:
        if team in full_db:
            teams[team].number_of_attempts = len(full_db[team])-1


@get('/problem-statement.pdf')
def problem_statement():
    '''Endpoint which gives the problem statement PDF file'''

    if int(time.time()) < contest_start_time:
        return {'error': 'Contest has not started'}

    return static_file('problem-statement.pdf', root='.')


@get('/input-files/<filename>.txt')
def input_file(filename):
    '''Endpoint which gives the input files'''

    if int(time.time()) < contest_start_time:
        return {'error': 'Contest has not started'}

    return static_file(filename+'.txt', root='./input-files')


@get('/time-keeper')
def get_time_keeper():
    return {
        'contest-start-time': datetime.datetime.fromtimestamp(time_keeper['contest-start-time']).strftime('%Y-%m-%d %H:%M:%S'),
        'contest-duration': time_keeper['contest-duration']
    }


@get('/get-teamname')
def get_teamname():
    '''Method which verifies whether the passcode is valid '''

    passcode = request.query['passcode']

    if passcode in team_passcodes:
        return {'ok': True, 'teamname': team_passcodes[passcode]}
    else:
        return {'ok': False, 'error': 'Passcode does not exist'}


@route('/set-timings')
def set_timings():
    '''Endpoint for admin to change the timings of the contest'''

    if 'passcode' not in request.query:
        return {'error': 'Passcode not present'}

    passcode = request.query['passcode']

    if not passcode == 'EaQTc0DP3PhnXCnIuto9':
        return {'error': 'not authorized for this task'}

    global time_keeper, contest_start_time, contest_duration
    contest_start_time = int(request.query['start-time'])
    contest_duration = int(request.query['duration'])

    time_keeper['contest-start-time'] = contest_start_time
    time_keeper['contest-duration'] = contest_duration

    # Dump the new start time and duration to JSON file
    f = open('time-keeper.json', 'w')
    json.dump(time_keeper, f, indent=4)
    f.close()


@route('/reset')
def reset():
    '''Endpoint for admin to reset the database'''

    if 'passcode' not in request.query:
        return {'error': 'Passcode not present'}

    passcode = request.query['passcode']

    if not passcode == 'EaQTc0DP3PhnXCnIuto9':
        return {'error': 'not authorized for this task'}

    database.set({})


@route('/leaderboard')
def leaderboard():
    '''Routes to leaderboard of contest'''

    leaderboard_list = list()

    for team in teams:
        leaderboard_list.append([sum(teams[team].score), -teams[team].last_time, teams[team].score, teams[team].teamname])

    leaderboard_list.sort()
    leaderboard_list.reverse()

    # Return the HTML text
    return get_leaderboard(leaderboard_list)


@route('/my-submissions')
def my_submissions():
    '''Endpoint which returns the teams submissions'''

    if 'passcode' not in request.query:
        return {'error': 'Passcode not present'}

    passcode = request.query['passcode']

    if passcode not in teams:
        return {'error': 'Passcode does not exist'}

    # Return the HTML text
    return get_submission(passcode)


@post('/submission')
def submission():
    '''Endpoint to make a submission'''

    global contest_start_time, contest_duration

    # If contest has not started do not accept submissions
    if int(time.time()) < contest_start_time:
        return {'error': 'Contest has not started'}

    # If contest has ended do not accept submissions
    if int(time.time()) >= contest_start_time+(contest_duration*60):
        return {'error': 'Contest has ended'}

    files = list()

    passcode = request.forms.get('passcode')
    code_file = request.files.get('code-file')

    # If passcode has not been mentioned or wrong passcode has been given,
    # do not accept submissions
    if not passcode or passcode not in teams:
        return {'error': 'Please verify passcode'}

    # If there is no code file, do not accept the submission
    if not code_file:
        return {'error': 'Please upload code file'}

    # Ensure that each team submits 1 output file per minute
    if int(time.time()) < contest_start_time+(60*teams[passcode].number_of_attempts):
        return {'error': 'Submission limit exceeded. Please try after a few minutes'}

    # Count the number of files in the submission
    number_of_files = 0

    for i in range(1, 6):
        files.append(request.files.get('file%d' % i))
        if files[i-1]:
            number_of_files += 1

    # If the number of output files is 0, do not evaluate the submission
    if number_of_files == 0:
        return {'error': 'No output files found'}

    if not os.path.isdir(passcode):
        os.mkdir(passcode)

    # Initialize the file path for the code file and save the code file temporarily
    code_file_path = '%s/code-%d-%s' % (passcode, teams[passcode].number_of_attempts+1, code_file.filename)
    code_file.save(code_file_path)

    # Store the code file and delete the temporary code file
    storage.child(code_file_path).put(code_file_path)
    os.remove(code_file_path)

    score = []

    for i in range(0, 5):
        if not files[i]:
            score.append({'result': 'NF', 'points': 0})
        else:
            # For each output file, increase the number of attempts
            teams[passcode].number_of_attempts += 1

            # Initialize the path for output file and save the output file temporarily
            output_file_path = '%s/output-%d' % (passcode, teams[passcode].number_of_attempts)
            files[i].save(output_file_path)

            # Start a thread which makes a submission for an output file
            Thread(target=teams[passcode].make_attempt, args=(i+1, code_file_path, output_file_path, teams[passcode].number_of_attempts,)).start()

    return {'ok': True}


def delete_later(filename):
    '''Method which deletes a temporary file once score is evaluated'''

    # Wait for 3 seconds and delete the file
    time.sleep(3)
    os.remove(filename)


@get('/best-score')
def get_best_score():
    '''Method which returns the best score of a team'''

    if 'passcode' not in request.query:
        return {'error': 'Passcode not present'}

    passcode = request.query['passcode']

    if passcode not in teams:
        return {'error': 'Passcode does not exist'}

    return {'score': teams[passcode].score}


@get('/code-file/<passcode>/<filename>')
def get_code_file(passcode, filename):
    '''Endpoint which is used to fetch the code file for a submission'''

    if passcode not in teams:
        return {'error': 'passcode does not exist'}

    path_on_cloud = "%s/%s" % (passcode, filename)
    path_on_local = "%s/%s" % (passcode, filename)

    if not os.path.isdir(passcode):
        os.mkdir(passcode)

    # Temporarily store the code file and delete it later
    storage.child(path_on_cloud).download(filename=path_on_local, path='')
    Thread(target=delete_later, args=(path_on_local,)).start()

    return static_file(path_on_local, root='.')


@get('/output-file/<passcode>/<filename>')
def get_output_file(passcode, filename):
    '''Endpoint which is used to fetch the code file for a submission'''

    if passcode not in teams:
        return {'error': 'passcode does not exist'}

    # Return the output file as text
    output_text = database.child('submissions').child(passcode).child(filename).get().val()

    return output_text


if os.environ.get('APP_LOCATION') == 'heroku':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    run(host='localhost', port=8080, debug=True)
