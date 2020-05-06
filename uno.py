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
    scores = []

    for i in range(len(players)):
        scores.append(0)
    
    if deck[0] != "+4":
        playedPile = deck.pop(0)
    else:
        deck.append(deck[0])
        playedPile = deck.pop(0)

    playTurn = 0

    reverse = False
    playerSelect = False
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
            #Play the slected Card
            if e.type == pygame.MOUSEBUTTONDOWN and count > 0 :
                if pos[0] in range(50,201) and pos[1] in range(50,101):
                    if isValidPlay(playedPile, selectedCard, count):
                        playedPile = selectedCard
                        if "Reverse" in playedPile:
                            reverse = not reverse
                        cardIndex = hands[players[playTurn]].index(selectedCard)
                        hands[players[playTurn]].pop(cardIndex)
                        if "+2" in playedPile:
                            nextPlayer = changePlayer(players, playTurn, reverse)
                            for i in range(2):
                                hands[players[nextPlayer]].append(deck[0])
                                deck.pop(0)
                        if "+4" in playedPile:
                            nextPlayer = changePlayer(players, playTurn, reverse)
                            for i in range (4):
                                hands[players[nextPlayer]].append(deck[0])
                                deck.pop(0)
                        if "Skip" in playedPile:
                            playTurn = changePlayer(players, playTurn, reverse)
                        wait = pygame.time.delay(2000)
                        playTurn = changePlayer(players, playTurn, reverse)
                        playerSelect = False
            #Add a card to the players hand when they draw a card, drawing a card is signaled by the mouse click event
            # in the location of the deck. Count must be greater than 0 for the game to have started
            if e.type == pygame.MOUSEBUTTONDOWN and count > 0 and pos[0] in range(550,651) and pos[1] in range(275,476):
                # If the card drawn can be played it must be played and not added to the current players hand
                if isValidPlay(playedPile, deck[0], count):
                    playedPile = deck[0]
                    if "Reverse" in playedPile:
                        reverse = not reverse
                    deck.pop(0)
                    if "+2" in playedPile:
                            nextPlayer = changePlayer(players, playTurn, reverse)
                            for i in range(2):
                                hands[players[nextPlayer]].append(deck[0])
                                deck.pop(0)
                    if "+4" in playedPile:
                        nextPlayer = changePlayer(players, playTurn, reverse)
                        for i in range (4):
                            hands[players[nextPlayer]].append(deck[0])
                            deck.pop(0)
                    if "Skip" in playedPile:
                            playTurn = changePlayer(players, playTurn, reverse)
                    wait = pygame.time.delay(2000)
                    playTurn = changePlayer(players, playTurn, reverse)
                    playerSelect = False
                else:
                    hands[players[playTurn]].append(deck[0])
                    deck.pop(0)
                    wait = pygame.time.delay(2000)
                    playTurn = changePlayer(players, playTurn, reverse)
                    playerSelect = False
            
                    
            if e.type == pygame.MOUSEBUTTONDOWN and count > 0:
                if cardLocations != None:
                    for cards in cardLocations:
                        if pos[0] in range(cardLocations[cards][0], (cardLocations[cards][0] + cardLocations[cards][2] +1)):
                            if pos[1] in range(cardLocations[cards][1], (cardLocations[cards][1] + cardLocations[cards][3] + 1)):
                                playerSelect = True
                                xstart = cardLocations[cards][0] - 5
                                ystart = cardLocations[cards][1] - 5
                                height = cardLocations[cards][2] + 10
                                width = cardLocations[cards][3] + 10
                                selectedCard = cards

        #Display all info after this point
        window.fill(white)
        startButton(window,count)
        displayUNO(window,count)
        whoseTurn(window, count, playTurn, players)
        playCardButton(window,count)
        cardLocations = displayHand(window, players[playTurn], hands, count)
        hovered = hoverBox(window, count, cardLocations)
        if playerSelect:
            pygame.draw.rect(window,black,(xstart,ystart,height,width),2)
        if roundWinner(hands):
            winnerIndex = players.index(roundWinner(hands)[1])
            roundScore = updateScores(hands)
            scores[winnerIndex] += roundScore
            print(hands)
            hands, deck = createHands(players)
        displayScores(window, count, players, scores)
        cardsPlayed(window, count, playedPile)
        drawCards(window, count)
        #Update the Display
        pygame.display.update()
        clock.tick(60)

def createDeck():
    deck = []
    colors = ["red", "gold", "green", "blue"]
    wild = "Wild"
    plusFour = "+4"
    actions = ["Skip", "Reverse", "+2"]
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
        cardLocations = {}
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
                # this is to deal with the fact that there are multiple cards of the same card in the deck. We will add a space to the name of that card in order to not overwrite the location
                # of the first card in the cardLocations dictionary. It is quick and dirty and could be improved, but the function works for now.
                if cards in cardLocations:
                    cards += " "
                    if cards in cardLocations:
                        cards += " "
                        if cards in cardLocations:
                            cards += " "
                cardLocations[cards]= [xstart,ystart,text_width, text_height]
                xstart = xstart + text_width + 15
            else: 
                xstart = 215
                ystart = ystart + text_height + 15
                window.blit(playersCard, (xstart,ystart))
                #See comment on line 194
                if cards in cardLocations:
                    cards += " "
                    if cards in cardLocations:
                        cards += " "
                        if cards in cardLocations:
                            cards += " "
                cardLocations[cards] = [xstart, ystart, text_width, text_height]
                xstart = xstart + text_width + 15

        # Return the cardLocations so that we will be able to identify when a card is being slected or hovered over.
        return cardLocations

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

def hoverBox(window, count, locations):
    if count > 0:
        pos = pygame.mouse.get_pos()
        for cards in locations:
            xstart = locations[cards][0]
            ystart = locations[cards][1]
            width = locations[cards][2]
            height = locations[cards][3]
            boxLocation = (xstart - 5, ystart - 5, width + 10, height + 10)
            if pos[0] in range(xstart, (xstart + width + 1)):
                if pos[1] in range (ystart, (ystart + height + 1)):
                    pygame.draw.rect(window,black, boxLocation, 2)
                    return True, cards, boxLocation

def cardsPlayed(window, count, card):
    if count > 0:
        font = pygame.font.SysFont("arial", 70)
        pygame.draw.rect(window,black,(325,275,100,200),4)
        playedCard = card.split(" ")
        if len(playedCard) > 2:
            playedCard = playedCard[0:2]
        if len(playedCard) == 2:
            color = playedCard[1]
            if color == "red":
                color = red
            elif color == "blue":
                color = blue
            elif color == "green":
                color = green
            else:
                color = gold
        else:
            color = black
        text = playedCard[0]
        text_width, text_height = font.size(text)
        playersCard = font.render(text,1, color)
        xstart = 325 + ((100-text_width)/2)
        ystart = 275 +((200-text_height)/2)
        window.blit(playersCard,(xstart,ystart))

def isValidPlay(pileCard, selectedCard, count):
    if count > 0:
        # print(type(pileCard))
        # print(type(selectedCard))
        playedCard = pileCard.split(" ")
        wantToPlay = selectedCard.split(" ")
        if selectedCard == "Wild" or selectedCard == "+4" or pileCard == "Wild" or pileCard == "+4":
            return True
        if len(playedCard) == len(wantToPlay):
            if wantToPlay[0] == playedCard[0] or wantToPlay[1] == playedCard[1]:
                return True
        return False
        
def notValidPlay(window , count):
    if count > 0:
        font = pygame.font.SysFont("arial", 40)
        text = "That is not a Valid Play, Please choose another card"
        text_width, text_height = font.size(text)
        message = font.render(text,1,black)
        xstart = 375 - (text_width/2)
        ystart = 500 + (text_height/2)
        window.blit(message,(xstart,ystart))

def changePlayer(players, playTurn, reverse):
    if not reverse:
        playTurn += 1
        if playTurn == len(players):
            playTurn = 0
    else:
        playTurn -= 1
        if playTurn < 0:
            playTurn = len(players) -1
    return playTurn

def displayScores(window, count, players, scores):
    if count > 0:
        font = pygame.font.SysFont("arial", 40)
        for i in range(len(players)):
            text = "{}: {}".format(players[i], scores[i])
            text_width, text_height = font.size(text)
            message = font.render(text, 1 , black)
            xstart = 50
            ystart = 700 -(text_height * i) - (i * 5)
            window.blit(message,(xstart, ystart))


def roundWinner(hands):
    for player in hands:
        if len(hands[player]) == 0:
            return True, player

def updateScores(hands):
    roundScore = 0
    for players in hands:
        for cards in hands[players]:
            if ("+2" in cards) or ("Reverse" in cards) or  ("skip" in cards):
                roundScore += 20
            elif ("Wild" in cards) or ("+4" in cards):
                roundScore += 50
            else:
                points = int(cards[0])
                roundScore += points
    return roundScore


if __name__=="__main__":
    main()
    pygame.quit()



     