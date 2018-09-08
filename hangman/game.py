from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self, letter, hit=False, miss=False):
        if hit and miss:
            raise InvalidGuessAttempt

        self.letter = letter
        self.hit = hit
        self.miss = miss
        if not hit:
            self.miss = True

    def is_hit(self):
        if self.hit:
            return True
        return False

    def is_miss(self):
        if self.miss:
            return True
        return False

class GuessWord(object):

    def __init__(self, word):
        if not word:
            raise InvalidWordException
        self.answer = word
        self.masked = '*' * len(word)

    def unmask(self, letter):
        count = 0
        for answer_letter in self.answer:
            if answer_letter.lower() == letter.lower():
                self.masked = (self.masked[:count] + letter.lower() +
                               self.masked[count + 1:])
            count += 1
        return self.masked

    def perform_attempt(self, letter):
        if len(letter) != 1:
            raise InvalidGuessedLetterException

        if letter.lower() in self.answer.lower():
            attempt = GuessAttempt(letter, hit=True)
            self.masked = self.unmask(letter)
        else:
            attempt = GuessAttempt(letter, miss=True)
        return attempt


class HangmanGame(object):

    WORD_LIST = ['rmotr', 'python', 'awesome']

    def __init__(self, word_list=None,
                 number_of_guesses=5):
        if word_list is None:
            word_list = self.WORD_LIST

        self.remaining_misses = number_of_guesses
        self.word = GuessWord(self.select_random_word(word_list))
        self.previous_guesses = []

    def guess(self, letter):
        if self.is_finished():
            raise GameFinishedException

        self.previous_guesses.append(letter.lower())
        attempt = self.word.perform_attempt(letter)

        if attempt.is_miss():
            self.remaining_misses -= 1
        if self.is_won():
            raise GameWonException
        if self.is_lost():
            raise GameLostException

        return attempt

    def is_finished(self):
        if self.is_won() or self.is_lost():
            return True
        return False

    def is_won(self):
        if self.word.answer == self.word.masked:
            return True
        return False

    def is_lost(self):
        if self.remaining_misses < 1:
            return True
        return False

    @classmethod
    def select_random_word(cls, word_list):
        if not word_list:
            raise InvalidListOfWordsException
        return random.choice(word_list)
