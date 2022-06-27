from guizero import App, Text, PushButton, Box, Drawing

# Map of short names to long names
book_map = {}
book_map['GEN'] = 'Genesis'
book_map['EX'] = 'Exodus'
book_map['LEV'] = 'Leviticus'
book_map['NUM'] = 'Numbers'
book_map['DEU'] = 'Deuteronomy'
book_map['JOS'] = 'Joshua'
book_map['JUD'] = 'Judges'
book_map['RUT'] = 'Ruth'
book_map['1SA'] = '1 Samuel'
book_map['2SA'] = '2 Samuel'
book_map['1KI'] = '1 Kings'
book_map['2KI'] = '2 Kings'
book_map['1CH'] = '1 Chronicles'
book_map['2CH'] = '2 Chronicles'
book_map['EZR'] = 'Ezra'
book_map['NEH'] = 'Nehemiah'
book_map['EST']= 'Esther'
book_map['JOB'] = 'Job'
book_map['PSA'] = 'Psalms'
book_map['PRV'] = 'Proverbs'
book_map['ECC'] = 'Ecclesiastes'
book_map['SOS'] = 'Song of Solomon'
book_map['IS'] = 'Isaiah'
book_map['JER'] = 'Jeremiah'
book_map['LAM'] = 'Lamentations'
book_map['EZK'] = 'Ezekiel'
book_map['DAN'] = 'Daniel'
book_map['HOS'] = 'Hosea'
book_map['JOL'] = 'Joel'
book_map['AMS'] = 'Amos'
book_map['OBD'] = 'Obadiah'
book_map['JNH'] = 'Jonah'
book_map['MIC'] = 'Micah'
book_map['NAH'] = 'NAH''Nahum'
book_map['HBK'] = 'Habakkuk'
book_map['ZPH'] = 'Zephaniah'
book_map['HAG'] = 'Haggai'
book_map['ZCH'] = 'Zechariah'
book_map['MAL'] = 'Malachi'
book_map['MAT'] = 'Matthew'
book_map['MK'] = 'Mark'
book_map['LK'] = 'Luke'
book_map['JN'] = 'John'
book_map['ACT'] = 'Acts'
book_map['ROM'] = 'Romans'
book_map['1CO'] = '1 Corinthians'
book_map['2CO'] = '2 Corinthians'
book_map['GAL'] = 'Galatians'
book_map['EPH'] = 'Ephesians'
book_map['PHI'] = 'Philippians'
book_map['COL'] = 'Colossians'
book_map['1TH'] = '1 Thessalonians'
book_map['2TH'] = '2 Thessalonians'
book_map['1TI'] = '1 Timothy'
book_map['2TI'] = '2 Timothy'
book_map['TIT'] = 'Titus'
book_map['PHM'] = 'Philemon'
book_map['HEB'] = 'Hebrews'
book_map['JMS'] = 'James'
book_map['1PT'] = '1 Peter'
book_map['2PT'] = '2 Peter'
book_map['1JN'] = '1 John'
book_map['2JN'] = '2 John'
book_map['2JN'] = '3 John'
book_map['JD'] = 'Jude'
book_map['REV'] = 'Revelation'

bible_file = './bible.txt'
ICON_EXIT = './exit.png'
ICON_PLAY = './play.png'
ICON_PAUSE = './pause.png'
ICON_FAST_FORWARD = './fast_forward.png'
ICON_NEXT = './next.png'
ICON_PREV = './prev.png'
ICON_REWIND = './rewind.png'
ICON_WIDTH = 48
ICON_BG = "white"
SCREEN_ROWS = 6
SCREEN_COLS = 30
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
BORDER_PADDING = 5
BORDER_COLOR = "green"
BIBLE_FONT_SIZE = 32
TIME_SECOND = 1000  # 1000 ms = 1 s
TRUNC_CHARS = "..."
appendString = '*' * SCREEN_COLS
spaceString = ' ' * SCREEN_COLS
REWIND_FF_AMOUNT = 20  # verses to skip
paused = False
textItems = {str: Text}
curVerse = 0
startPos = 0
curLine = 1
lastPos = 0
moreChunks = True
verses = []
app = App

versesDelay = 8 * TIME_SECOND
topPadding = Drawing
bottomPadding = Drawing

def get_book_Name(verse):
    global book_map

    pos = verse.find(' ')
    if pos > 0:
        book = verse[0:pos]

        try:
            long_book = book_map[book]
        except KeyError:
            return book

        if len(long_book) > 0:
            return long_book

        return book

    return ""


def init_me():
    global textItems, app

    newFontSize = get_bible_font_size()

    for txtNum in range(SCREEN_ROWS):
        textItems['txt' + str(txtNum)].text_size = newFontSize

    topPadding.width = app.width
    bottomPadding.width = app.width
    app.after(20, display_verse)


def get_bible_font_size():
    global app

    return int(BIBLE_FONT_SIZE * (app.width / SCREEN_WIDTH))


def get_screen_cols():
    global SCREEN_COLS

    return SCREEN_COLS


def go_faster():
    global TIME_SECOND, versesDelay

    if versesDelay >= (2 * TIME_SECOND):  # minimum is 1 second delay
        versesDelay -= TIME_SECOND


def go_slower():
    global TIME_SECOND, versesDelay

    # no limit, go as slow as yu want
    versesDelay += TIME_SECOND


def init_chunk_values():
    global curVerse, startPos, curLine, lastPos, moreChunks
    startPos = 0
    curLine = 1
    lastPos = 0
    moreChunks = True


def prev():
    global curVerse, paused

    lastPaused = paused

    if not paused:
        paused = True

    if curVerse > 0:
        curVerse -= 1
        init_chunk_values()
        show_next_verse()

    paused = lastPaused


def go_next():  # next is a reserved word
    global curVerse, verses, paused

    last_paused = paused

    if not paused:
        paused = True

    if curVerse < (len(verses) - 1):
        curVerse += 1
        init_chunk_values()
        show_next_verse()

    paused = last_paused


def rewind():
    global curVerse, paused

    lastPaused = paused

    if not paused:
        paused = True

    if curVerse > REWIND_FF_AMOUNT:
        curVerse -= REWIND_FF_AMOUNT
        init_chunk_values()
        show_next_verse()

    paused = lastPaused


def fast_forward():
    global curVerse, verses, paused

    lastPaused = paused

    if not paused:
        paused = True

    if curVerse < (len(verses) - REWIND_FF_AMOUNT):
        curVerse += REWIND_FF_AMOUNT
        init_chunk_values()
        show_next_verse()

    paused = lastPaused


def do_quit():
    global paused
    global app

    paused = True

    try:
        app.cancel(display_verse)
    except:
        print("Error canceling displayVerse in doQuit")

    app.after(10, exit_app)


def exit_app():
    global app

    print('We are outta here!')

    try:
        app.destroy()
    except:
        print("Error destroying app")


def pause_play():
    global paused
    global app

    paused = not paused
    if paused:
        pauseButton.image = ICON_PLAY
    else:
        pauseButton.image = ICON_PAUSE
        app.after(20, display_verse)


def load_bible():
    # Using readlines() 
    file1 = open(bible_file, 'r', encoding="utf-8", errors="ignore")
    return file1.readlines()


def reset_screen():
    global txt1, txt2, txt3, txt4

    for txtNum in range(SCREEN_ROWS):
        textItems['txt' + str(txtNum)].value = ''


def print_screen(line, reset):

    if reset:
        reset_screen()

    textItems['txt' + str(curLine - 1)].value = line


def get_next_chunk_pos(verse, max_chars, truncate):
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
            # We need to allow room for ...
            spacePos = verse.rindex(' ', startPos, lastPos - 1)

            if spacePos != -1 and spacePos > startPos:
                lastPos = spacePos

    return lastPos


# this is actually called after curVerse is modified,
# so it should already be pointing to next verse to display
def show_next_verse():
    global txtNextVerse, curVerse, verses,  txtBookName

    if curVerse < len(verses):
        verse = verses[curVerse]

        book = get_book_Name(verse)

        if len(book) > 0:
            txtBookName.value = "  BOOK: " + book

        dashPos = verse.index('-')
        if dashPos != -1:
            toShow = verse[0:dashPos - 1]
            txtNextVerse.value = "Next Verse: " + toShow


def display_verse():
    global curVerse
    global paused
    global startPos
    global curLine
    global lastPos
    global moreChunks
    global VERSES_DELAY
    global app

    line = ""

    if not paused:
        verse = verses[curVerse].rstrip()

        while moreChunks:
            lastPos = get_next_chunk_pos(verse, SCREEN_COLS, curLine == 4)

            if lastPos == -1:
                moreChunks = False
            else:
                moreChunks = lastPos < len(verse)

                if curLine == SCREEN_ROWS and moreChunks:
                    line = verse[startPos:lastPos] + TRUNC_CHARS
                else:
                    line = verse[startPos:lastPos]

                print_screen(line, curLine == 1)

                if moreChunks:
                    startPos = lastPos

                    if verse[startPos] == ' ':
                        startPos += 1

                    curLine += 1
                    if curLine == (SCREEN_ROWS + 1):
                        curLine = 1
                        app.after(versesDelay, display_verse)
                        return

        curVerse += 1
        if curVerse >= len(verses):
            curVerse = 0

        show_next_verse()

        startPos = 0
        curLine = 1
        lastPos = 0
        moreChunks = True

        app.after(versesDelay, display_verse)


verses = load_bible()

app = App(title="pyBibleVerses", layout="grid",
          width=800, height=400, bg=(0, 0, 20))

# Add Widgets

# 1. Add row of controls for traversal, etc
controlBox = Box(app, align='left', grid=[0, 0], layout="grid")

# Add control buttons
rewindButton = PushButton(controlBox, width=ICON_WIDTH, image=ICON_REWIND,
                          grid=[0, 0], command=rewind)
prevButton = PushButton(controlBox, width=ICON_WIDTH, image=ICON_PREV,
                        grid=[1, 0], command=prev)
pauseButton = PushButton(controlBox, width=ICON_WIDTH, image=ICON_PAUSE,
                         grid=[2, 0], command=pause_play)
nextButton = PushButton(controlBox, width=ICON_WIDTH, image=ICON_NEXT,
                        grid=[3, 0], command=go_next)
ffButton = PushButton(controlBox, width=ICON_WIDTH, image=ICON_FAST_FORWARD,
                      grid=[4, 0], command=fast_forward)
quitButton = PushButton(controlBox, width=ICON_WIDTH, image=ICON_EXIT,
                        grid=[5, 0],
                        command=do_quit)

# add some padding
pad1 = Text(controlBox, text="  ", grid=[6, 0])

slowerButton = PushButton(controlBox, text="Slower", grid=[7, 0],
                          command=go_slower)
fasterButton = PushButton(controlBox, text="Faster", grid=[8, 0],
                          command=go_faster)
# more padding
pad2 = Text(controlBox, text="  ", grid=[9, 0])

# Show what verse is next
txtNextVerse = Text(controlBox, size=16, text="Next Verse",
                    color="white", width="fill", align="left",
                    grid=[10, 0])

pad2 = Text(controlBox, text="    ", grid=[11, 0])
txtBookName = Text(controlBox, size=20, text="Book",
                   color="blue", width="fill", align="right",
                   grid=[12, 0])

rewindButton.bg = ICON_BG
prevButton.bg = ICON_BG
pauseButton.bg = ICON_BG
nextButton.bg = ICON_BG
ffButton.bg = ICON_BG
quitButton.bg = ICON_BG
slowerButton.text_color = "white"
fasterButton.text_color = "white"

# 2. Now add text area to display verse
txtEmpty1 = Text(app, text=spaceString, align="left",
                 grid=[0, 1], font="Courier", width="fill",
                 size=BIBLE_FONT_SIZE, color="white")

# txtTop = Text(app, text=appendString,align="left",
#              grid=[0,2], font="Courier", width="fill",
#              size=BIBLE_FONT_SIZE, color="white")

topPadding = Drawing(app, height=20, width=app.width, grid=[0, 2])

txtEmpty2 = Text(app, text=spaceString, align="left",
                 grid=[0, 3], font="Courier", width="fill",
                 size=BIBLE_FONT_SIZE, color="white")

contentBox = Box(app, grid=[0, 4], layout="grid", width=app.width)
# contentBox.set_border(BORDER_PADDING,BORDER_COLOR)


for txtNum in range(SCREEN_ROWS):
    textItems['txt' + str(txtNum)] = Text(contentBox, text=str(txtNum), align="left", grid=[0, txtNum],
                                          font="Courier", width="fill", size=BIBLE_FONT_SIZE, color="white")

# txtBottom = Text(app, text=appendString,align="left",
#              grid=[0,3 + SCREEN_ROWS], font="Courier", width="fill",
#              size=BIBLE_FONT_SIZE, color="white")

txtEmpty3 = Text(app, text=spaceString, align="left",
                 grid=[0, 5], font="Courier", width="fill",
                 size=BIBLE_FONT_SIZE, color="white")

bottomPadding = Drawing(app, height=20, width=app.width, grid=[0, 6])

topPadding.bg = "blue"
bottomPadding.bg = "blue"

app.full_screen = True

# pauseButton.after(20, displayVerse)
app.after(20, init_me)

app.display()
