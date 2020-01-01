import requests
from app.models import Team, Position, Player, HitterStats, PitcherStats


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
    Position.objects.create(scoring_code=0,
                            name='Designated Hitter',
                            abbrev='DH')


def add_hitters(num, year='2019'):
    """Creates Player model objects from MLB.com stats sorted by top
    OPS (On base percentage + slugging). Returns the top {num} of players"""
    response = requests.request('GET', "http://lookup-service-prod.mlb.com/json/named.leader_hitting_repeater.bam?sport_code=mlb&results=" + str(num) + "&game_type='R'&season=" + str(year) + "&sort_column=ops")
    print(response.status_code)
    data = response.json()
    players = data['leader_hitting_repeater']['leader_hitting_mux']['queryResults']['row']
    for p in players:
        player_obj = Player(
            player_id=p['player_id'],
            name=p['name_display_first_last'],
            team=Team.objects.get(pk=p['team_abbrev']),
            position=Position.objects.get(abbrev=p['pos']),
            image="http://mlb.com/images/players/525x330/" + p['player_id'] + ".jpg"
        )
        player_obj.save()

        HitterStats(
            player=player_obj,
            avg=p['avg'],
            slg=p['slg'],
            ops=p['ops'],
            hits=p['h'],
            hr=p['hr'],
            rbi=p['rbi'],
            so=p['so'],
        ).save()


def add_pitchers(num, sort_by='era'):
    """Creates Pitcher model based on top stats sorted by either
    ERA, strikeouts, K/walk ratio, wins, or innings pitched."""
    if not sort_by in ('so', 'k_bb', 'w', 'ip'):
        sort_by = 'era'
    response = requests.request('GET', "http://lookup-service-prod.mlb.com/json/named.leader_pitching_repeater.bam?sport_code='mlb'&results=" + str(num) + "&game_type='R'&season='2019'&sort_column='" + sort_by + "'")
    print(response.status_code)
    data = response.json()
    pitchers = data['leader_pitching_repeater']['leader_pitching_mux']['queryResults']['row']
    for p in pitchers:
        player_obj = Player(
            player_id=p['player_id'],
            name=p['name_display_first_last'],
            team=Team.objects.get(pk=p['team_abbrev']),
            position=Position.objects.get(pk='P'),
            image="http://mlb.com/images/players/525x330/" + p['player_id'] + ".jpg"
        )
        player_obj.save()

        PitcherStats(
            player=player_obj,
            throws=p['throws'],
            k_per_9=p['k_9'],
            bb_per_9=p['bb_9'],
            k_bb=p['k_bb'],
            era=p['era'],
            innings=p['ip']
        ).save()