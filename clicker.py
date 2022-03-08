import keyboard
from pynput import mouse
from pynput.mouse import Button, Controller
import time
import os

timerStarted = False
recordingStarted = False
recordingStopped = False
startPlaying = False # init play loop
stopppedPlaying = False # the loop has finished
nextEvent = 0 # the next event from the eventTimes array
timePaused = False
t0 = 0
eventTimes = []
mouseController = Controller()
showMessage = True
iterations = 0

def on_click(x, y, button, pressed):
    global timerStarted
    global t0

    actualTime = time.time() - t0
    if t0 == 0:
        actualTime = 0
    eventTimes.append({
        "x": mouseController.position[0],
        "y": mouseController.position[1],
        "type": ('Pressed' if pressed else 'Released'),
        "time": actualTime
    })
    newClick = eventTimes[len(eventTimes) - 1]
    print("[" + str(newClick['time']) + "] Recorded " + str(newClick['type']) + " at " + str(newClick['x']) + ':' + str(newClick['y']))  
    if not timerStarted:
        timerStarted = True

def show_message(state):
    global showMessage
    global nextEvent
    global iterations
    if showMessage:
        os.system('cls')
        if state == 'start':
            print('Click to start recording! [q]: quit, [s]: stop recording')
        if state == 'finished recording':
            print('Press p to start playing the recorded clicks. [q]: quit')
        if state == 'played click':
            print('next event: ' + str(nextEvent))
            print('iterations: ' + str(iterations))
            print('time: ' + str(time.time() - t0))
            for i,c in enumerate(eventTimes):
                if i == nextEvent - 1:
                    print(">" + str(c))
                else: 
                    print(" " + str(c))
            print('[q]: quite, [g]: pause [h]: unpause')
        if state == 'wait':
            pass
        showMessage = False


listener = mouse.Listener(
    on_click=on_click
)
listener.start()
def main():
    while True:
        show_message('start')
        try:
            global timerStarted
            global recordingStarted
            global recordingStopped
            global stopppedPlaying
            global startPlaying
            global nextEvent
            global mouseController
            global showMessage
            global timePaused
            global t0
            global iterations

            if keyboard.is_pressed('q'):
                listener.stop()
                break
            if keyboard.is_pressed('s'):
                recordingStopped = True
                listener.stop()
                showMessage = True
                show_message('finished recording')
            if keyboard.is_pressed('p'):
                startPlaying = True

            if startPlaying:
                if keyboard.is_pressed('g'):
                    timePaused = True         
                if keyboard.is_pressed('h') and timePaused:
                    timePaused = False
                    t0 = time.time() + eventTimes[nextEvent]['time']
            if timerStarted and not recordingStarted and not recordingStopped:
                t0 = time.time() + eventTimes[nextEvent - 1]['time']
                timerStarted = False
                recordingStarted = True

            if startPlaying and not timePaused:
                if stopppedPlaying:
                    # resetting the timer for each round
                    t0 = time.time()
                    nextEvent = 0
                    stopppedPlaying = False
                if not stopppedPlaying and not timePaused:
                    if (time.time() - t0) > eventTimes[nextEvent]["time"] and ((len(eventTimes)) > nextEvent):
                        mouseController.position = (float(eventTimes[nextEvent]["x"]),float(eventTimes[nextEvent]["y"]))
                        if (eventTimes[nextEvent]["type"] == "Pressed"):
                            mouseController.press(Button.left)
                            showMessage = True
                            show_message('played click')
                        if (eventTimes[nextEvent]["type"] == "Released"):
                            mouseController.release(Button.left)
                            showMessage = True
                            show_message('played click')
                        nextEvent += 1
                    if len(eventTimes) < nextEvent + 1:
                        stopppedPlaying = True
                        iterations += 1


        except Exception as e:
            print(str(e))
            break;
main()