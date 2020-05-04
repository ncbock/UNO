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
    currentRound = 0
    nextRound = 1

    players = getPlayers()
    hands, deck = createHands(players)

    playTurn = 0
    while True:
        pos = pygame.mouse.get_pos()
        for e in pygame.event.get():
            #Close the window
            if e.type == pygame.QUIT:
                return
            #Start the Game
            if e.type == pygame.MOUSEBUTTONDOWN and count < 1:
                if pos[0] in range(300,451) and pos[1] in range(500,551):
                    count += 1
            #Play the slected Card, this needs expansion
            if e.type == pygame.MOUSEBUTTONDOWN and count > 0 :
                if pos[0] in range(50,201) and pos[1] in range(50,101):
                    playTurn += 1
                    if playTurn == len(players):
                        playTurn = 0
            #Add a card to the players hand when they draw a card, drawing a card is signaled by the mouse click event
            # in the location of the deck. 
            if e.type == pygame.MOUSEBUTTONDOWN and count > 0 and pos[0] in range(550,651) and pos[1] in range(275,476):
                hands[players[playTurn]].append(deck[0])
                deck.pop(0)


        #Display all info after this point
        window.fill(white)
        startButton(window,count)
        displayUNO(window,count)
        whoseTurn(window, count, playTurn, players)
        playCardButton(window,count)
        displayHand(window, players[playTurn], hands, count)
        drawCards(window, count)
        #Update the Display
        pygame.display.update()
        clock.tick(60)

def createDeck():
    deck = []
    colors = ["red", "gold", "green", "blue"]
    wild = "wild"
    plusFour = "+4"
    actions = ["skip", "reverse", "+2"]
    for i in range(2):
        for color in colors:
            #There is only 1 "0" card per color, 4 wild cards, and 4 "+4 cards" in the deck
            #All other cards have 2 cards per color
            if i < 1:
                for card in range(10):
                    deck.append(str(card) + " " + color)
                deck.append(wild)
            else:
                for card in range(1,10):
                    deck.append(str(card) + " " + color)
                deck.append(plusFour)
            for card in actions:
                deck.append(str(card) + " " + color)
    shuffle(deck)
    return deck

def getPlayers():
    numPlayers = int(input("How many Players?  "))
    players = []
    for i in range(numPlayers):
        playerName = input("Player {} what is your name?  ".format(i+1))
        players.append(playerName)
    return players

def createHands(players):
    deck = createDeck()
    #Dictionary will contain players, and a list with their hands
    currentHands = {}
    #Create the players and their empty hands.
    for player in players:
        currentHands[player] = []
    #Each player to recieve 7 cards, essentially deal the cards
    for i in range(7):
        for player in players:
            #Add first card of the shuffled deck to the players hand
            currentHands[player].append(deck[0])
            #Remove the added card from the deck
            deck.pop(0)

    return currentHands, deck
    
def startButton(window, count):
    font = pygame.font.SysFont("arial", 35)
    pos = pygame.mouse.get_pos()
    if count < 1:
        buttonColor = black
        buttonSize = 2
        if pos[0] in range(300,451):
            if pos[1] in range (500,551):
                buttonColor = green
                buttonSize = 4
        pygame.draw.rect(window,buttonColor, (300,500,150,50),buttonSize)
        start = font.render("START", 1, black)
        text_width, text_height = font.size("START")
        xstart = 300 + ((150 - text_width)/2)
        ystart = 500 + ((50 - text_height)/2)
        window.blit(start,(xstart, ystart))

def displayUNO(window, count):
    if count < 1:
        font = pygame.font.SysFont("arial", 200)
        uno= font.render("UNO!", 1, gold)
        text_width, text_height = font.size("UNO!")
        xstart = (750- text_width)/2
        ystart = (750 -text_height)/2
        window.blit(uno,(xstart, ystart))

def whoseTurn(window, count, turn, playerList):
    if count > 0:
        font = pygame.font.SysFont("arial", 45)
        player = playerList[turn]
        playerTurn = font.render("{} it's your turn!".format(player), 1, gold)
        window.blit(playerTurn,(215,50))

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
        text_width, text_height = font.size("Play Card")
        xstart = 50 + ((150-text_width)/2)
        ystart = 50 + ((50-text_height)/2)
        window.blit(playCard, (xstart, ystart))

def displayHand(window, player, hand, count):
    if count > 0:
        font = pygame.font.SysFont("arial", 35)
        xstart = 215
        ystart = 125
        for cards in hand[player]:
            currentCard = cards.split(" ")
            if len(currentCard) == 2:
                if currentCard[1] == "red":
                    color = red
                elif currentCard[1] == "green":
                    color = green
                elif currentCard[1] == "blue":
                    color = blue
                else:
                    color = gold
                playersCard = font.render(currentCard[0],1,color)
            else:
                playersCard = font.render(currentCard[0],1,black)
            text_width, text_height = font.size(currentCard[0])
            if xstart + text_width < 725:
                window.blit(playersCard, (xstart,ystart))
                xstart = xstart + text_width + 15
            else: 
                xstart = 215
                ystart = ystart + text_width + 15
                window.blit(playersCard, (xstart,ystart))

def drawCards(window, count):
    if count > 0:
        font = pygame.font.SysFont("arial", 70)
        pos = pygame.mouse.get_pos()
        if pos[0] in range(550,651) and pos[1] in range(275,476):
            color = green
            size = 8
        else:
            color = black
            size = 4
        pygame.draw.rect(window, color, (550,275,100,200), size)
        text = "UNO!"
        uno = font.render(text, 1, gold)
        text_width, text_height = font.size(text)
        uno = pygame.transform.rotate(uno, 270)
        xstart = 550 + ((100- text_height)/2) 
        ystart = 275 + ((200-text_width)/2)
        window.blit(uno,(xstart, ystart))



if __name__=="__main__":
    main()
    pygame.quit()



     