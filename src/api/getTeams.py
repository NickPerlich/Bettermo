import requests
import sys
from unidecode import unidecode


def fetch_team_data():
    url = "https://fantasy.premierleague.com/api/bootstrap-static"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        data = response.json()  # Parse the JSON response

        keys = []
        for key in data["teams"][0]:
            keys.append(key)

        teams = []
        for i in data["teams"]:
            teams.append(get_team_info(i, keys))
        
        return teams
        
    except requests.exceptions.RequestException as e:
        print("Error occurred:", e)



def get_team_info(team_data, keys):
    team = {}

    team["name"] = team_data['name']
    team["code"] = team_data['code']
    team["id"] = team_data['id']
    team["loss"] = team_data['loss']
    team["played"] = team_data['played']
    team["points"] = team_data['points']
    team["position"] = team_data['position']
    team["short_name"] = team_data['short_name']
    team["strength"] = team_data['strength']
    team["win"] = team_data['win']
    team["strength_overall_home"] = team_data['strength_overall_home']
    team["strength_overall_away"] = team_data['strength_overall_away']
    team["strength_attack_home"] = team_data['strength_attack_home']
    team["strength_attack_away"] = team_data['strength_attack_away']
    team["strength_defence_home"] = team_data['strength_defence_home']
    team["strength_defence_away"] = team_data['strength_defence_away']

    return team

