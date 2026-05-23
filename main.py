import pyautogui as gui
import pygetwindow as gw
import time
import random
import pydirectinput as pyd
from rapidocr import RapidOCR
import keyboard as kbd

screen_width, screen_height = gui.size()

#Friendship Lvl 0: (110, 107, 121) Gray
#Friendship Lvl 1: (42, 192, 255) Blue
#Friendship Lvl 2: (162, 230, 30) Green
#Friendship Lvl 3: (255, 173, 30) Orange
#Friendship lvl max: (255, 235, 120) Yellow

#Speed Friend:      (60, 190, 255)
#Stamina Friend:    (255, 133, 115)
#Power Friend:      (255, 171, 16)
#Wit Friend:        (26, 210, 156)

def press(key):
    pyd.press(key)
    time.sleep(random.uniform(0.025, 0.05))

def gotoRest():
    for i in range(4):
        press('a')
        press('s')
    press('a')
    press('a')

def gotoTraining():
    gotoRest()
    press('d')
    press('enter')

def gotoSkills():
    gotoTraining()
    press('d')

def gotoInfirmary():
    gotoRest()
    press('s')   

def gotoRecreation():
    gotoTraining()
    press('s')  

def gotoRaces():
    gotoSkills()
    press('s')
    
#Gets number of friendships and bond trainings for a single training
def trainingValue(trainingType):

    #Array of coordinates for friendship levels and training type, first value is friendship level, second is training type
    trainingCoords = (((int(0.45 * screen_width), int(0.222 * screen_height)), (int(0.447 * screen_width), int(0.157 * screen_height))), 
                  ((int(0.45 * screen_width), int(0.315 * screen_height)), (int(0.447 * screen_width), int(0.252 * screen_height))), 
                  ((int(0.45 * screen_width), int(0.408 * screen_height)), (int(0.447 * screen_width), int(0.345 * screen_height))), 
                  ((int(0.45 * screen_width), int(0.501 * screen_height)), (int(0.447 * screen_width), int(0.438 * screen_height))),
                  ((int(0.45 * screen_width), int(0.597 * screen_height)), (int(0.447 * screen_width), int(0.533 * screen_height)))
    )

    #Speed Friend:      (60, 190, 255)
    #Stamina Friend:    (255, 133, 115)
    #Power Friend:      (255, 171, 16)
    #Wit Friend:        (26, 210, 156)

    friendshipLevels = [(110, 107, 121), (42, 192, 255), (162, 230, 30), (255, 173, 30)]
    maxFriendshipLevels = (255, 173, 30)

    trainings = {
        "bonding": 0,
        "friendships": 0
    }

    for pairs in trainingCoords:
        supportFriend = False       #Whether or not character is support or NPC, NPC trainings aren't considered for bondings
        characterPresent = False    #Whether a bondable character is present, max bonds on unmatching trainings don't count
        maxFriendship = False       #Whether a support is on max bond, used to check for friendship trainings

        if gui.pixelMatchesColor(pairs[0][0], pairs[0][1], (110, 107, 121), tolerance=10):
            #print("Friendship level 0")
            characterPresent = True
        elif gui.pixelMatchesColor(pairs[0][0], pairs[0][1], (42, 192, 255), tolerance=10):
            #print("Friendship level 1")
            characterPresent = True
        elif gui.pixelMatchesColor(pairs[0][0], pairs[0][1], (162, 230, 30), tolerance=10):
            #print("Friendship level 2")
            characterPresent = True
        elif gui.pixelMatchesColor(pairs[0][0], pairs[0][1], (255, 173, 30), tolerance=10) or gui.pixelMatchesColor(pairs[0][0], pairs[0][1], (255, 235, 120), tolerance=10):
            #print("Friendship level max")
            maxFriendship = True
        else:
            #print("No-one here")
            #print(trainingType, "\n", trainings)
            return trainings
    
        if gui.pixelMatchesColor(int(pairs[1][0]), int(pairs[1][1]), (60, 190, 255), tolerance=10):
            #print("Speed friend")
            if trainingType == "speed" and maxFriendship:
                trainings["friendships"] += 1
            elif characterPresent:
                trainings["bonding"] += 1
            supportFriend = True
        elif gui.pixelMatchesColor(int(pairs[1][0]), int(pairs[1][1]), (255, 133, 115), tolerance=10):
            #print("Stamina friend")
            if trainingType == "stamina" and maxFriendship:
                trainings["friendships"] += 1
            elif characterPresent:
                trainings["bonding"] += 1
            supportFriend = True
        elif gui.pixelMatchesColor(int(pairs[1][0]), int(pairs[1][1]), (255, 171, 16), tolerance=10):
            #print("Power friend") 
            if trainingType == "power" and maxFriendship:
                trainings["friendships"] += 1
            elif characterPresent:
                trainings["bonding"] += 1
            supportFriend = True
        elif gui.pixelMatchesColor(int(pairs[1][0]), int(pairs[1][1]), (26, 210, 156), tolerance=10):
            #print("Wit friend")
            if trainingType == "wit" and maxFriendship:
                trainings["friendships"] += 1
            elif characterPresent:
                trainings["bonding"] += 1
            supportFriend = True

        #if characterPresent and not supportFriend:
            #print("Director or Reporter")
    
    #print(trainingType, "\n", trainings)
    return trainings

#Goes through each training and checks for most valuable training friendship wise
def checkTrainings():

    trainingTypes = ["speed", "stamina", "power", "guts", "wit"]

    trainingValues = {}

    gotoTraining()
    
    #Set cursor to "speed training"
    for i in range(6):
        press('a')
    press('w')

    #Iterates through each training, assigning values live
    for type in trainingTypes:
        trainingValues[type] = trainingValue(type)
        press('d')

    press('esc')
    return trainingValues

#Checks energy bar, returns 0-20 based on how full energy bar is, assumes default max energy of 100
def checkEnergy():
    #Empty color: (118, 117, 118)
    i = 0.235
    increment = (0.35 - i) / 20
    energyLevel = 0
    while i < 0.35 - increment:
        #gui.moveTo(int(i * screen_width), int(0.13 * screen_height))
        if gui.pixelMatchesColor(int(i * screen_width), int(0.13 * screen_height), (118, 117, 118), tolerance=10):
            return energyLevel
        else:
            energyLevel += 1
            i += increment
    return energyLevel

#Returns 0-4 based on mood
def checkMood():
    #Awful  (202, 128, 255)
    #Bad    (16, 173, 247)
    #Normal (255, 212, 24)
    #Good   (255, 169, 66)
    #Great  (255, 130, 156)

    #gui.moveTo(int(0.405 * screen_width), int(0.115 * screen_height))
    #moodColor = gui.pixel(int(0.41 * screen_width), int(0.115 * screen_height))
    #print(moodColor)

    if gui.pixelMatchesColor(int(0.405 * screen_width), int(0.115 * screen_height), (202, 128, 255), tolerance=50):
        return 0
    elif gui.pixelMatchesColor(int(0.405 * screen_width), int(0.115 * screen_height), (16, 173, 247), tolerance=50):
        return 1
    elif gui.pixelMatchesColor(int(0.405 * screen_width), int(0.115 * screen_height), (255, 212, 24), tolerance=50):
        return 2
    elif gui.pixelMatchesColor(int(0.405 * screen_width), int(0.115 * screen_height), (255, 169, 66), tolerance=50): 
        return 3
    elif gui.pixelMatchesColor(int(0.405 * screen_width), int(0.115 * screen_height), (255, 130, 156), tolerance=50):
        return 4
    else:
        return -1

#Gets racing affinities; track, distance, and style
#May be redundant if using career preset races
def checkAffinities():

    raceAffinities = {
        "Turf": "",
        "Dirt": "",
        "Sprint": "",
        "Mile": "",
        "Medium": "",
        "Long": "",
        "Front": "",
        "Pace": "",
        "Late": "",
        "End": "",
    }

    #Open stats menu
    gotoSkills()
    press('w')
    press('enter')

    gui.screenshot(region=(int(0.2 * screen_width), int(0.31 * screen_height),
                           int(0.43 * screen_width) - int(0.2 * screen_width), int(0.41 * screen_height) - int(0.31 * screen_height))
                           ).save("images/affinities.jpg")
    result = ocr("images/affinities.jpg").txts
    for i in range(len(result)-1):
        if(len(result[i]) == 1):
            i += 1
        #OCR reads Medium A as one word due to spacing
        elif(result[i] != "MediumA"):
            raceAffinities[result[i]] = result[i+1]
            i += 2
        elif(result[i] == "MediumA"):
            raceAffinities["Medium"] = result[i][-1]
            i += 1

    print(raceAffinities)
    return

#Gets currents stats
def checkStats():

    stats = {
        "speed": 0,
        "stamina": 0, 
        "power": 0,
        "guts": 0,
        "wit": 0
    }
    gui.screenshot(region=(int(0.16 * screen_width), int(0.6455 * screen_height),
                           int(0.19 * screen_width) - int(0.16 * screen_width), int(0.69 * screen_height) - int(0.645 * screen_height))
                           ).save("images/speed.png")
    speed = ocr("images/speed.png").txts[1]
    stats["speed"] = int(speed)

    gui.screenshot(region=(int(0.21 * screen_width), int(0.645 * screen_height),
                           int(0.24 * screen_width) - int(0.21 * screen_width), int(0.69 * screen_height) - int(0.645 * screen_height))
                           ).save("images/stamina.png")
    stamina = ocr("images/stamina.png").txts[1]
    stats["stamina"] = int(stamina)

    gui.screenshot(region=(int(0.26 * screen_width), int(0.645 * screen_height),
                           int(0.29 * screen_width) - int(0.26 * screen_width), int(0.69 * screen_height) - int(0.645 * screen_height))
                           ).save("images/power.png")
    power = ocr("images/power.png").txts[1]
    stats["power"] = int(power)

    gui.screenshot(region=(int(0.31 * screen_width), int(0.645 * screen_height),
                           int(0.34 * screen_width) - int(0.31 * screen_width), int(0.69 * screen_height) - int(0.645 * screen_height))
                           ).save("images/guts.png")
    guts = ocr("images/guts.png").txts[1]
    stats["guts"] = int(guts)

    gui.screenshot(region=(int(0.36 * screen_width), int(0.645 * screen_height),
                           int(0.39 * screen_width) - int(0.36 * screen_width), int(0.69 * screen_height) - int(0.645 * screen_height))
                           ).save("images/wit.png")
    wit = ocr("images/wit.png").txts[1]
    stats["wit"] = int(wit)

    return stats


def eventHandler():
    options = {}

    #Possible coordinates for dialogue boxes, white for each dialogue option
    eventDialogueCoords = ((int(0.152 * screen_width), int(0.7 * screen_height)),
                            (int(0.152 * screen_width), int(0.598 * screen_height)),
                            (int(0.152 * screen_width), int(0.496 * screen_height)))

    if (gui.pixelMatchesColor(eventDialogueCoords[0][0], eventDialogueCoords[0][1], (255, 255, 255), tolerance=5) and
        gui.pixelMatchesColor(eventDialogueCoords[1][0], eventDialogueCoords[1][1], (255, 255, 255), tolerance=5)):
            if gui.pixelMatchesColor(eventDialogueCoords[2][0], eventDialogueCoords[2][1], (255, 255, 255), tolerance=5):
                choices = 3
            else:
                choices = 2

    #Checks for dialogue box location by detecting green choice options    
    dialogueStartY = 0.335

    #Option 1
    colorCheckY = .335
    while not gui.pixelMatchesColor(int(0.8 * screen_width), int(colorCheckY * screen_height), (121, 202, 11), tolerance=10):
        #gui.moveTo(int(0.8 * screen_width), int(colorCheckY * screen_height))
        colorCheckY += .005
    gui.screenshot(region=(int(0.565 * screen_width), int((dialogueStartY * screen_height)),
                            int(0.8 * screen_width) - int(0.565 * screen_width), int(colorCheckY * screen_height) - int(dialogueStartY * screen_height))
                            ).save("images/eventDialogue_1.jpg")
    options[1] = ocr("images/eventDialogue_1.jpg").txts

    #Option 2
    colorCheckY += 0.06
    dialogueStartY = colorCheckY
    while ((not gui.pixelMatchesColor(int(0.8 * screen_width), int(colorCheckY * screen_height), (121, 202, 11), tolerance=10)) and
          (colorCheckY < .865)):
        #gui.moveTo(int(0.8 * screen_width), int(colorCheckY * screen_height))
        colorCheckY += .005
    gui.screenshot(region=(int(0.565 * screen_width), int((dialogueStartY * screen_height)),
                            int(0.8 * screen_width) - int(0.565 * screen_width), int(colorCheckY * screen_height) - int(dialogueStartY * screen_height))
                            ).save("images/eventDialogue_2.jpg")
    options[2] = ocr("images/eventDialogue_2.jpg").txts

    #Option 3
    if choices == 3:
        colorCheckY += 0.06
        dialogueStartY = colorCheckY
        while colorCheckY < .865:
            #gui.moveTo(int(0.8 * screen_width), int(colorCheckY * screen_height))
            colorCheckY += .005
        gui.screenshot(region=(int(0.565 * screen_width), int((dialogueStartY * screen_height)),
                                int(0.8 * screen_width) - int(0.565 * screen_width), int(colorCheckY * screen_height) - int(dialogueStartY * screen_height))
                                ).save("images/eventDialogue_3.jpg")
        options[3] = ocr("images/eventDialogue_3.jpg").txts

    print(options)

    #Sets cursor to Effects button
    for i in range(4):
        press('s')
    for i in range(3):
        press('a')
    press('w')

    if choices == 3:    #Assuming all triple choices are new years shrine visits, always chooses energy
        for key, effects in options.items():
            for string in effects:
                if "energy" in string.lower():
                    for i in range(4-key):
                        press('w')
    else:               #Two choices
        for key, effects in options.items():
            for string in effects:
                if "energy" in string.lower():
                    for i in range(4-key):
                        press('w')
                

def main():
    running = True
    def stopProgram():
        nonlocal running
        running = False

    kbd.add_hotkey('end', stopProgram)

    #Turns:
    # 1-12          13-24         25-36         37-48           49-60         61-72         73-78
    #Predebut", "Postdebut", "EarlyClassic", "LateClassic", "EarlySenior", "LateSenior", "Finales")

    #Predebut: Focus on bonding trainings
    #Postdebut: Focus on bonding, start shifting towards friendship trainings if possible
    #EarlyClassic & onward: Focus on friendship trainings, only do bonding if no high friendship trainings available

    currentMood = 2 #0-4, awful to great, starting mood is normal, prioritize keeping mood at least good (3), if below 2, add weight to recreation
    currentEnergy = 20 #0-20, starting energy is 20, try to keep above 10, if below 10 add weight to rest, lower energy = more weight to rest, needs to be exponential as chances of failure scales exponentially as energy decreases
    currentStats = {"speed": 0,"stamina": 0,"power": 0,"guts": 0,"wit": 0} #0-1200, purpose of trainer bot is to get at least speed, stamina, and power over 600 for 3 star sparks, possibly wit as well with further developments
    gw.getWindowsWithTitle("UmaMusume")[0].activate()

    trainings = checkTrainings()
    time.sleep(1)
    currentEnergy = checkEnergy()
    currentMood = checkMood()
    stats = checkStats()

    for pair in trainings:
        print(pair, trainings[pair])
    print("Energy: ", currentEnergy)
    print("Mood: ", currentMood)
    print(stats)
    '''
    for turnIndex in range(78):
        if not running:
            break
        print("Turn ", turnIndex)
        time.sleep(1)
    '''

ocr = RapidOCR()
gw.getWindowsWithTitle("UmaMusume")[0].activate()
#main()
eventHandler()


'''
#Top left: int(0.565 * screen_width), int(0.325 * screen_height)
#Right X: int(0.8 * screen_width)
#Green box height: ~0.05 * screen_height
gui.moveTo(int(0.8 * screen_width), int(0.275 * screen_height))
print(gui.pixel(int(0.8 * screen_width), int(0.275 * screen_height)))
time.sleep(1)
gui.moveTo(int(0.8 * screen_width), int(0.325 * screen_height))
print(gui.pixel(int(0.8 * screen_width), int(0.325 * screen_height)))
'''