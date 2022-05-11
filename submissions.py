import pyrebase
import json


def get_submission(passcode):
    f = open('database_config.json', 'r')
    database_config = json.load(f)
    f.close()

    # Initialize firebase database
    database = pyrebase.initialize_app(database_config).database()

    # Retrieve information of all submissions made by the team
    info = database.child(passcode).get().val()

    # If info is None, then there are no submission made
    if not info:
        return '''No submissions made'''

    html_text = '''
        <html>
            <head>
                <title>Hash it Out Submissions</title>
                <style>
                    body {
                        font-family: verdana, sans-serif;
                        text-align: center;
                    }

                    #contest-name {
                        margin-top: 50px;
                        font-weight: bold;
                        font-size: 32px;
                    }

                    #contest-link {
                        margin-top: 50px;
                    }

                    #last-updated {
                        margin-top: 20px;
                    }

                    table {
                        margin-top: 50px;
                        margin-left: auto;
                        margin-right: auto;
                        margin-bottom: 100px;
                    }

                    th, td {
                        padding: 5px;
                        padding-left: 20px;
                        padding-right: 20px;
                    }

                    tr:nth-child(odd) {
                        background-color: #e8e8e8;
                    }

                    .team-members {
                        font-size: 12px;
                        margin-top: 5px;
                    }

                    .team-info {
                        max-width: 250px;
                    }

                    .problem-link {
                        color: #FFFFFF;
                    }

                    .right {
                        text-align: right;
                    }
                </style>
            </head>
            
            <body>
                <table>
                    <tr style="background-color: #000000;color: #ffffff;">
                        <th>Submission</th>
                        <th>Input</th>
                        <th>Code file</th>
                        <th>Output file</th>
                        <th>Verdict</th>
                        <th>Points</th>
                        <th>Date and Time of submission</th>
                    </tr>
    '''

    # Write the submission details such as submission number, input number,
    # path for code file and output files, points for the respective submission
    for i in range(1, len(info)):
        html_text += '''
            <tr>
                <td>%d</td>
                <td>%s</td>
                <td><a href="%s" download>Download</a></td>
                <td><a href="%s" download="output.txt">Download</a></td>
                <td>%s</td>
                <td>%d</td>
                <td>%s</td>
            </tr>
        ''' % (i,
               info[i]['input-number'],
               info[i]['code-file-path'],
               info[i]['output-path'],
               info[i]['submission-verdict']['result'] if info[i]['submission-verdict']['result'] == 'AC' else info[i]['submission-verdict']['result']+': '+info[i]['submission-verdict']['error'],
               info[i]['submission-verdict']['points'],
               info[i]['date-and-time'])

    html_text += '''
                </table>
            </div>
        </body>
    </html>
    '''

    return html_text
