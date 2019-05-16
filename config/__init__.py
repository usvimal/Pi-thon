import os

from discord import ActivityType
from xml.etree import ElementTree

# Set at default values for when config.xml or parsing xml fails
# There are also other variables which are not defined here, but will be defined dynamically in _load()
cogs = []
games, gamestimer = [], 200


def _load():
	tree = ElementTree.parse(r"config/config.xml")
	root = tree.getroot()

	_load_environment(root.find("environment"))
	_load_settings(root.find("settings"))
	_load_cogs(root.find("cogs"))
	_load_games(root.find("games"))


def _load_environment(env_element):
	for child in env_element:
		value_type = child.get("type")
		value = os.environ.get(child.text)

		if value_type == "str":
			value = str(value)
		elif value_type == "int":
			value = int(value)

		globals()[child.text] = value


def _load_settings(settings_element):
	# More flexibility can be gained from removing for loop and adding one-by-one
	for child in settings_element:
		globals()[child.tag] = child.text


def _load_cogs(cogs_element):
	for child in cogs_element:
		if child.get("activated") == "True":
			cogs.append(child.text)


def _load_games(games_element):
	for child in games_element:
		activity_type = child.get("activity_type")

		if activity_type == "playing":
			activity_type = ActivityType.playing
		elif activity_type == "watching":
			activity_type = ActivityType.watching
		elif activity_type == "listening":
			activity_type = ActivityType.listening

		games.append((activity_type, child.text))


# Load and then cleanup unnecessary modules
_load()
del os, ActivityType, ElementTree
