import random, re, os, sys, subprocess
from tkinter import *


# location of Itunes music folder
# replace 'username' below with the username on your computer
path = '/Users/seandavis/Music/iTunes/iTunes Media/Music/'


class Application(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()
        master.bind('<Return>', self.update)

    def create_widgets(self):
        # Labels
        self.board_label = Label(self,text= working_song, font=('Monaco', 25))
        self.attempts_label = Label(self,text='Attempts Remaining: ' + str(attempts), font=(None, 20))
        self.letters_guessed_label = Label(self,text='Letters Guessed: ' + str(guessed.sort()), font=(None, 20))
        self.guess_label= Label(self,text='Enter a letter:', font=(None, 20))
        self.solve_label = Label(self,text='Enter the full song:', font=(None, 20))
        self.error_label = Label(self, text='Invalid Input', font=(None, 20))
        self.correct_label = Label(self, text = '\nCorrect!', font=(None, 20))
        self.game_over_label = Label(self, text ='Game Over', font=(None, 20))
        self.incorrect_solve_label = Label(self, text = 'Incorrect', font=(None, 20))
        self.message_label = Label(self, font=(None, 20))
        self.artist_label = Label(self,text=all_songs[song][0],font=(None, 20))
        self.album_label = Label(self,text=all_songs[song][1],font=(None, 20))
        string = 'The song was ' + song + ' by ' + all_songs[song][0] + ' from the album ' + all_songs[song][1]
        self.correct_song_label = Label(self, text= string, wraplengt=400,font=(None, 20))

        self.board_label.grid(row=2,column=0,columnspan=4, sticky=W, padx = (30,0))
        self.attempts_label.grid(row=0,column=0,sticky=W)
        self.letters_guessed_label.grid(row=1,column=0,sticky=W,columnspan=4)
        self.guess_label.grid(row=3,column=0)


        # Entry Box
        self.user_guess=Entry(self,width=15,font=(None, 20))
        self.user_guess.grid(row=4,column=0)


       # Radio Buttons
        self.mode=StringVar()
        self.mode.set('guess')
        
        self.guess_radio_button = Radiobutton(self,text='Guess',variable=self.mode,value='guess',
                                              command=self.guess_mode,font=(None, 20))
        self.guess_radio_button.grid(row=5,column=0,sticky=W)
        
        self.solve_radio_button = Radiobutton(self,text='Solve',variable=self.mode,value='solve',
                                              command=self.solve_mode,font=(None, 20))
        self.solve_radio_button.grid(row=5,column=0,sticky=E)

 
        # Buttons
        self.show_artist_button = Button(self,text='Show Artist',command=self.show_artist,font=(None, 20))
        self.show_album_button = Button(self,text='Show Album',command=self.show_album,font=(None, 20))
        self.restart_button = Button(self,text='Restart',command=self.restart,font=(None, 20))
        self.go_button = Button(self,text="Go!",command=self.update, font=(None, 20))
        self.play_song_button = Button(self,text="Play Song",command=lambda:open_file(all_songs[song][2]), font=(None, 20))

        self.show_artist_button.grid(row=6,column=0,sticky=W)
        self.show_album_button.grid(row=7,column=0,sticky=W)
        self.restart_button.grid(row=0,column=1,columnspan=4,sticky=W)
        self.go_button.grid(row=4,column=1,sticky=W)




        
    def show_artist(self):
        self.artist_label.grid(row=6,column=1,columnspan=3,sticky=W)
        
    def show_album(self):
        self.album_label.grid(row=7,column=1,columnspan=3,sticky=W)
        
    def guess_mode(self):
        self.solve_label.grid_forget()
        self.guess_label.grid(row=3,column=0)
        
    def solve_mode(self):
        self.guess_label.grid_forget()
        self.solve_label.grid(row=3,column=0)

    def game_over(self,win):
        if win:
            self.correct_label.grid(row=9,column=0,columnspan=3)
        else:
            self.game_over_label.grid(row=9,column=0,columnspan=3)
            
        self.correct_song_label.grid(row=10,column=0,columnspan=3)
        self.play_song_button.grid(row=11,column=0,columnspan=3)
        self.user_guess.grid_forget()
        self.go_button.grid_forget()
        self.guess_radio_button.grid_forget()
        self.solve_radio_button.grid_forget()
        self.guess_label.grid_forget()
        self.solve_label.grid_forget()
        self.message_label.grid_forget()


    # show/hide/reset widgets after the user chooses to restart the game
    def restart(self):
        # pick new song and reset some variables 
        initialize()
        
        # show widgets that are hidden after game ends
        self.go_button.grid(row=4,column=1,sticky=W)
        self.user_guess.grid(row=4,column=0)
        self.guess_radio_button.grid(row=5,column=0,sticky=W)
        self.solve_radio_button.grid(row=5,column=0,sticky=E)
        self.guess_label.grid(row=3,column=0)
        self.solve_label.grid(row=3,column=0)
        # set the 'Guess' radio button as active
        self.mode.set('guess')

        # hide widgets that might be present at end of game
        self.message_label.grid_forget()
        self.game_over_label.grid_forget()
        self.incorrect_solve_label.grid_forget()
        self.error_label.grid_forget()
        self.correct_song_label.grid_forget()
        self.artist_label.grid_forget()
        self.album_label.grid_forget()
        self.correct_label.grid_forget()
        self.play_song_button.grid_forget()

        # reset the text on labels
        self.attempts_label['text'] = 'Attempts Remaining: ' + str(attempts)
        self.letters_guessed_label['text'] = 'Letters Guessed: ' + ','.join(sorted(guessed)).replace(',', ' ')        
        self.board_label['text'] = working_song
        self.artist_label['text'] = all_songs[song][0]
        self.album_label['text'] = all_songs[song][1]
        string = 'The song was ' + song + ' by ' + all_songs[song][0] + ' from the album ' + all_songs[song][1]
        self.correct_song_label['text'] = string
        self.user_guess.delete(0, 'end')
        

    # this is called after the 'Go!' button or 'Enter' key is pressed
    def update(self, event=None):
        global working_song, song, attempts, guessed

        # get user's input from entry box 
        user_response = self.user_guess.get().upper()
        
        # hide labels that may be present
        self.incorrect_solve_label.grid_forget()
        self.message_label.grid_forget()
        self.error_label.grid_forget()

        # reset the entry box to be blank
        self.user_guess.delete(0, 'end')

        # Solve radio button is selected
        if self.mode.get() == 'solve':

            # if correct song is entered
            if user_response == song.upper():
                self.board_label['text'] = song.upper()
                self.game_over(True)
                
            # if nothing is entered
            elif user_response == '':
                self.error_label.grid(row=4,column=3,sticky=W)
                
            # if user is wrong
            else:
                self.incorrect_solve_label.grid(row=4,column=3,sticky=W)
                attempts -= 1
                self.attempts_label['text'] = 'Attempts Remaining: ' + str(attempts)

                
        # Guess radio button is selected
        elif self.mode.get() == 'guess':           

            # make sure the guess is valid
            if is_valid(user_response, valid_input):
                # input_handler will tell if check if the guess is a correct letter
                # and will update working_song, attempts, and create a response message
                working_song,attempts,message = input_handler(user_response, song, working_song, attempts)
                self.attempts_label['text'] = 'Attempts Remaining: ' + str(attempts)
                self.message_label['text'] = message
                self.message_label.grid(row=4,column=3,sticky=W)
                self.board_label['text'] = working_song

                # update Letters Guessed label
                self.letters_guessed_label['text'] = 'Letters Guessed: ' + ','.join(sorted(guessed)).replace(',', ' ')

            else:
                self.error_label.grid(row=4,column=3,sticky=W)
                
            
            # song has been filled in
            if working_song == song.upper():
                self.correct_label.grid(row=9,column=0,columnspan=3)
                self.game_over(True)
                
            # song is not filled in and attempts has reached 0
            elif attempts == 0:
                self.game_over(False)

                


# opens a file on all platforms (hopefully)
# have only tested it on a mac
def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])



# takes the name of an artists and adds all songs by that artist to all_songs
# all_songs is a dictionary with each key's value being a list
    # example: Come Together: ['The Beatles', 'Abbey Road', '<location of file>']
def song_adder (artist):
    # creates a list of all the albums by artist
    albums = os.listdir(path + artist)

    # removes .DS_store from the list
    for i in range(len(albums) - 1, -1, -1):
        if albums[i] == '.DS_Store':
            del albums[i]
            
    # creates a list of all the songs in album
    for album in albums:
        songs = os.listdir(path + artist +"/" + album)

        # removes .DS_store from the list
        for i in range(len(songs) - 1, -1, -1):
            if songs[i] == '.DS_Store':
                del songs[i]

        # removes the track listing at the beginning of each song title and the extension at the end
        # and then adds song to dictionary 'all_songs'
        for song in songs:
            location = path + artist + "/" + album + "/" + song
            song = re.sub('\d-\d\d ', "", song)
            song = re.sub('\d\d ', "", song)
            song = song[:-4]
            all_songs[song] = [artist, album, location]

# picks a random song from all_songs
def song_selector():
    song = random.choice(list(all_songs.keys()))
    return song

# takes a word or words and returns a tuple with all the letters in the words replaced
# with '_' and the initial word or words
    # example: ('____ ________', 'Come Together')
def blank_words(word):
    working_word = ""
    for letter in word:
        if letter.isalpha():
            working_word += "_"
        else:
            working_word += letter
    return working_word


# displays options for the user and gets input from user
# only returns the input if it's in the list 'valid', otherwise it runs itself again
def is_valid(user_input, valid):
    if user_input in valid and user_input not in guessed:
        return True
    else:
        return False


def input_handler(user_input,song,working_song,attempts):
    if user_input in song.upper():
        count = 0
        for i in range(len(song)):
            if song[i].upper() == user_input:
                working_song = working_song[:i] + user_input + working_song[i+1:]
                count += 1
        message = ('There are '+ str(count) + ' ' + user_input + "'s")

        # removes the letter from valid_input so it can't be guessed twice
        valid_input.remove(user_input)
        guessed.append(user_input)
        
    else:
        message = (user_input + ' is not in the title')

        # adds the letter to the guessed list
        if user_input not in guessed:
            guessed.append(user_input)
    attempts -= 1

    return (working_song,attempts,message)



def create_song_dict():
    global all_songs
    all_songs = {}

    # use song_adder function below with as many artists as desired
    song_adder('The Beatles')
    #song_adder('Queen')
    


def initialize():
    global valid_input, guessed, working_song, attempts, song
    attempts = 10
    valid_input = ['QUIT','SOLVE','ARTIST','ALBUM','A','B','C','D','E','F','G','H','I','J','K','L','M','N',
                   'O','P','Q','R','S','T','U','V','W','X','Y','Z']
    guessed = []
    
    # picks song and makes a blank version of it
    song = song_selector()
    working_song = blank_words(song)
    

# main
def main():
    root = Tk()
    root.title('TITLE TITLE GOOD TITLE')
    root.geometry('550x450')
    root.resizable(width = TRUE, height = TRUE)

    app = Application(root)
    root.mainloop()

create_song_dict()
initialize()
main()
