# template for "Stopwatch: The Game"
import simplegui

# define global variables
timer_time_in_tenth_of_a_second = 0
timer_is_running = False
successful_stops = 0
total_stops = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(time):
    '''
        Formats input time (in tenth's of seconds) into format A:BC.D. 
        
        Examples:
        format(0) == 0:00.0
        format(11) = 0:01.1
        format(321) = 0:32.1
        format(613) = 1:01.3
    '''
    tenths_of_seconds = time % 10  
    seconds = (time // 10) % 60
    minutes = (time // 10 - seconds) // 60
    
    formatted_output = str(minutes) + ":"
    if seconds < 10:
        formatted_output = formatted_output + "0" + str(seconds)
    else:
        formatted_output = formatted_output + str(seconds)
    formatted_output = formatted_output + "." + str(tenths_of_seconds)
    return formatted_output
    
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_button_handler():
    '''
        Starts the timer
    '''
    global timer_is_running
    if timer_is_running:
        print "Timer is already running"
    else:
        print "Starting timer"
        timer.start()
        timer_is_running = True
    
    
def stop_button_handler():
    '''
        Stops the timer
    '''
    global timer_is_running, total_stops, successful_stops
    if timer_is_running:
        print "Stopping timer"
        timer.stop()
        timer_is_running = False
        total_stops += 1
        if timer_time_in_tenth_of_a_second % 10 == 0:
            successful_stops += 1
    else:
        print "Timer is not running"
    
    
def reset_button_handler():
    '''
        Resets the timer time to 0
    '''
    print "Resetting timer and scores"
    global timer_time_in_tenth_of_a_second, timer_is_running, total_stops, successful_stops
    timer_time_in_tenth_of_a_second = 0
    total_stops = 0
    successful_stops = 0
    if timer_is_running:
        print "Stopping the timer"
        timer.stop()
        timer_is_running = False

    
# define event handler for timer with 0.1 sec interval
def update_timer_time():
    '''
        Increments the global variable timer_time_in_tenth_of_a_second
        by 1 each time this method is called
    '''
    global timer_time_in_tenth_of_a_second
    timer_time_in_tenth_of_a_second += 1

    
# define draw handler
def draw_handler(canvas):
    '''
        Draws the formatted timer time in the canvas
    '''
    canvas.draw_text(str(successful_stops) + "/" + str(total_stops), (350, 22), 30, "Green")
    canvas.draw_text(format(timer_time_in_tenth_of_a_second), (100, 160), 80, "White")
    
    
# create frame
frame = simplegui.create_frame("Timer Game", 400, 300)


# register event handlers
frame.set_draw_handler(draw_handler)
start_button = frame.add_button("Start", start_button_handler, 100)
stop_button = frame.add_button("Stop", stop_button_handler, 100)
reset_button = frame.add_button("Reset", reset_button_handler, 100)
timer = simplegui.create_timer(100, update_timer_time)


# start frame
frame.start()


# Please remember to review the grading rubric
