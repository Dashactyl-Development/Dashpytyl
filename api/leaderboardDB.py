import json
'''
coin leaderboard system

also made in json but its just to store userIDs to usernames :D



bottom text
'''
with open('api/usernameToUserID.json') as leaderboardjsonfile:
	leaderboardList = json.load(leaderboardjsonfile)

def savechanges(changes):
	with open("api/usernameToUserID.json", "w") as leaderboard:
		json.dump(changes, leaderboard)


def checkifexists(discordID, discordUsername):
	try:
		if leaderboardList[str(discordID)] is not None:
			pass
		elif leaderboardList[str(discordID)] is not None and leaderboardList[str(discordID)] is not discordUsername:
			leaderboardList[str(discordID)] = discordUsername
	
	except KeyError:
		leaderboardList[str(discordID)] = str(discordUsername)
		savechanges(leaderboardList)