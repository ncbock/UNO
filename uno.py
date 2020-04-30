import pygame
from random import shuffle

#RGB Colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
gold = (212,175,55)
red = (255, 0, 0)
blue = (0, 0, 255)

clock = pygame.time.Clock()


def main():
    pygame.init()
    window = pygame.display.set_mode((750,750))
    count = 0
    round = 0

    players = getPlayers()

    playTurn = 0

    while True:
        player = 0
        pos = pygame.mouse.get_pos()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.MOUSEBUTTONDOWN and count < 1:
                if pos[0] in range(300,451) and pos[1] in range(450,501):
                    count += 1
            if e.type == pygame.MOUSEBUTTONDOWN and count > 0 :
                if pos[0] in range(50,201) and pos[1] in range(50,101):
                    playTurn += 1
                    if playTurn == len(players):
                        playTurn = 0


        #Display all info after this point
        window.fill(white)
        startButton(window,count)
        displayUNO(window,count)
        whoseTurn(window, count, playTurn, players)
        playCardButton(window,count)
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

def getPlayers():
    numPlayers = int(input("How many Players?  "))
    players = []
    for i in range(numPlayers):
        playerName = input("Player {} what is your name?  ".format(i+1))
        players.append(playerName)
    return players

# status = {}

# for player in players:
#     status[player] = {"score": 0, "hand": []}

# for i in range(7):
#     for player in players:
#         status[player]["hand"].append(cardDeck[0])
#         cardDeck.pop(0)

# discardPile = cardDeck.pop(0)


def startButton(window, count):
    font = pygame.font.SysFont("arial", 35)
    pos = pygame.mouse.get_pos()
    if count < 1:
        buttonColor = black
        buttonSize = 2
        if pos[0] in range(300,451):
            if pos[1] in range (450,501):
                buttonColor = green
                buttonSize = 4
        pygame.draw.rect(window,buttonColor, (300,450,150,50),buttonSize)
        start = font.render("START", 1, black)
        window.blit(start,(318,458))

def displayUNO(window, count):
    if count < 1:
        font = pygame.font.SysFont("arial", 200)
        uno= font.render("UNO!", 1, gold)
        window.blit(uno,(125, 200))

def whoseTurn(window, count, turn, playerList):
    if count > 0:
        font = pygame.font.SysFont("arial", 45)
        player = playerList[turn]
        playerTurn = font.render("{} it's your turn!".format(player), 1, gold)
        window.blit(playerTurn,(300,50))

def playCardButton(window, count):
    if count > 0:
        font = pygame.font.SysFont("arial",30)
        pos = pygame.mouse.get_pos()
        buttonColor = black
        buttonSize = 2
        if pos[0] in range(50,201) and pos[1] in range(50,101):
            buttonColor = green
            buttonSize = 4
        pygame.draw.rect(window, buttonColor, (50,50,150,50),buttonSize)
        playCard = font.render("Play Card", 1, black)
        window.blit(playCard, (65,65))

if __name__=="__main__":
    main()
    pygame.quit()



     