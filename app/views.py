# views.py

import nba_py as nba
import urllib2
import pycurl
import json
from flask import Response

from nba_py import player
from app import app

CURRENT_SEASON = '2017-18'
MEASURE_TYPES = ['advanced', 'base']
PER_TYPES = ['per36']
PACE_TYPES = ['per100']

@app.route('/')
def index():
	return 'Whassup'

@app.route('/players')
def players():
	player_list = player.PlayerList(season=CURRENT_SEASON).info()
	res = Response(json.dumps(player_list), mimetype='application/json')
	return res

@app.route('/giannis')
def giannis():
	giannis_id = player.get_player('Giannis', 'Antetokounmpo')
	res = Response(json.dumps(player.PlayerSummary(giannis_id).info()), mimetype='application/json')
	return res

@app.route('/players/<player_id>/<stats_type>')
def player_detail(player_id, stats_type):
	if (stats_type in MEASURE_TYPES):
		player_info = player.PlayerGeneralSplits(player_id, season=CURRENT_SEASON, measure_type=stats_type.title()).overall()
	elif (stats_type in PER_TYPES):
		player_info = player.PlayerGeneralSplits(player_id, season=CURRENT_SEASON, per_mode='Per36').overall()
	elif (stats_type in PACE_TYPES):
		player_info = player.PlayerGeneralSplits(player_id, season=CURRENT_SEASON, pace_adjust='Y').overall()
	else:
		return "WHAT THE FUCK"
	res = Response(json.dumps(player_info), mimetype='application/json')
	return res