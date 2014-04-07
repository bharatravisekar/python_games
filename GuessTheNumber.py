# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui
import random

# initialize global variables used in your code
secret_num  = 0
total_guesses_allowed = 0
remaining_guesses = 0
game_type = 100

# Helper method to initialize the game based on the type of the game
def init():
    if(game_type == 100): 
        range100()
    else:
        range1000()

# define event handlers for control panel
def range100():
    # button that changes range to range [0,100) and restarts
    print "\nNew game. Range is from 0 to 100"
    global game_type
    global secret_num
    global total_guesses_allowed
    global remaining_guesses
    game_type = 100
    secret_num = random.randrange(0, 100)
    total_guesses_allowed = 7
    remaining_guesses = total_guesses_allowed
    print "Number of remaining guesses is", remaining_guesses

def range1000():
    # button that changes range to range [0,1000) and restarts
    print "\nNew game. Range is from 0 to 1000"
    global game_type
    global secret_num
    global total_guesses_allowed
    global remaining_guesses
    game_type = 1000
    secret_num = random.randrange(0, 1000)
    total_guesses_allowed = 10
    remaining_guesses = total_guesses_allowed
    print "Number of remaining guesses is", remaining_guesses
    
def get_input(guess):
    global remaining_guesses
    guess_num = int(guess)
    print "\nGuess was", guess_num
    remaining_guesses -= 1
    print "Number of remaining guesses is", remaining_guesses
    if(secret_num == guess_num):
        print "Correct!"
        init()
    elif(secret_num < guess_num):
        print "Lower!"
    else:
        print "Higher!"

    if(remaining_guesses == 0):
        print "You ran out of guesses. The number was", secret_num
        init()
    
# create frame
frame = simplegui.create_frame("Guess the number game", 200, 200)

# register event handlers for control elements
button100 = frame.add_button("Range [0, 100)", range100)
button1000 = frame.add_button("Range [0, 1000)", range1000)
input_box = frame.add_input("Enter a guess", get_input, 200)

# start frame
frame.start()

init()
# always remember to check your completed program against the grading rubric
