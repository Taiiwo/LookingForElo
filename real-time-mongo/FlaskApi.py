from time import time
from RTM import RTM
from flask import Flask
from flask.ext.cors import CORS
import json
import util

app = Flask(__name__)
CORS(app)
rtm = RTM()
util = util.Util()

# Sends a message by storing in the database.
@app.route('/send')
def send_message():
    if request.method == "POST":
        data = str(request.form['data'])
        sender_pair = request.form['sender_pair']
        recipient = request.form['recipient']
        collection = "messages"
        
        rtm.send(data, sender_pair, recipient, collection)

@app.route('/check', methods=["POST"])
def check_for_summoners():
    team = json.loads(request.form['team'])
    requirements = json.loads(request.form['requirements'])
    # search the database for group(s) that match requirements
    i = 0
    db_cache = {}
    check_cache = {}
    for team_combinations in make_list(len(requirements)):
        possible_team = []
        for i in team_combinations:
            # get all groups with i number of members
            if i in db_cache:
                groups = db_cache[i]
            else:
                groups = util.db['teams_waiting'].find({"team": {"size": i}})
                db_cache[i] = groups
            for group in groups:
                # check if we match their requirements
                if group["_id"] in check_cache:
                    check = check_cache[group['_id']]
                else:
                    check = check_team(team, group['requirements'])
                    check_cache[group['_id']] = check
                if check:
                    possible_team += group['members']
        if len(possible_team) == len(requirements):
            if check_team(possible_team, requirements):
                return possible_team

@app.route('/test')
def test():
    return "ayylmao"
            
        

@app.route('/add_recipient')
def add_recipient():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        password1 = request.form['password']
        
        if password == password1:
            if rtm.add_recipient(username, password):
                return True
        return False

# Makes a list of combinations that add up to `length` with each value under
# `length`
def make_list(length):
    lists = [[length]]
    for s in range(1, length + 1):
        rem = length - s
        if rem == 0:
          continue
        for l in make_list(rem):
            x = [s]
            x.extend(l)
            x.sort(reverse=True)
            lists.append(x)
        strict_lists = []
        for l in lists:
            if l not in strict_lists:
                strict_lists.append(l)
                yield l

# utility function that checks if a team meets a set of requirements
def check_team(team, requirements):
    user_roles = {}
    # for each member of the team
    for index, member in enumerate(team):
        # look through each requirement
        for requirement in requirements:
            # if the rank is allowed
            if member['values'][0][0] in requirement[0]:
                # then look through the roles
                for role in member['values'][1]:
                    # if the role is one of the valid ones
                    if role in requirement[1]:
                        user_roles[role] = index
    # check if there are no duplicates
    # (As each player can only play one role at a time)
    if len(user_roles) == len(team):
        return len(user_roles) == len(set(user_roles))
    else:
        return False

@app.route('/')
def index():
    return 'Index Page!'

if __name__ == '__main__':
    app.run(debug=True)
