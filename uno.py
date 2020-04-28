from random import shuffle

def createDeck():
    deck = []
    colors = ["red", "yellow", "green", "blue"]
    wild = "wild"
    plusFour = "+4"
    actions = ["skip", "reverse", "+2"]
    for i in range(2):
        for color in colors:
            #There is only 1 "0" card per color, 4 wild cards, and 4 "+4 cards" in the deck
            #All other cards have 2 cards per color
            if i < 1:
                for card in range(10):
                    deck.append(color + " " + str(card))
                deck.append(wild)
            else:
                for card in range(1,10):
                    deck.append(color + " " + str(card))
                deck.append(plusFour)
            for card in actions:
                deck.append(color + " " + str(card))
    shuffle(deck)
    return deck

cardDeck = createDeck()

def getPlayers():
    numPlayers = int(input("How many Players?\n"))
    players = []
    for i in range(numPlayers):
        playerName = input("Player {} what is your name?  ".format(i+1))
        players.append(playerName)
    return players


hands = {}

for player in players:
    hands[player] = []


for i in range(7):
    for player in players:
        hands[player].append(cardDeck[0])
        cardDeck.pop(0)




