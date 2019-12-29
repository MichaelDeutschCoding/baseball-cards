import requests
from app.models import Team, Position


def get_teams_list():
    response = requests.request('GET', 'http://lookup-service-prod.mlb.com/json/named.team_all_season.bam?sport_code=%27mlb%27&all_star_sw=%27N%27&sort_order=name_asc&season=2019')
    data = response.json()
    teams = data['team_all_season']['queryResults']['row']
    for team in teams:
        Team(name=team['name'],
             team_symbol=team['name_abbrev'],
             city=team['city'],
             state=team['state'],
             stadium=team['venue_name'],
             league=team['league']).save()


def add_positions():
    Position.objects.create(scoring_code=1,
                            name='Pitcher',
                            abbrev='P')
    Position.objects.create(scoring_code=2,
                            name='Catcher',
                            abbrev='C')
    Position.objects.create(scoring_code=3,
                            name='First Baseman',
                            abbrev='1B')
    Position.objects.create(scoring_code=4,
                            name='Second Baseman',
                            abbrev='2B')
    Position.objects.create(scoring_code=5,
                            name='Third Baseman',
                            abbrev='3B')
    Position.objects.create(scoring_code=6,
                            name='Shortstop',
                            abbrev='SS')
    Position.objects.create(scoring_code=7,
                            name='Left Fielder',
                            abbrev='LF')
    Position.objects.create(scoring_code=8,
                            name='Center Fielder',
                            abbrev='CF')
    Position.objects.create(scoring_code=9,
                            name='Right Fielder',
                            abbrev='RF')


get_teams_list()
