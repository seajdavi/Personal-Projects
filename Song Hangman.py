# Some characters like ':' and '/' and '?' get converted to '_' making it look wrong
    # example: 'California Saga/Big Sur' goes to 'California Saga_Big Sur'
    # but you can't guess '/'. The answer is 'California Saga_Big Sur'
    # no need to guess '_' though, unless solving
# songs with only numbers are insta-wins since numbers converted to underscores
# when song plays, you have to click in python window before entering anything



import random, re, os, sys, subprocess

# location of Itunes music folder
# replace 'username' with the username on your computer below
path = '/Users/username/Music/iTunes/iTunes Media/Music/'

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
def SongAdder (artist):
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
def SongSelector():
    song = random.choice(list(all_songs.keys()))
    return song

# takes a word or words and returns a tuple with all the letters in the words replaced
# with '_' and the initial word or words
    # example: ('____ ________', 'Come Together')
def BlankWords(word):
    working_word = ""
    for letter in word:
        if letter.isalpha():
            working_word += "_"
        else:
            working_word += letter
    return working_word


# takes the song and what the user has guessed of that song so far
# returns true if they're equal
def IsCorrect(song, working_song):
    if song.upper() == working_song:
        # displays the song info
        print("Correct!")
        print("The song title was", song, "by", all_songs[song][0], "from the album", all_songs[song][1])
        return True
    else:
        return False

def PlayAgain(song):
    # asks user if they wan to play the song
    while True:
        replay = input("Play song? (y/n) ").upper()
        if replay == "Y":
            open_file(all_songs[song][2])
            break
        elif replay == "N":
            break

    # asks user if they want to play again
    while True:
        replay = input("Play the game again? (y/n) ").upper()
        if replay == "Y":
            return True
        elif replay == "N":
            return False
            



# displays options for the user and gets input from user
# only returns the input if it's in the list 'valid', otherwise it runs itself again
def GetInput(valid):
# asks user for input
    print("- Enter the letter you want to guess")
    print("- Or enter 'Solve' to solve for the entire song title")
    print("- Or enter 'Artist' to see the artist")
    print("- Or enter 'Album' to see the album")
    print("- Or enter 'Quit' to give up")
    
    user_input = input("\nYour Guess: ").upper()
    if user_input in valid and user_input not in guessed:
        return user_input
    else:
        print("\nInvalid Input\n")
        return GetInput(valid)

           
def DisplayBoard(progress, attempts):
    guessed.sort()
    print("\n\n\t\t\t" + progress +"\n")
    print("Letters Guessed:", guessed)


def InputHandler(user_input,song,working_song,attempts):
    
    if user_input == "QUIT":
        return ("QUIT", attempts)
    
    elif user_input == "SOLVE":
        solve = input("Enter the full song title: ").upper()
        if solve == song.upper():
            working_song = solve
        else:
            print("Incorrect")
        attempts += 1  
        
    elif user_input == "ARTIST":
        print("The artist of this song is", all_songs[song][0])
        
    elif user_input == "ALBUM":
        print("The song is from the album", all_songs[song][1])
        
    else:
        if user_input in song.upper():
            count = 0
            for i in range(len(song)):
                if song[i].upper() == user_input:
                    working_song = working_song[:i] + user_input + working_song[i+1:]
                    count += 1
            print("There are", count, user_input + "'s")

            # removes the letter from valid_input so it can't be guessed twice
            valid_input.remove(user_input)
            guessed.append(user_input)
            
        else:
            print(user_input, "is not in the title")

            # adds the letter to the guessed list
            if user_input not in guessed:
                guessed.append(user_input)
        attempts += 1
            
    return (working_song,attempts)
            

def Game(attempts):
    # picks song and makes a blank version of it
    song = SongSelector()
    working_song = BlankWords(song)

    # shows what the player has guessed and asks for more guesses until they get it right
    while working_song != song.upper() and working_song != 'QUIT':
        DisplayBoard(working_song, attempts)
        user_input = GetInput(valid_input)
        working_song,attempts = InputHandler(user_input, song, working_song,attempts)
        print ("\nAttempts:", attempts, '\n')
        if attempts == 9:
            print('*************')
            print('FINAL ATTEMPT')
            print('*************')
        if attempts > 9:
            break

    if working_song == "QUIT":
        print("The song title was", song, "by", all_songs[song][0], "from the album", all_songs[song][1])

    else:
        if not IsCorrect(song, working_song):
            print ("You Lose")
            print("The song title was", song, "by", all_songs[song][0], "from the album", all_songs[song][1])


    if PlayAgain(song):
        initialize()
    else:
        print("\n\n\nGame Over")

def initialize():
    global all_songs, valid_input, guessed
    all_songs = {}
    valid_input = ['QUIT','SOLVE','ARTIST','ALBUM','A','B','C','D','E','F','G','H','I','J','K','L','M','N',
                   'O','P','Q','R','S','T','U','V','W','X','Y','Z']
    guessed = []
    
    # use SongAdder function below with as many artists as desired
    #SongAdder("The Beatles")
    #SongAdder("Queen")
    
    Game(0)


initialize()
