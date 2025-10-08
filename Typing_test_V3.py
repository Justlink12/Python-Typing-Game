import pygame
from pygame.locals import *
import sys
import time
import random

class TypingGame:

    def __init__(self):

        self.w = 1500
        self.h = 1000

    # changes font style of all of draw_text & draw_text_diff methods
        #self.font = ('monospace')
        self.font = ('CascadiaMono-Regular.ttf')
        # self.font = ('CascadiaMono-Regular.ttf')

        self.reset = True
        self.active = False
        self.escape = False
        self.testType = ""
        self.input_text = ''
        self.word = ''
        self.rw = ' '
        self.rw_color = (255,255,255)
        self.starttime = False
        self.tracktime = 0
        self.end_time = 0

        self.storeWords = []

        self.end = False

        # color constants rgb(r,g,b)
        self.HEAD_C = (255, 213, 102)
        self.HEAD_R = (120 , 25, 150)
        self.TEXT_C = (240, 240, 240)
        self.RESULT_C = (255, 70, 70)
        self.BG = (250, 250, 250)

        self.list_libraries = ['libEZ1.txt','libEZ2.txt', 'libEZ3.txt','libMED1.txt','libMED2.txt', 'libMED3.txt','libHARD1.txt','libHARD2.txt', 'libHARD3.txt']
        self.outFile = 'outFile.txt'

        pygame.init()  # initializes all imported pygame modules
        pygame.font.init()

        self.screen = pygame.display.set_mode(
            (self.w, self.h))  # init screen w/set_mode

        pygame.display.set_caption('Programming Typing Test')
        self.imp = pygame.image.load("pumpkin.jpeg").convert()
        self.imp = pygame.transform.scale(self.imp,(250,250))


    def draw_text(self, screen, msg, y, fsize, color):
        
        font = pygame.font.Font(self.font,fsize)
        text = font.render(msg, 1, color)  # renders font for text
        text_rect = text.get_rect(center=(self.w/2, y)) # n determines centeredness for text
        screen.blit(text, text_rect)  # copy screen to be updated
        pygame.display.update()  # update screen

    def draw_text_diff(self, screen, msg, y, fsize, color,w):
        font = pygame.font.Font(self.font,fsize)
        text = font.render(msg, 1, color)  # renders font for text
        text_rect = text.get_rect(center=(w, y)) # n determines centeredness for text
        screen.blit(text, text_rect)  # copy screen to be updated
        pygame.display.update()  # update screen

    def get_sentence(self):
        
        if self.testType == "easy":
            self.libpick = self.list_libraries[0:2]
        elif self.testType == "med":
            self.libpick = self.list_libraries[3:5]
        elif self.testType == "hard":
            self.libpick = self.list_libraries[6:8]
        else:
            self.libpick = self.list_libraries
        print(self.testType)
        
        # chooses at random based on rand()
        self.f = random.choice(self.libpick)

        with open(self.f, 'r') as file:

            fileRead = file.read()
            libSent = fileRead.split('\n')

            return libSent

    def run(self):
        self.testType = self.menu()

        self.reset_game()
        self.multi = 0
        # init length of line and lineEnd bool
        self.lineCount = len(self.word)
        self.lineEnd = False
        self.lineTracker = 0

        self.rightTracker = 0
        self.wrongTracker = 0
        self.running = True

        clock = pygame.time.Clock()
        
    

        while (self.running):
            #Starts the timer only when the user press enter on the typing box
            if self.starttime:
                #Sets the fps to 60
                clock.tick(60)
                #Adds the time in milliseconds between each tick. Self.multi ensures the timer starts at 0
                self.tracktime += clock.get_time()*self.multi
                #Multi is set to 1 to allow calculations in next loops
                self.multi = 1
                #print(self.tracktime)
            
            pygame.draw.rect(self.screen, self.HEAD_C,
                             (100, 350, 1250, 100), 2) # first box around r/wrong
            pygame.draw.rect(self.screen, self.HEAD_C,
                             (100, 250, 1250, 100), 2)  # second box around current line to type

            if self.lineTracker == 5: #instructive material disappears after 5 lines types
                self.screen.fill((250, 250, 250), (2, 500, 90, 100))
                self.screen.fill((250, 250, 250), (2, 350, 90, 100))
                self.screen.fill((250, 250, 250), (2, 115, 1480, 100))
                

            pygame.draw.rect(self.screen, self.HEAD_C,
                             (100, 650, 1250, 100), 2) # fourth box for the next line to be typed
            pygame.draw.rect(self.screen, self.HEAD_C,
                             (100, 750, 1250, 100), 2) # fifth box for the 2nd next line to be typed
            
            self.screen.fill((0, 0, 0), (100, 500, 1250, 100))

            # update the text of user input
            self.draw_text(self.screen, self.input_text,550, 26, (250, 250, 250))
            


            pygame.display.update()
            
            for event in pygame.event.get():

                if event.type == QUIT or self.escape == True:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()

                    # position of input box
                    if(self.button(100,1250,500,1000,x,y)):
                        self.active = True
                        self.input_text = ''
                        #self.tracktime = time.time()
                        self.starttime = True

                     # position of reset box
                    if (x >= 700 and x <= 825 and y >= 800 and self.end):
                        self.txt_compare()
                        #Takes user to the results screen
                        self.results()
                        self.testType = self.menu()
                        self.reset_game()
                        x, y = pygame.mouse.get_pos()
                        self.lineCount = len(self.word)
                        self.lineEnd = False

                elif event.type == pygame.KEYDOWN:

                    if self.active and not self.end:

                        if event.key == pygame.K_RETURN and self.lineTracker < self.lineCount:

                            self.screen.fill(self.BG, (100, 250, 1250, 100))
                            self.screen.fill(self.BG, (100, 350, 1250, 100))
                            self.screen.fill(self.BG, (100, 650, 1250, 100))
                            self.screen.fill(self.BG, (100, 750, 1250, 100))

                            pygame.draw.rect(self.screen, self.HEAD_C,(95, 495, 1260, 110), 5) # Draw outline around input box after first enter 
                            self.storeWords.append(self.input_text)

                            self.input_rw()

                            self.input_text = '' # reset input text
                            try:
                                self.draw_text(self.screen, self.word[self.lineTracker], 400, 20, (10, 10, 10)) #draw current line to be typed
                                self.draw_text_diff(self.screen, str(self.lineTracker+1), 400, 32, (10,10,10),150)
                            except: 
                                self.draw_text(self.screen, " ", 400, 28, (10, 10, 10)) #draw current line to be typed
                                self.draw_text_diff(self.screen, " ", 400, 32, (10,10,10),150)

                            try:
                                self.draw_text(self.screen, self.word[self.lineTracker+1], 700, 20, (10, 10, 10))
                                self.draw_text_diff(self.screen, str(self.lineTracker+2), 700, 32, (10,10,10),150)
                                
                            except:
                                self.draw_text(self.screen, " ", 700, 28, (10, 10, 10))
                                self.draw_text_diff(self.screen, " ", 700, 50, (10,10,10),150)

                            try:   
                                self.draw_text(self.screen, self.word[self.lineTracker+2], 800, 20, (10, 10, 10))
                                self.draw_text_diff(self.screen, str(self.lineTracker+3), 800, 32, (10,10,10),150)
                            except: 
                                self.draw_text(self.screen, " ", 800, 28, (10, 10, 10))
                                self.draw_text_diff(self.screen, " ", 800, 32, (10,10,10),150)

                            self.screen.fill(self.rw_color, (100, 250, 1250, 100))
                            self.draw_text(self.screen, self.rw,
                                           300, 28, (10, 10, 10))

                            self.lineTracker += 1
                        
                        elif event.key == pygame.K_RETURN and self.lineTracker == self.lineCount:

                            self.screen.fill(self.BG, (100, 250, 1250, 100))
                            self.screen.fill(self.BG, (100, 350, 1250, 100))
                            self.screen.fill(self.BG, (100, 650, 1250, 100))
                            self.screen.fill(self.BG, (100, 750, 1250, 100))
                            # temp rect to test where to fill
                            pygame.draw.rect(self.screen, self.HEAD_C,(95, 495, 1260, 110), 5) # Draw outline around input box after first enter 
                            self.storeWords.append(self.input_text)

                            self.input_rw()

                            self.input_text = '' # reset input text
                            try:
                                self.draw_text(self.screen, self.word[self.lineTracker], 400, 20, (10, 10, 10)) #draw current line to be typed
                                self.draw_text_diff(self.screen, str(self.lineTracker+1), 400, 32, (10,10,10),150)
                            except: 
                                self.draw_text(self.screen, " ", 400, 20, (10, 10, 10)) #draw current line to be typed
                                self.draw_text_diff(self.screen, " ", 400, 32, (10,10,10),150)
                            
                            # if future text is out of index then print a " "
                            try:
                                self.draw_text(self.screen, self.word[self.lineTracker+1], 700, 20, (10, 10, 10))
                                self.draw_text_diff(self.screen, str(self.lineTracker+2), 700, 32, (10,10,10),150)
                                
                            except:
                                self.draw_text(self.screen, " ", 700, 28, (10, 10, 10))
                                self.draw_text_diff(self.screen, " ", 700, 50, (10,10,10),150)

                            try:   
                                self.draw_text(self.screen, self.word[self.lineTracker+2], 800, 32, (10, 10, 10))
                                self.draw_text_diff(self.screen, str(self.lineTracker+3), 800, 32, (10,10,10),150)
                            except: 
                                self.draw_text(self.screen, " ", 800, 28, (10, 10, 10))
                                self.draw_text_diff(self.screen, " ", 800, 32, (10,10,10),150)
                            
                            self.screen.fill(self.rw_color, (100, 250, 1250, 100))
                            self.draw_text(self.screen, self.rw,
                                           300, 28, (10, 10, 10))

                            self.lineTracker += 1
                            self.F_time = self.tracktime    

                            self.draw_text(self.screen, "Results", self.h - 70, 40, (20, 20, 20))
                            
                            #Gets the time at which the user has finished the typing passage. Not in use currently
                            #self.end_time = time.time()

                            self.end = True

                            self.starttime = False
                            self.multi = 0
                            self.lineTracker = 0

                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]

                        elif event.key == pygame.K_ESCAPE:
                            self.escape = True
                            

                        else:
                            try:
                                self.input_text += event.unicode

                            except:
                                pass

            pygame.display.update()
        clock.tick(60)
            
    #Used to simplify button creation on screen
    def button(self,x1,x2,y1,y2,mx,my):
        #print(x1,x2,y1,y2,mx,my)
        if(mx >= x1 and mx <= x2 and my >= y1 and my <= y2):
            return True
        else:
            return False


    def menu(self):
        cur = True
        #Screen is cleared
        pygame.display.update()
        #self.endtime = (time.time() - self.tracktime) * 1000
        #Sets the background to white
        # Using blit to copy content from one surface to other
        
        self.screen.fill(self.BG)
        self.draw_text(self.screen, "The Amazing Typing Test!",150, 40, (0, 0, 0))
        #pygame.draw.rect(self.screen, self.HEAD_R,
                             #(600, 380, 300, 100), 2)  
            #self.draw_text(self.screen, "Random Test",(self.h/2) - 70, 40, (255, 255, 255))
    
        self.screen.fill((120, 15, 150), (500, 380, 500, 100))

            #Bottom box
        self.screen.fill((120, 15, 150), (500, 500, 500, 100))
        #pygame.draw.rect(self.screen, self.HEAD_R,
                             #(500, 580, 500, 100), 2)
        self.screen.fill((120, 15, 150), (500, 620, 500, 100))
        self.screen.fill((120, 15, 150), (500, 740, 500, 100))
        #pygame.draw.rect(self.screen, self.HEAD_R,
                             #(500, 580, 500, 100), 2)
        self.draw_text(self.screen, "I think I want...",(self.h/2) - 190, 40, (0, 0, 0))
        self.draw_text(self.screen, "An Easy Test",(self.h/2) - 70, 40, (255, 255, 255))
        self.draw_text(self.screen, "A bit of a challenge",(self.h/2) + 45, 40, (255, 255, 255))
        self.draw_text(self.screen, "To try God Mode",(self.h/2) + 165, 40, (255, 255, 255))
        self.draw_text(self.screen, "A Random Test",(self.h/2) + 285, 40, (255, 255, 255))

        #Keeps the user on the results screen until specified to leave program or take a new test
        while(cur):
            #self.screen.fill(0, 0, 0)
            
            time.sleep(0.1)
            
            for event in pygame.event.get():

                if event.type == QUIT or self.escape == True:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()

                     # position of reset box
                    if(self.button(500,1000,380,480,x,y)):
                        self.reset_game()
                        x, y = pygame.mouse.get_pos()
                        print("Yellow")
                        return "easy"
                    if(self.button(500,1000,500,600,x,y)):
                        self.reset_game()
                        x, y = pygame.mouse.get_pos()
                        return "med"
                    if(self.button(500,1000,620,720,x,y)):
                        self.reset_game()
                        x, y = pygame.mouse.get_pos()
                        return "hard"
                    if(self.button(500,1000,740,840,x,y)):
                        self.reset_game()
                        x, y = pygame.mouse.get_pos()
                        return "rand"
                #Allows user to escape program with ESC button
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.escape = True
                        
            #x, y = pygame.mouse.get_pos()
            #if x>0:
                #cur = False


    def results(self):
        cur = True
        #Screen is cleared
        pygame.display.update()
        #self.endtime = (time.time() - self.tracktime) * 1000
        #Sets the background to white
        # Using blit to copy content from one surface to other
        
        self.resultText = "Your results!"
        self.screen.fill(self.BG)
        #Calculates the amount of time passed and rounds it to 2 decimal places
        self.endtime = round(self.tracktime/1000,2)
        #Calculates the percentage of correct words to wrong words
        self.test_results = round((self.rightTracker/len(self.word))*100,2)
        #Open the score text file for reading and writing
        self.scorefile = open("score.txt","r")
        self.highScore = float(self.scorefile.readline())
        self.scorefile.close()
        print(self.test_results)
        # calculates lines/minute by converting time to minutes and diving
        self.lpm = round((len(self.word)/self.endtime)*60)
        self.clpm = round(self.lpm*(self.test_results/100))
        #Calculates the correct words per minute based of results percentage
        # self.cwpm = round(self.wpm*(self.test_results/100))
        if self.highScore < self.test_results:
            self.scorefile = open("score.txt","w")
            self.resultText = "Your Results! New Highscore!"
            self.scorefile.write(str(self.test_results))
            self.scorefile.close()
            #Brings up a picture of a cat
            self.screen.blit(self.imp, (50, self.h*0.3))

        #Output of results to screen
        self.draw_text(self.screen, self.resultText, 80, 80, (10, 10, 10))
        self.draw_text(self.screen, str(self.test_results)+"% correct", 150, 60, (10, 10, 10))
        self.draw_text(self.screen, str(self.endtime)+" secs", 220, 60, (10, 10, 10))
        self.draw_text(self.screen, str(self.lpm)+" lines per minute", 290, 60, (10, 10, 10))

        self.draw_text(self.screen, str(self.clpm)+" correct lpm", 350, 60, (10, 10, 10))

        #Keeps the user on the results screen until specified to leave program or take a new test
        while(cur):
            #self.screen.fill(0, 0, 0)
            
            time.sleep(0.1)
            self.draw_text(self.screen, "New Test",self.h - 70, 40, (20, 20, 20))
            
            for event in pygame.event.get():

                if event.type == QUIT or self.escape == True:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()

                     # position of reset box
                    if(self.button(700,825,800,1000,x,y) and self.end):
                        self.reset_game()
                        x, y = pygame.mouse.get_pos()
                        cur = False
                #Allows user to escape program with ESC button
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.escape = True
                        
            #x, y = pygame.mouse.get_pos()
            #if x>0:
                #cur = False

    def reset_game(self):
        
        self.screen.fill((0, 0, 0))
        pygame.display.update()

        #Initialize variables
        self.reset = False
        self.end = False
        self.starttime = False
        self.tracktime = 0
        self.input_text = ''
        self.word = ''
        self.storeWords = []

        # Get random sentence or later random file
        self.word = self.get_sentence()
        #Removes all the spaces from each item in the self.word list
        #For the text document, use ~ where spaces are required
        for i in range(len(self.word)):
            self.word[i] = self.word[i].replace(" ","")
            self.word[i] = self.word[i].replace("~"," ")
        
            
        # print(self.word)
        if (not self.word):
            self.reset_game()  # contingency

        # drawing heading
        self.screen.fill(self.BG)

        self.draw_text(self.screen, "Typing Speed Test", 60, 70, (10, 10, 10))
        self.draw_text(self.screen, '(click the black bar and press enter to start game)', 150, 45, (10, 10, 10))

        self.draw_text_diff(self.screen, "Type", 530, 20, (10,10,10),25)
        self.draw_text_diff(self.screen, "   here ->", 570, 20, (10,10,10),25) # instruction on what to type; next to second box

        self.draw_text_diff(self.screen, "Type", 370, 20, (10,10,10),25)
        self.draw_text_diff(self.screen, "   this ->", 400, 20, (10,10,10),25) # instruction on what where to type; next to third box (input box)

        # draw the rectangle for input box
        pygame.draw.rect(self.screen, (255, 192, 25), (100, 500, 1250, 100), 2)

        pygame.display.update()

    def txt_compare(self):
        """
        Notes: 
        -10/19/23
            - This gives output to self.outFile, mutable in __init__ method
            - output is a bit messy, perhaps using a rich text file (RTF) would be easier on the eyes by:
                - changing font 
                - " color
                - " styling
            - write functions don't work like print(), you can't have more than one arg
            - I ended up not using difflib because output was an eye sore
        """
        with open(self.outFile, 'w') as f:

            f.write("Typing Corrections: \n\n")

            # removes first element of store words list to make words and storewords the same length
            self.storeWords.pop(0)

            line_accum = 1
            for model, input in zip(self.word, self.storeWords):

                if model == input: # if element (self.word) == element (self.storeWords) corrent line output to file
                    f.write(str(line_accum))
                    f.write((". CORRECT: "))
                    f.write(model)
                    f.write(" == ")
                    f.write(input)
                    f.write("\n")

                elif model != input: # if element (self.word) != element (self.storeWords) wrong line output to file
                    f.write(str(line_accum))
                    f.write(". WRONG: ")
                    f.write(model)
                    f.write(" != ")
                    f.write(input)
                    f.write("\n")
                line_accum += 1

    def input_rw(self):
        """
        Notes: 
        -10/19/23
            -instead of using the top most line box in the program for other words, I have change the use case to display 
                if whole line is correct/wrong
            -built in right tracker and wrong tracker just in case you need/want to track line accuracy

        
        """
        try:
            if self.lineTracker == 0: # for first line, DOES NOT OUTPUT right or wrong
                self.rw = " "
            elif self.word[self.lineTracker-1] == self.storeWords[-1]: # if input text meets model == RIGHT
                self.rw = "Right!" 
                self.rw_color = (0,255,0)                
                self.rightTracker += 1
            elif self.word[self.lineTracker-1] != self.storeWords[-1]: # if input text doesn't meet model == WRONG
                self.rw = "Wrong!"
                self.rw_color = (255,0,0)
                self.wrongTracker += 1
            else:
                print("input_rw ERROR, please see def input_rw(self):")
        except: #for last line DOES NOT OUTPUT right or wrong
            self.rw = " "

def main():
    TypingGame().run()


if __name__ == main():
    main()
