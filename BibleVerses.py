from guizero import App,Text,PushButton,Box,Drawing
import time
import tkinter

bible_file = './bible.txt'
ICON_EXIT = './exit.png'
ICON_PLAY = './play.png'
ICON_PAUSE = './pause.png'
ICON_FAST_FORWARD = './fast_forward.png'
ICON_NEXT = './next.png'
ICON_PREV = './prev.png'
ICON_REWIND = './rewind.png'
ICON_WIDTH = 48
ICON_BG="white"
SCREEN_ROWS = 6
SCREEN_COLS=30
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

BIBLE_FONT_SIZE=32 
TIME_SECOND = 1000 # 1000 ms = 1 s
TRUNC_CHARS = "..."
appendString = '*' * SCREEN_COLS
spaceString = ' ' * SCREEN_COLS
REWIND_FF_AMOUNT = 20 #verses to skip
paused = False
textItems = {str:Text}
curVerse = 0
startPos = 0
curLine = 1
lastPos = 0
moreChunks = True
verses = []
app = App
app = App
versesDelay = 8 * TIME_SECOND
topPadding = Drawing
bottomPadding = Drawing

def initMe():
    global textItems,app

    newFontSize = getBibleFontSize()

    for txtNum in range(SCREEN_ROWS):
        textItems['txt' + str(txtNum)].text_size = newFontSize

    topPadding.width = app.width
    bottomPadding.width = app.width

    app.after(20, displayVerse)

def getBibleFontSize():
    global app

    return int(BIBLE_FONT_SIZE * (app.width / SCREEN_WIDTH))

def getScreenCols():
    global SCREEN_COLS

    return SCREEN_COLS

def goFaster():
    global TIME_SECOND, versesDelay
    
    if versesDelay >= (2 * TIME_SECOND): # minimum is 1 second delay
        versesDelay -= TIME_SECOND

def goSlower():
    global TIME_SECOND, versesDelay
    
    # no limit, go as slow as yu want
    versesDelay += TIME_SECOND

def initChunkValues():
    global curVerse,startPos,curLine,lastPos,moreChunks    
    startPos = 0
    curLine = 1
    lastPos = 0
    moreChunks = True
    
def prev():
    global curVerse,paused
    
    lastPaused = paused;
    
    if not paused:
        paused = True;
    
    if curVerse > 0:
        curVerse -= 1
        initChunkValues()
        showNextVerse()

        
    paused = lastPaused

def goNext(): #next is a reserved word
    global curVerse,verses,paused

    lastPaused = paused;
    
    if not paused:
        paused = True;
    
    if curVerse < (len(verses) - 1):
        curVerse += 1
        initChunkValues()
        showNextVerse()

    paused = lastPaused
    
def rewind():
    global curVerse, paused

    lastPaused = paused;
    
    if not paused:
        paused = True;
   
    if curVerse > REWIND_FF_AMOUNT:
        curVerse -= REWIND_FF_AMOUNT
        initChunkValues()
        showNextVerse()


    paused = lastPaused
    
def fastForward():
    global curVerse,verses,paused

    lastPaused = paused;
    
    if not paused:
        paused = True;
       
    if curVerse < (len(verses) - REWIND_FF_AMOUNT):
        curVerse += REWIND_FF_AMOUNT
        initChunkValues()
        showNextVerse()

    
    paused = lastPaused

def doQuit():
    global paused
    global app
    
    paused = True
    
    try:
        app.cancel(displayVerse)
    except:
        print("Error canceling displayVerse in doQuit")
        
    app.after(10,exitApp)

def exitApp():
    global app

    print('We are outta here!')
    
    try:
        app.destroy()
    except:
        print("Error destroying app")

def pausePlay():
    global paused
    global app
    
    paused = not paused
    if paused:
        pauseButton.image = ICON_PLAY
    else:
        pauseButton.image = ICON_PAUSE
        app.after(20, displayVerse)
        
def loadBible():
    # Using readlines() 
    file1 = open(bible_file,'r',encoding="utf-8",errors="ignore") 
    return file1.readlines()          

def resetScreen():
    global txt1,txt2,txt3,txt4
 
    for txtNum in range(SCREEN_ROWS):
        textItems['txt' + str(txtNum)].value = ''

    
def printScreen(line, reset):
    global txt1,txt2,txt3,txt4,txt5,txt6 

    print('Printing to line ' +
          str(curLine) +
          ', Text to print: ' +
          line)
    
    if reset:
        resetScreen()

    textItems['txt' + str(curLine - 1)].value = line    

    
def getNextChunkPos(verse, max_chars, truncate):
    global lastPos
    spacePos = 0
    lastPos = startPos + max_chars
    
    if lastPos > len(verse):
        lastPos = len(verse)
    else:
        spacePos = verse.rindex(' ', startPos, lastPos)

        if spacePos != -1 and spacePos > startPos:
            lastPos = spacePos

        if truncate and ((lastPos - startPos) > (max_chars - len(TRUNC_CHARS))):
            #We need to allow room for ...
            spacePos = verse.rindex(' ', startPos, lastPos - 1)
            
            if spacePos != -1 and spacePos > startPos:
                lastPos = spacePos

    return lastPos;

# this is actually called after curVerse is modified,
# so it should already be pointing to next verse to display
def showNextVerse():
    global txtNextVerse,curVerse,verses
    
    if curVerse < len(verses):
        verse = verses[curVerse]
        dashPos = verse.index('-')
        if dashPos != -1:
            toShow = verse[0:dashPos-1]
            txtNextVerse.value = "Next Verse: " + toShow

def displayVerse():
    global curVerse
    global paused 
    global startPos
    global curLine
    global lastPos
    global moreChunks
    global VERSES_DELAY
    global app
    
    line = ""


    print("Paused: " + str(paused))

    if not paused:
        verse = verses[curVerse].rstrip()
        
        while(moreChunks):
            lastPos = getNextChunkPos(verse, SCREEN_COLS, curLine == 4);

            if lastPos == -1:
                moreChunks = False
            else:
                moreChunks = lastPos < len(verse)

                if curLine == SCREEN_ROWS and moreChunks:
                    line = verse[startPos:lastPos] + TRUNC_CHARS
                else:
                    line = verse[startPos:lastPos]

                printScreen(line, curLine == 1);

                if moreChunks:
                    startPos = lastPos

                    if verse[startPos] == ' ':
                        startPos += 1;
                    
                    curLine += 1
                    if curLine == (SCREEN_ROWS + 1):
                        curLine = 1
                        app.after(versesDelay, displayVerse)
                        return
                        
                        
                    
        curVerse += 1
        if curVerse >= len(verses):
            curVerse = 0
        
        showNextVerse()
        
        startPos = 0
        curLine = 1
        lastPos = 0
        moreChunks = True
        
        app.after(versesDelay, displayVerse)
        
verses = loadBible()

app = App(title="pyBibleVerses", layout="grid",
          width=800, height=400, bg=(0,0,20))

#Add Widgets

# 1. Add row of controls for traversal, etc
myBox = Box(app, align='left', grid=[0,0], layout="grid")

# Add control buttons
rewindButton = PushButton(myBox, width=ICON_WIDTH, image=ICON_REWIND,
                        grid=[0,0], command=rewind)
prevButton = PushButton(myBox, width=ICON_WIDTH, image=ICON_PREV,
                        grid=[1,0], command=prev)
pauseButton = PushButton(myBox, width=ICON_WIDTH, image=ICON_PAUSE,
                        grid=[2,0], command=pausePlay)
nextButton = PushButton(myBox, width=ICON_WIDTH, image=ICON_NEXT,
                        grid=[3,0], command=goNext)
ffButton = PushButton(myBox, width=ICON_WIDTH, image=ICON_FAST_FORWARD,
                        grid=[4,0], command=fastForward)
quitButton = PushButton(myBox, width=ICON_WIDTH, image=ICON_EXIT,
                        grid=[5,0],
                        command=doQuit)

# add some padding
pad1 = Text(myBox, text="  ", grid=[6,0])

slowerButton = PushButton(myBox, text="Slower",grid=[7,0],
                          command=goSlower)
fasterButton = PushButton(myBox, text="Faster",grid=[8,0],
                          command=goFaster)
# more padding
pad2 = Text(myBox, text="  ", grid=[9,0])

# Show what verse is next
txtNextVerse = Text(myBox, size =16, text="Next Verse", 
	color="white", width="fill", align="left",
	grid=[10,0])

rewindButton.bg=ICON_BG
prevButton.bg=ICON_BG
pauseButton.bg=ICON_BG
nextButton.bg=ICON_BG
ffButton.bg=ICON_BG
quitButton.bg=ICON_BG
slowerButton.text_color = "white"
fasterButton.text_color = "white"



# 2. Now add text area to display verse
txtEmpty1 = Text(app, text=spaceString,align="left",
              grid=[0,1], font="Courier", width="fill",
              size=BIBLE_FONT_SIZE, color="white")

#txtTop = Text(app, text=appendString,align="left",
#              grid=[0,2], font="Courier", width="fill",
#              size=BIBLE_FONT_SIZE, color="white")

topPadding = Drawing(app,height=20,width=app.width,grid=[0,2])

txtEmpty2 = Text(app, text=spaceString,align="left",
              grid=[0,3], font="Courier", width="fill",
              size=BIBLE_FONT_SIZE, color="white")

for txtNum in range(SCREEN_ROWS):
    textItems['txt' + str(txtNum)] = Text(app, text=str(txtNum), align="left", grid=[0,4 + txtNum],
            font="Courier", width="fill", size=BIBLE_FONT_SIZE, color="white")


#txtBottom = Text(app, text=appendString,align="left",
#              grid=[0,3 + SCREEN_ROWS], font="Courier", width="fill",
#              size=BIBLE_FONT_SIZE, color="white")

txtEmpty3 = Text(app, text=spaceString,align="left",
              grid=[0,4 + SCREEN_ROWS], font="Courier", width="fill",
              size=BIBLE_FONT_SIZE, color="white")

bottomPadding = Drawing(app,height=20,width=app.width,grid=[0,5 + SCREEN_ROWS])

topPadding.bg = "blue"
bottomPadding.bg = "blue"

app.full_screen=True

#pauseButton.after(20, displayVerse)
app.after(20, initMe)

app.display()
