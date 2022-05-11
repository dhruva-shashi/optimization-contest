def get_leaderboard(leaderboard):
    '''Method which returns the HTML text which contains the leaderboard'''

    html_text = '''
        <html>
            <head>
                <title>Hash it Out Final Round</title>
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
                <div id="content">
                    <table>
                        <tr style="background-color: #000000;color: #ffffff;">
                            <th>Rank</th>
                            <th>Team</th>
                            <th>A</th>
                            <th>B</th>
                            <th>C</th>
                            <th>D</th>
                            <th>E</th>
                            <th>Score</th>
                            <th>Timestamp</th>
                        <tr>
                '''

    # Write the score of each team onto the table
    for i in range(1, len(leaderboard)+1):
        html_text += '''
            <tr>
                <td>%d</td>
                <td>%s</td>
                <td>%d</td>
                <td>%d</td>
                <td>%d</td>
                <td>%d</td>
                <td>%d</td>
                <td>%d</td>
                <td>%f</td>
            </tr>
        ''' % (i, leaderboard[i-1][3], leaderboard[i-1][2][0], leaderboard[i-1][2][1], leaderboard[i-1][2][2], leaderboard[i-1][2][3], leaderboard[i-1][2][4], leaderboard[i-1][0], -leaderboard[i-1][1])

    html_text += '''
                </table>
            </div>
        </body>
    </html>
    '''

    return html_text
