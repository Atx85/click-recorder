import keyboard
from pynput import mouse
from pynput.mouse import Button, Controller
import time

timerStarted = False
recordingStarted = False
recordingStopped = False
startPlaying = False # init play loop
stopppedPlaying = False # the loop has finished
nextEvent = 0 # the next event from the eventTimes array
t0 = 0
eventTimes = []
mouseController = Controller()

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
    print(eventTimes)  
    if not timerStarted:
        timerStarted = True

def on_click_show_pos(x, y, button, pressed):
    global eventTimes
    global nextEvent
    print(('Pressed' if pressed else 'Released') + ' at ' + str(x) + ':' + str(y))

listener = mouse.Listener(
    on_click=on_click
)
listener.start()
clickListener = mouse.Listener(
    on_click=on_click_show_pos
)

clickListener.start()

def main():
    while True:
        try:
            global timerStarted
            global recordingStarted
            global recordingStopped
            global stopppedPlaying
            global startPlaying
            global nextEvent
            global mouseController

            if keyboard.is_pressed('q'):
                listener.stop()
                break
            if keyboard.is_pressed('s'):
                recordingStopped = True
                listener.stop()
                # print('recording is stopped press p for play')

            if keyboard.is_pressed('p'):
                startPlaying = True
            if timerStarted and not recordingStarted and not recordingStopped:
                global t0
                t0 = time.time()
                timerStarted = False
                recordingStarted = True

            if startPlaying:
                actualTime = time.time() - t0
                if stopppedPlaying:
                    t0 = time.time()
                    nextEvent = 0
                    stopppedPlaying = False
                if not stopppedPlaying:
                    if (time.time() - t0) > eventTimes[nextEvent]["time"] and ((len(eventTimes) - 1) > nextEvent):
                        mouseController.position = (float(eventTimes[nextEvent]["x"]),float(eventTimes[nextEvent]["y"]))
                        print(mouseController.position)
                        if (eventTimes[nextEvent]["type"] == "Pressed"):
                            mouseController.press(Button.left)
                        if (eventTimes[nextEvent]["type"] == "Released"):
                            mouseController.release(Button.left)
                        nextEvent += 1
                    if len(eventTimes) - 1 <= nextEvent:
                        stopppedPlaying = True


        except Exception as e:
            print(str(e))
            break;
main()