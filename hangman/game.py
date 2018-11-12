from .exceptions import *
from random import choice


class GuessAttempt(object):
    def __init__(self,letter, hit=False, miss=False):
        if hit and miss:
            raise InvalidGuessAttempt()
        self.letter = letter
        self.hit = hit
        self.miss = miss
        
    def is_hit(self):
        return bool(self.hit)
        
    def is_miss(self):
        return bool(self.miss)


class GuessWord(object):
    def __init__(self, word):
        if not word:
            raise InvalidWordException
        self.answer = word.lower()
        self.masked = '*' * len(word)
        
    def perform_attempt(self, letter):
        if len(letter) > 1:
            raise InvalidGuessedLetterException
            
        if letter.lower() in self.answer:
            new_word = ''
            for answer_char, masked_char in zip(self.answer, self.masked):
                if answer_char == letter.lower():
                    new_word += answer_char
                else:
                    new_word += masked_char
            self.masked = new_word
            return GuessAttempt(letter.lower(),hit = True)
        return GuessAttempt (letter.lower(),miss = True)


class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, list_of_words=WORD_LIST, number_of_guesses=5):
        self.word = GuessWord(self.select_random_word(list_of_words))
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        
    def guess(self, letter):
        if self.is_finished() == True:
            raise GameFinishedException()
        attempt = self.word.perform_attempt(letter)
        self.previous_guesses.append(attempt.letter)
        if attempt.is_miss():
            self.remaining_misses -= 1
        if self.is_won() == True:
            raise GameWonException()
        if self.is_lost() == True:
            raise GameLostException()
        return attempt
        
    def is_won(self):
        if self.word.answer == self.word.masked:
            return True
        return False
        
    def is_lost(self):
        if self.remaining_misses <= 0:
            return True
        return False
    
    def is_finished(self):
        if self.is_lost() == True or self.is_won() == True:
            return True
        return False
    
    @classmethod
    def select_random_word(cls, list_of_words):
        if not list_of_words:
            raise InvalidListOfWordsException()
        return choice(list_of_words)