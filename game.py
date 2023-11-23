#!/bin/python3
import RPi.GPIO as GPIO
import time
from random import randrange

BUTTON_1 = 21
BUTTON_2 = 20
BUTTON_3 = 16
BUTTON_4 = 26

LED_1 = 5
LED_2 = 6
LED_3 = 13
LED_4 = 19

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(BUTTON_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(LED_1, GPIO.OUT)
GPIO.setup(LED_2, GPIO.OUT)
GPIO.setup(LED_3, GPIO.OUT)
GPIO.setup(LED_4, GPIO.OUT)

p_button_1 = GPIO.input(BUTTON_1)
p_button_2 = GPIO.input(BUTTON_2)
p_button_3 = GPIO.input(BUTTON_3)
p_button_4 = GPIO.input(BUTTON_4)

sleep_light_feedback = 0.2


level_difficulty = [2,3,4,5,6,7,8,9,10]
level_speed = 0.5
current_level = 0
next_level = False
level_pattern = []
input_pattern = []

def createPattern():
    global level_pattern
    level_pattern = []
    for x in  range(level_difficulty[current_level]):
        level_pattern.append(randrange(1,5))

def showLevelPattern():
    for x in level_pattern:
        print(x)
        time.sleep(level_speed)
        match x:
            case 1:
                GPIO.output(LED_1, GPIO.HIGH)
                
            case 2:
                GPIO.output(LED_2, GPIO.HIGH)
                
            case 3:
                GPIO.output(LED_3, GPIO.HIGH)
                
            case 4:
                GPIO.output(LED_4, GPIO.HIGH)
            
        time.sleep(level_speed)

        resetLeds()

def increaseSpeed():
    global level_speed
    if level_difficulty[current_level] == 4:
        level_speed = 0.4
    if level_difficulty[current_level] >= 7:
        level_speed = 0.3

def checkInput():
    print("Input now")
    global next_level, level_difficulty, current_level, input_pattern, p_button_1, p_button_2, p_button_3, p_button_4

    input_pattern = []
    abfrage = True

    for x in range(level_difficulty[current_level]):
        
        while (abfrage):
            time.sleep(0.1)
            s_button_1 = GPIO.input(BUTTON_1)
            s_button_2 = GPIO.input(BUTTON_2)
            s_button_3 = GPIO.input(BUTTON_3)
            s_button_4 = GPIO.input(BUTTON_4)

            if s_button_1 != p_button_1:
                p_button_1 = s_button_1
                if s_button_1 == GPIO.HIGH:
                    print("Button 1 pressed")
                    GPIO.output(LED_1, GPIO.HIGH)
                    time.sleep(sleep_light_feedback)
                    compareInput(1,x)
                    x += 1
            if s_button_2 != p_button_2:
                p_button_2 = s_button_2
                if s_button_2 == GPIO.HIGH:
                    print("Button 2 pressed")
                    GPIO.output(LED_2, GPIO.HIGH)
                    time.sleep(sleep_light_feedback)
                    compareInput(2,x)
                    x += 1
            if s_button_3 != p_button_3:
                p_button_3 = s_button_3
                if s_button_3 == GPIO.HIGH:
                    print("Button 3 pressed")
                    GPIO.output(LED_3, GPIO.HIGH)
                    time.sleep(sleep_light_feedback)
                    compareInput(3,x)
                    x += 1
            if s_button_4 != p_button_4:
                p_button_4 = s_button_4
                if s_button_4 == GPIO.HIGH:
                    print("Button 4 pressed")
                    GPIO.output(LED_4, GPIO.HIGH)
                    time.sleep(sleep_light_feedback)
                    compareInput(4,x)
                    x += 1
            
            resetLeds()

            if input_pattern == level_pattern:
                abfrage = False
                nextLevel()

def compareInput(input, currentPattern):
    global level_pattern, input_pattern
    print(currentPattern)
    if input == level_pattern[currentPattern]:
        input_pattern.append(input)
        print(input_pattern)
    else:
        print("Game over")
        allLeds()
        time.sleep(2)
        resetLeds()
        exit()

def nextLevel():
    print("next level")
    global current_level
    current_level += 1
    for x in range(4):
        time.sleep(0.2)
        resetLeds()
        time.sleep(0.2)
        allLeds()
    time.sleep(2)
    resetLeds()

def allLeds():
    GPIO.output(LED_1, GPIO.HIGH)
    GPIO.output(LED_2, GPIO.HIGH)
    GPIO.output(LED_3, GPIO.HIGH)
    GPIO.output(LED_4, GPIO.HIGH)

def resetLeds():
    GPIO.output(LED_1, GPIO.LOW)
    GPIO.output(LED_2, GPIO.LOW)
    GPIO.output(LED_3, GPIO.LOW)
    GPIO.output(LED_4, GPIO.LOW)

def game():
    while current_level < len(level_difficulty):
        createPattern()
        increaseSpeed()
        showLevelPattern()
        checkInput()

game()