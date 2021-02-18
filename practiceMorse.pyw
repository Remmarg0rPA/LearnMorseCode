#! python3
import wikipedia, time, winsound
import tkinter as tk
import threading

MorseAlphabet = {
	'a':'.-',	'b':'-...',	'c':'-.-.',
	'd':'-..',	'e':'.',	'f':'..-.',	
	'g':'--.',	'h':'....',	'i':'..',
	'j':'.---',	'k':'-.-',	'l':'.-..',
	'm':'--',	'n':'-.',	'o':'---',
	'p':'.--.',	'q':'--.-',	'r':'.-.',
	's':'...',	't':'-',	'u':'..-',
	'v':'...-',	'w':'.--',	'x':'-..-',
	'y':'-.--',	'z':'--..',
	'1':'.----',	'2':'..---',	'3':'...--',
	'4':'....-',	'5':'.....',	'6':'-....',
	'7':'--...',	'8':'---..',	'9':'----.',
	'0':'-----'
}
STOP = False
MODE = 1

#Converts letters to morse code
def toMorse(text):
        global MorseAlphabet
        message = ''
        text = str(text)

        #Transalates all characters that can be translated
        i = 0
        while i < len(text):
                #Add the morse equivalent of  letter
                if text[i] in MorseAlphabet.keys():
                        message += MorseAlphabet[text[i]] + ' '
                #If it is a space it is kept
                elif text[i] == ' ':
                        message +='  '
                i +=1
        
        #print(message)
        return message



#Plays the morse code as sound
def playMorse():
    global page_text, STOP

    #generates the morse code
    text = toMorse(page_text)

    #Creates a queue with what to send
    sendList = []
    for char in text:
    	sendList.append(char)

    in_box.delete('2.0', tk.END)
    window.update()

    freq = int(freq_entry.get())
    speed = int(speed_entry.get())

    time.sleep(0.5)
    for char in sendList:
            
        if STOP:
                STOP = False
                return None
        
        #Plays a . if it is a .
        if char == '.':
            if not MODE:
                    blink(speed)
            else:
                    winsound.Beep(freq, speed)

        #Plays a - if it is a -
        elif char == '-':
            if not MODE:
                    blink(speed*2)
            else:
                    winsound.Beep(freq, speed*2)

        #Sleeps if it is a space
        elif char == ' ':
            time.sleep(speed/1000)




def wiki_article():
    global page_text
    #Gets a random wikipedia article and downloads the summary of it
    while True:
        try:
            page_name = wikipedia.random(1)
            page_text = wikipedia.page(page_name).summary
            page_text = page_text.lower().strip()
            break
        except:
                pass

    #Deltetes all text in the text box when a new message is created
    in_box.delete('1.0', tk.END)
    window.update()
    
    #Removes all characters that cannot be translated to morse code
    i = 0
    while i < len(page_text):
        if page_text[i] not in MorseAlphabet.keys() and page_text[i] != ' ':
            page_text = page_text[:i] + page_text[i+1:]

        else:
            i +=1

    if len(page_text) > 30:
        page_text = page_text[:60]
        
    page_text = page_text.strip()




def checkEntry():
    global page_text

    #Removes last lines in text box ang get the entered text
    in_box.delete('2.0', tk.END)    
    e = in_box.get('1.0', tk.END)
    
    e = entry.strip()
    page_text = page_text.strip()
    
    if e == page_text.lower():
        in_box.insert(tk.END, '\nYou are correct!')
    else:
        in_box.insert(tk.END, '\nYour guess was incorrect. Try again!')
    
    window.update()





def showAns():
        global page_text
        in_box.delete('2.0', tk.END)
        in_box.insert('2.0', f'\nThe answer is "{page_text}"')



#Create functions that only run a new tread if there are no other already created
#This allows the user to write in the text box at the same time as the unction i run
THREAD = 0
def play():
        if threading.activeCount() <= 2:
                THREAD = threading.Thread(target=playMorse)
                THREAD.start()
        
def new():
        if threading.activeCount() <= 2:
                THREAD = threading.Thread(target=wiki_article)
                THREAD.start()

def check():
        if threading.activeCount() <= 2:
                THREAD = threading.Thread(target=checkEntry)
                THREAD.start()
def show():
        if threading.activeCount() <= 2:
                THREAD = threading.Thread(target=showAns)
                THREAD.start()
def chmod():
        global MODE, mode, bcolor
        if not MODE:
                mode.configure(text='Audio')
                MODE = 1
        else:
                mode.configure(text='Light')
                MODE = 0
        window.update()

def blink(duration):
        global mode, bcolor
        mode.configure(bg='red')
        window.update()
        time.sleep(duration/1000)
        mode.configure(bg=bcolor)
        window.update()


def Stop():
        global STOP
        STOP = True


color = 'powderblue'#thistle'
bcolor = 'white'#palegreen'#lavender'

#Creates the window and gives it a title
window = tk.Tk()
window.configure(bg=color, padx=15, pady=5)
window.title('Practice Morse Code')

#Creates three frames
frame_a = tk.Frame(bg=color)
frame_a.pack()
frame_b = tk.Frame(bg=color)
frame_b.pack()
frame_c = tk.Frame(bg=color)
frame_c.pack()

#Places text box and name for it in frame_a, the top frame
label = tk.Label(text='Input Guess:', master=frame_a, bg=color)
label.pack()
in_box = tk.Text(master=frame_a, width=48, height=5)
in_box.pack()


#Creates two inputs for frequency and speed
freq_label = tk.Label(master=frame_b, text='Frequency:', bg=color)
freq_label.pack(side=tk.LEFT)
freq_entry = tk.Entry(master=frame_b)
freq_entry.pack(side=tk.LEFT)
freq_entry.insert('0', '1000')

speed_label = tk.Label(master=frame_b, text='Speed in m.s:', bg=color)
speed_label.pack(side=tk.LEFT)
speed_entry = tk.Entry(master=frame_b)
speed_entry.pack(side=tk.LEFT)
speed_entry.insert('0', '350')


#Creates 4 buttons in frame_b, the bottom frame
#Button that plays he morse code
play = tk.Button(text='Play',
                 width=7, height=2,
                 bg=bcolor,
                 master=frame_c,
                 command=play)
play.pack(side=tk.LEFT)

#Button that generates a new message
new = tk.Button(text='New',
                width=7, height=2,
                bg=bcolor,
                master=frame_c,
                command=new)
new.pack(side=tk.LEFT)

#Button that checks if input is correct
check = tk.Button(text='Check Guess',
                width=10, height=2,
                bg=bcolor,
                master=frame_c,
                command=check)
check.pack(side=tk.LEFT)

#Button that shows the answer
show = tk.Button(text='Show Answer',
                width=10, height=2,
                bg=bcolor,
                master=frame_c,
                command=show)
show.pack(side=tk.LEFT)

#Button that changes the mode (audio/light)
mode = tk.Button(text='Audio',
                width=7, height=2,
                bg=bcolor,
                master=frame_c,
                command=chmod)
mode.pack(side=tk.LEFT)

#Button that stops playing the morse code
stop = tk.Button(text='Stop',
                width=7, height=2,
                bg=bcolor,
                master=frame_c,
                command=Stop)
stop.pack(side=tk.LEFT)





#Starts by gettin an article so you can play it without
#pressing new message in the beginning
wiki_article()


window.mainloop()

#Makes the playMorse functoin terminate if it is running
STOP = True

