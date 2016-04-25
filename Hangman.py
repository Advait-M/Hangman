from getpass import getpass # Don't use at school
from tkinter import *
import threading

gl = 8

# this class allows tkinter to be run in a different thread from the normal program
# it also creates the hangman graphics
class App(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        s = Canvas(self.root, width = 800, height = 800, background = "white")
        s.pack()
        def draw():
            if gl == 7:
                s.create_line(600, 600, 600, 200, fill = "black", width = 4)
                s.create_line(600, 200, 400, 200, fill = "black", width = 4)
            elif gl == 6:
                s.create_oval(350, 250, 450, 350, outline = "black", width = 4)
            elif gl == 5:
                s.create_line(400, 350, 400, 500, fill = "black", width = 4)
            elif gl == 4:
                s.create_line(400, 375, 325, 450, fill = "black", width = 4)
            elif gl == 3:
                s.create_line(400, 375, 475, 450, fill = "black", width = 4)
            elif gl == 2:
                s.create_line(400, 500, 325, 600, fill = "black", width = 4)
            elif gl == 1:
                s.create_line(400, 500, 475, 600, fill = "black", width = 4)
            elif gl == 0:
                s.create_line(400, 200, 400, 250, fill = "red", width = 8)
            self.root.after(1, draw)
        self.root.after(1, draw)
        self.root.mainloop()
app = App()

# this function checks whether the word has been guessed correctly
def isWordGuessed(secretWord, lettersGuessed):
   n = 0
   for i in range (0, len(lettersGuessed)):
      if lettersGuessed[i] in secretWord:
         n += 1
   if n == len(secretWord):
      return True
   else:
      return False

# this function organizes the letters guessed into the secret word and displays them to the user with blanks for missing letters
def getGuessedWord(secretWord, lettersGuessed):
    newstr = ''
    finalstr = ''
    for i in range (0, len(lettersGuessed)):
        if lettersGuessed[i] in secretWord:
            newstr += lettersGuessed[i]
    for n in range (0, len(secretWord)):
        
        if secretWord[n] in lettersGuessed:
            finalstr += secretWord[n]
        else:
            finalstr += ' _ '
    return finalstr

# this function finds out what letters have not been guessed
def getAvailableLetters(lettersGuessed):
    left = ''
    for i in range (97, 123):
        if chr(i) not in lettersGuessed:
            left += chr(i)
    return left

# this function finds out what letters have been guessed
def getUsedLetters(lettersGuessed):
    used = ''
    for i in range (97, 123):
        if chr(i) in lettersGuessed:
            used += chr(i)
    return used

# this function takes a letter from the user that he/she has guessed and checks if it is valid (if it is valid then it is returned)
def guessedLetterInput():
    guessedLetter = (input("Please guess a valid letter: ")).lower()
    if len(guessedLetter) == 1:
        if 97 <= ord(guessedLetter) <= 122:
            return guessedLetter
        else:
            return(guessedLetterInput())
    else:
        return(guessedLetterInput())

# this function takes the secret word from the user and checks if it is valid (if it is valid then it is returned)    
def secretWordInput():
    secretWord = str((input("What word do you want your friend to guess? Please enter a valid word: ")).lower())
    if len(secretWord) == 0:
        return(secretWordInput())
    for i in range(0,len(secretWord)):
        if 97 <= ord(secretWord[i]) <= 122:
            pass
        else:
            return(secretWordInput())
    return secretWord

# this is the function that combines most of the other functions and runs the game
def hangman(secretWord):
    lettersGuessed = ''
    mistakesMade = 0
    guessesLeft = 8
    wordLetters = len(secretWord)
    guessedWord = ''
    print("Welcome to the game, Hangman!")
    print("I am thinking of a word that is " + str(wordLetters) + " letters long.")
    # this loop runs as long as the word has not been guessed and there are guesses left
    while guessedWord != secretWord and guessesLeft != 0:
        global gl
        gl = guessesLeft
        print("You have " + str(guessesLeft) + " guesses left.")
        availableLetters = getAvailableLetters(lettersGuessed)
        usedLetters = getUsedLetters(lettersGuessed)
        print("Available letters: " + availableLetters)
        print("Used letters: " + usedLetters)
        guessedLetter = guessedLetterInput()
        guessedWord = getGuessedWord(secretWord, lettersGuessed)
        # checks if letter has not been already been guessed
        if guessedLetter not in lettersGuessed:
            lettersGuessed += guessedLetter
            guessedWord2 = getGuessedWord(secretWord, lettersGuessed)
            # checks if the guessed letter is in the secret word
            if guessedWord2 !=  guessedWord:
                print("Good guess: " + guessedWord2)
                guessedWord = guessedWord2
                print("-----------")
            # else it reduces the guesses left and increases mistakes made along with printing out a message
            else:
                print("Oops! That letter is not in my word: " + guessedWord2)
                mistakesMade += 1
                guessesLeft -= 1
                print("-----------")
        # if it has been guessed already then it prints that to the user and loops baack around
        else:
            print("Oops! You've already guessed that letter: " + guessedWord)
            print("-----------")
    gl = guessesLeft
    # checks if user won
    if guessedWord == secretWord:
        print("Congratulations, you won!")
    # else the user has lost (only way to exit the while loop was to win (word is guessed) or lose (0 guesses left))
    else:
        print("Sorry, you ran out of guesses. The word was \"" + secretWord + '\".')

# getpass does not work at school
secretWord = getpass("What word do you want your friend to guess? ") #Uses getpass module to make user input invisible
print("Welcome to Hangman! This game is a 2 player game in which 1 person will choose a word that the other has to guess. There are 8 guesses available for the player.")
# takes secret word from user
#secretWord = secretWordInput()
# runs hangman function
hangman(secretWord)
input() # To stop Python console from closing if using getpass
