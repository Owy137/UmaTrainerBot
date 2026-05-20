import pyautogui as gui
import pygetwindow as gw
import time
import random
import pydirectinput as pyd
from rapidocr import RapidOCR
import keyboard as kbd

#ocr = RapidOCR()

screen_width, screen_height = gui.size()

#Possible coordinates for dialogue boxes, white for each dialogue option
eventDialogueCoords = ((int(0.152 * screen_width), int(0.7 * screen_height)),
                       (int(0.152 * screen_width), int(0.598 * screen_height)),
                       (int(0.152 * screen_width), int(0.496 * screen_height)))


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
    time.sleep(random.uniform(0.05, 0.1))

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
        print("Stats for ", type)
        print(trainingValues[type], "\n ========================")
        press('d')

    return trainingValues

#Checks energy bar, returns 0-20 based on how full energy bar is, assumes default max energy of 100
def checkEnergy():
    #Empty color: (118, 117, 118)
    increment = (0.35 - 0.235) / 20
    i = 0.235
    energyLevel = 0
    while i < 0.35:
        if gui.pixelMatchesColor(int(i * screen_width), int(0.13 * screen_height), (118, 117, 118), tolerance=10):
            return energyLevel
        else:
            energyLevel += 1
            i += increment

#Returns 0-4 based on mood
def checkMood():
    #Awful  (189, 106, 255)
    #Bad    (16, 157, 247)
    #Normal (255, 192, 16)
    #Good   (255, 150, 57)
    #Great  (255, 103, 146)
    match gui.pixel(int(0.366 * screen_width), int(0.125 * screen_height)):
        case (189, 106, 255):
            print("Awful mood")
            return 0
        case (16, 157, 247):
            print("Bad mood")
            return 1
        case (255, 192, 16):
            print("Normal mood")
            return 2
        case (255, 150, 57):
            print("Good mood")
            return 3
        case (255, 103, 146):
            print("Great mood")
            return 4
    print("Couldn't read mood")
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

#ToDo
#def checkStats():

def main():
    running = True
    def stopProgram():
        nonlocal running
        running = False

    kbd.add_hotkey('end', stopProgram)

    #72 turns + 6 finale turns and races
    turn = [0] * 78
    # 1-12          13-24         25-36         37-48           49-60         61-72         73-78
    #Predebut", "Postdebut", "EarlyClassic", "LateClassic", "EarlySenior", "LateSenior", "Finales")\
    #Predebut: Focus on bonding trainings
    #Postdebut: Focus on bonding, start shifting towards friendship trainings if possible
    #EarlyClassic & onward: Focus on friendship trainings, only do bonding if no high friendship trainings available

    currentMood = 2 #0-4, awful to great, starting mood is normal, prioritize keeping mood at least good (3), if below 2, add weight to recreation
    currentEnergy = 20 #0-20, starting energy is 20, try to keep above 10, if below 10 add weight to rest, lower energy = more weight to rest, needs to be exponential as chances of failure scales exponentially as energy decreases
    currentStats = {"speed": 0,"stamina": 0,"power": 0,"guts": 0,"wit": 0} #0-1200, purpose of trainer bot is to get at least speed, stamina, and power over 600 for 3 star sparks, possibly wit as well with further developments

    for turnIndex in range(len(turn)):
        if not running:
            break
        print("Turn ", turnIndex)
        time.sleep(1)




