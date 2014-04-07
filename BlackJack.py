# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0


# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card:", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
 
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []
        
    def __str__(self):
        string = ""
        for c in self.cards:
            string += (str(c) + " ")
        return "Hand contains " + string            
        
    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = 0
        for c in self.cards:
            value += VALUES[c.get_rank()]
            if (c.get_rank() == 'A') and (value + 10 <= 21):
                value += 10
        return value
    
    def draw(self, canvas, pos, is_dealer):
        temp_pos = list(pos)
        i = 0
        for c in self.cards:
            if i == 0 and is_dealer and in_play:
                canvas.draw_image(card_back, [CARD_BACK_CENTER[0], CARD_BACK_CENTER[1]], CARD_BACK_SIZE, [temp_pos[0] + CARD_BACK_CENTER[0], temp_pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
                temp_pos[0] += CARD_BACK_SIZE[0] + 10
            else:    
                c.draw(canvas, temp_pos) 
                temp_pos[0] += CARD_SIZE[0] + 10
            i += 1

            
# define deck class 
class Deck:
    def __init__(self):
        cards = []
        for s in SUITS:
            for r in RANKS:
                cards.append(Card(s, r))
        self.cards = cards
        
    def __str__(self):
        string = ""
        for c in self.cards:
            string += (str(c) + " ")
        return "Deck contains" + string
            
    def deal_card(self):
        return self.cards.pop()
        
    def shuffle(self):
        random.shuffle(self.cards)
        

#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    print "Player hand", player_hand, "Value", player_hand.get_value()
    print "Dealer hand", dealer_hand, "Value", dealer_hand.get_value()
    in_play = True
    outcome = "Hit or Stand?"

    
def hit():  
    global in_play, score, outcome
    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score
    if in_play:
        player_hand.add_card(deck.deal_card())
        if player_hand.get_value() <= 21:
            print "Player hand", player_hand, "Value", player_hand.get_value()           
        else:
            outcome = "You are Busted. You Lose!"
            in_play = False
            score -= 1
            print "You are Busted. You Lose!"
            print "Player hand", player_hand, "Value", player_hand.get_value()           
            print "Score", score
            

def stand(): 
    global outcome, score, in_play
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
            print "Dealer hand", dealer_hand, "Value", dealer_hand.get_value()
        
        if dealer_hand.get_value() > 21:         
            outcome = "Dealer Busted. You win!"
            in_play = False
            score += 1
            print "Dealer Busted. You Win!"
            print "Dealer hand", dealer_hand, "Value", dealer_hand.get_value()
            print "Score", score
        else:            
            if player_hand.get_value() > dealer_hand.get_value():
                score += 1
                in_play = False
                outcome = "You Win!"
                print "You Win!"
                print "Player hand", player_hand, "Value", player_hand.get_value()
                print "Dealer hand", dealer_hand, "Value", dealer_hand.get_value()
                print "Score", score
            else:
                score -= 1
                in_play = False
                outcome = "You Lose!"
                print "You Lose!"
                print "Player hand", player_hand, "Value", player_hand.get_value()
                print "Dealer hand", dealer_hand, "Value", dealer_hand.get_value()
                print "Score", score
                
player_hand = Hand()
dealer_hand = Hand()

# draw handler    
def draw(canvas):
    canvas.draw_text("Black Jack", (250, 30), 30, "Black")
    canvas.draw_text("Score: " + str(score), (450, 30), 30, "Blue")
    canvas.draw_text("Dealer: " + outcome, (20, 150), 30, "Black")
    dealer_hand.draw(canvas, (20, 200), True)    
    canvas.draw_text("Player: ", (20, 400), 30, "Black")
    player_hand.draw(canvas, (20, 450), False)    


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
frame.start()


# remember to review the gradic rubric