# implementation of card game - Memory

import simplegui
import random

N = 16
CARD_SIZE_X = 50
CARD_SIZE_Y = 100
CANVAS_SIZE_X = CARD_SIZE_X * N
CANVAS_SIZE_Y = CARD_SIZE_Y

# helper function to initialize globals
def init():
    global deck, exposed, moves, state
    deck = range(N//2) + range(N//2)
    random.shuffle(deck)
    exposed = [False] * N
    moves = 0
    state = 0
    label.set_text("Moves = " + str(moves))

         
# Find index of card given the click position
def get_index(pos):
    return pos[0] // CARD_SIZE_X


# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, moves, last_1, last_2
    index = get_index(pos)
    if exposed[index] == False:
        exposed[index] = True
        if state == 0:
            state = 1
            last_1 = index
            moves += 1
        elif state == 1:
            state = 2
            last_2 = index
        elif state == 2:
            if deck[last_1] == deck[last_2]:
                exposed[last_1] = True
                exposed[last_2] = True
            else:
                exposed[last_1] = False
                exposed[last_2] = False
            state = 1    
            last_1 = index
            moves += 1
    label.set_text("Moves = " + str(moves))
    
    
# cards are logically 50x100 pixels in size    
def draw(canvas):
    x = 0
    y = 70
    for i in range(N):
        num = deck[i]
        if(exposed[i]):
            canvas.draw_polygon([(x, 0), (x + CARD_SIZE_X, 0), (x + CARD_SIZE_X, CARD_SIZE_Y), (x, CARD_SIZE_Y)], 2, "Brown", "Black")
            canvas.draw_text(str(num), (x + 10, y), 60, "White")
        else:
            canvas.draw_polygon([(x, 0), (x + CARD_SIZE_X, 0), (x + CARD_SIZE_X, CARD_SIZE_Y), (x, CARD_SIZE_Y)], 2, "Brown", "Green")
            
        x += CARD_SIZE_X


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", CANVAS_SIZE_X, CANVAS_SIZE_Y)
frame.add_button("Restart", init)
label = frame.add_label("Moves = 0")

# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()


# Always remember to review the grading rubric