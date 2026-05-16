import pyautogui as gui
import pygetwindow as gw
import time
import random
import pydirectinput as pyd
from rapidocr import RapidOCR

#ocr = RapidOCR()

screen_width, screen_height = gui.size()
friendshipCoordsPixel = ((0.45 * screen_width, 0.222 * screen_height), (0.45 * screen_width, 0.315 * screen_height), (0.45 * screen_width, 0.408 * screen_height), (0.45 * screen_width, 0.501 * screen_height))
trainingTypeCoordsPixel = ((0.447 * screen_width, 0.157 * screen_height), (0.447 * screen_width, 0.252 * screen_height), (0.447 * screen_width, 0.345 * screen_height), (0.447 * screen_width, 0.438 * screen_height))

#Array of coordinates for friendship levels and training type, first value is friendship level, second is training type
trainingCoords = (((0.45 * screen_width, 0.222 * screen_height), (0.447 * screen_width, 0.157 * screen_height)), 
                  ((0.45 * screen_width, 0.315 * screen_height), (0.447 * screen_width, 0.252 * screen_height)), 
                  ((0.45 * screen_width, 0.408 * screen_height), (0.447 * screen_width, 0.345 * screen_height)), 
                  ((0.45 * screen_width, 0.501 * screen_height), (0.447 * screen_width, 0.438 * screen_height)),
                  ((0.45 * screen_width, 0.597 * screen_height), (0.447 * screen_width, 0.533 * screen_height)),)

#Friendship Lvl 0: (110, 107, 121) Gray
#Friendship Lvl 1: (42, 192, 255) Blue
#Friendship Lvl 2: (162, 230, 30) Green
#Friendship Lvl 3: (255, 173, 30) Orange

#Speed Friend:      (60, 190, 255)
#Stamina Friend:    (255, 133, 115)
#Power Friend:      (255, 171, 16)

def press(key):
    pyd.press(key)
    time.sleep(random.uniform(0.1, 0.3))

def gotoRest():
    for i in range(4):
        press('a')
        press('s')
    press('a')
    press('a')

def gotoTraining():
    gotoRest()
    press('d')

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
    
#Gets number of friends in each training, to maximize building friendship levels, doesn't count max friendships
#ToDo: If max level, check for friendship type, if type matches with training, count as friendship training
#Speed Friend:      (60, 190, 255)
#Stamina Friend:    (255, 133, 115)
#Power Friend:      (255, 171, 16)
#Wit Friend:        (26, 210, 156)
def trainingValue(trainingType):
    friendshipLevels = [(110, 107, 121), (42, 192, 255), (162, 230, 30), (255, 173, 30)]
    maxFriendshipLevels = (255, 173, 30)

    trainings = {
        "bonding": 0,
        "friendships": 0
    }

    for pairs in trainingCoords:
        supportFriend = False
        characterPresent = False
        maxFriendship = False

        if gui.pixelMatchesColor(int(pairs[0][0]), int(pairs[0][1]), (110, 107, 121), tolerance=10):
            print("Friendship level 0")
            characterPresent = True
        elif gui.pixelMatchesColor(int(pairs[0][0]), int(pairs[0][1]), (42, 192, 255), tolerance=10):
            print("Friendship level 1")
            characterPresent = True
        elif gui.pixelMatchesColor(int(pairs[0][0]), int(pairs[0][1]), (162, 230, 30), tolerance=10):
            print("Friendship level 2")
            characterPresent = True
        elif gui.pixelMatchesColor(int(pairs[0][0]), int(pairs[0][1]), (255, 173, 30), tolerance=10):
            print("Friendship level max")
            characterPresent = True
            maxFriendship = True
        else:
            print("No-one here")
            return
    
        if gui.pixelMatchesColor(int(pairs[1][0]), int(pairs[1][1]), (60, 190, 255), tolerance=10):
            print("Speed friend")
            if trainingType == "speed" and maxFriendship:
                trainings["friendships"] += 1
            else:
                trainings["bonding"] += 1
            supportFriend = True
        elif gui.pixelMatchesColor(int(pairs[1][0]), int(pairs[1][1]), (255, 133, 115), tolerance=10):
            print("Stamina friend")
            if trainingType == "stamina" and maxFriendship:
                trainings["friendships"] += 1
            else:
                trainings["bonding"] += 1
            supportFriend = True
        elif gui.pixelMatchesColor(int(pairs[1][0]), int(pairs[1][1]), (255, 171, 16), tolerance=10):
            print("Power friend") 
            if trainingType == "power" and maxFriendship:
                trainings["friendships"] += 1
            else:
                trainings["bonding"] += 1
            supportFriend = True
        elif gui.pixelMatchesColor(int(pairs[1][0]), int(pairs[1][1]), (26, 210, 156), tolerance=10):
            print("Wit friend")
            if trainingType == "wit" and maxFriendship:
                trainings["friendships"] += 1
            else:
                trainings["bonding"] += 1
            supportFriend = True

        if characterPresent and not supportFriend:
            print("Director or Reporter")
    
    print(trainings)
    return trainings

#Goes through each training and checks for most valuable training friendship wise
def checkTrainings():
    friendshipBuilding = {
        "speed": 0,
        "stamina": 0,
        "power": 0,
        "guts": 0,
        "wit": 0
    }
    friendshipTraining = {
        "speed": 0,
        "stamina": 0,
        "power": 0,
        "guts": 0,
        "wit": 0
    }

    gotoTraining()
    
    press('enter')
    #Set cursor to "speed training"
    for i in range(6):
        press('a')
    press('w')

    #Iterates through each training, assigning values live
    for key, value in friendshipBuilding.items():
        friendshipBuilding[key] = trainingValue(key)
        press('d')
    
    print(friendshipBuilding)
    return (friendshipBuilding, friendshipTraining)

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


#gw.getWindowsWithTitle('Umamusume')[0].activate()
#checkTrainings()
#print("Energy level: ",checkEnergy(), "/ 20")
#print(checkMood())
#gui.screenshot(region=(100, 100, 200, 200)).save("images/test.png")
#checkAffinities()

trainingValue()

