import json
import FlaskApi
a = '[[{"id":"28856300","username":"Taiiwo","values":[[0],[0]]},{"id":"28375468","username":"warlord","values":[[5],[1]]}],[[[0,1,2],[0]],[[3,4,5],[1]],[[1,2],[3]]]]'
data = json.loads(a)
team = [
    {
        "values": [[0,], [0,]]
    },
    {
        "values": [[5,], [1,]]
    }
]
requirements = [
    [[0,1,2], [0,]],
    [[4,5,6], [1,]],
    [[5,], [2,]],
]

team = data[0]
requirements = data[1]
print FlaskApi.check_team(team, requirements)
