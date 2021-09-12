import json

'''
coin system

uses json bc im bad at sql and stuff


bottom text
'''
def saveChanges(changes: dict):
	with open("static/js/coins.json", "w") as coin_:
		json.dump(changes, coin_)

def addCoins(userID, coinsAmount: int):
    with open("static/js/coins.json") as coin:
        coins = json.load(coin)
    if userID in coins:
        if coins[userID] <= coinsAmount:
            if coins is None:
                return
            elif coins is not None:
                coins[userID] = coinsAmount
                saveChanges(coins)
        elif coins[userID] > coinsAmount:
            coins[userID] += 1
    elif userID not in coins:
        coins[userID] = 1
    saveChanges(coins)

def checkIfExists(discordUserId):
    with open("static/js/coins.json") as coin:
        coins = json.load(coin)
    if discordUserId in coins:
        pass
    elif discordUserId not in coins:
        coins[str(discordUserId)] = 1

def removeCoins(userID, coinsToRemove: int):
    with open("static/js/coins.json") as coin:
        coins = json.load(coin)
    try:
        if userID in coins:
            if coins[userID] <= coinsToRemove:
                return False
            elif coins[userID] > coinsToRemove:
                coins[userID] = coins[userID] - coinsToRemove
                return True
        elif userID not in coins:
            coins[userID] = 1
            return False
    except KeyError:
        return False
    except IndexError:
        return False

    saveChanges(coins)
