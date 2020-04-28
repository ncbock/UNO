import pygame
from random import shuffle

#RGB Colors
white = (255, 255, 255)
black = (0, 0, 0)

clock = pygame.time.Clock()

def main():
    pygame.init()
    window = pygame.display.set_mode((750,750))

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return

        #Display all info after this point
        window.fill(white)


        #Update the Display
        pygame.display.update()
        clock.tick(60)

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

players = getPlayers()  
status = {}

for player in players:
    status[player] = {"score": 0, "hand": []}

for i in range(7):
    for player in players:
        status[player]["hand"].append(cardDeck[0])
        cardDeck.pop(0)

discardPile = cardDeck.pop(0)

if __name__=="__main__":
    main()
    pygame.quit()



     