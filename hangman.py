import operator
import re


class Hangman:
    def __init__(self):
        self._name_of_the_game = 'HANGMAN - Guess the word'
        self._secret_word = 'imitation'  # 'imbosk'  # 'excuse'
        self._already_guessed_letters = []
        self._encoded_secret_word = ''.join(['_' for _ in self._secret_word])
        self._maximum_iterations = int(1.5 * self._secret_word.__len__()) + 1
        # BY DEFAULT 50% MORE CHANCES THAN LENGTH OF SECRET WORD

    def get_maximum_iterations(self):
        return self._maximum_iterations

    def is_word_guessed(self):
        if self._secret_word.upper() == self._encoded_secret_word.upper():
            return True

    @staticmethod
    def finish_the_game(result='LOSS'):
        print()
        print('Game over.', end=' ')
        if result == 'WIN':
            print('Victory!!')
        else:
            print('You\'re hanging!')

    def print_game_status(self):
        print('-----------------------------------------')
        print(self._name_of_the_game)
        print()
        if self.already_guessed_letters_to_string().__len__() > 0:
            print('Already used letters:')
        else:
            print('No used letters yet')
        print(self.already_guessed_letters_to_string().upper())
        print(self.print_encoded_word())
        print()

    def already_guessed_letters_to_string(self):
        return "".join([letter for letter in self._already_guessed_letters]) if self._already_guessed_letters.__len__() > 0 else ""

    def print_encoded_word(self):
        # print(self.encoded_secret_word)
        return "".join([letter.upper() + ' ' for letter in self._encoded_secret_word])

    @staticmethod
    def guess_the_letter():
        return str(input('Enter the letter: '))

    def append_to_already_used(self, letter):
        append_result = 0
        if letter.isalpha() and len(letter) == 1:
            if letter.upper() not in hangman.already_guessed_letters_to_string().upper():
                self._already_guessed_letters.append(letter)
                append_result = 1
            else:
                print('This letter was already used.')
        else:
            print('Only one letter please')
        return append_result

    def shoot(self, *args, **kwargs):
        hit_result = 0
        # input("shoot")
        if 'letter' in kwargs:
            for i in range(self._secret_word.__len__()):
                if kwargs['letter'].upper() == self._secret_word[i].upper():
                    hit_result = 1
            if hit_result == 1:
                print('The right shot!')
            else:
                print('You miss!')
        if 'word' in kwargs:
            if kwargs['word'] == self._secret_word:
                hit_result = 1
        return hit_result

    def decode_secret_word(self, *args, **kwargs):
        if 'letter' in kwargs:
            for i in range(self._secret_word.__len__()):
                if letter.upper() == self._secret_word[i].upper():
                    self._encoded_secret_word = self._encoded_secret_word[:i] + kwargs['letter'] + self._encoded_secret_word[i + 1:]
                    # print(f'Encoded new: {self._encoded_secret_word}')
        if 'word' in kwargs:
            self._encoded_secret_word = word

    def get_secret_word_length(self):
        return len(self._encoded_secret_word)

    def get_encoded_secret_word(self):
        return self._encoded_secret_word


class BotPlayer:
    def __init__(self, length):
        self._valid_words = self.load_words()
        self._secret_word_length = length
        self._words_with_correct_length = self.get_words_with_correct_length_from_file(length)
        self._letters_to_guess = []
        self._guessed_letters = []
        self._missed_letters = []
        self._deleted_letters = []
        self._guess_whole_word = False

    @property
    def words(self):
        return self._words_with_correct_length

    @property
    def guessed(self):
        return self._guessed_letters

    @property
    def missed(self):
        return self._missed_letters

    @property
    def deleted(self):
        return self._deleted_letters

    @property
    def ltg(self):
        return self._letters_to_guess

    @property
    def answer(self):
        return self._guess_whole_word

    @staticmethod
    def load_words():
        with open('words_alpha.txt') as word_file:
            valid_words = set(word_file.read().split())

        return valid_words

    # zapisz do pliku slowa o dlugosci X
    def get_words_with_correct_length_from_file(self, length):
        words_with_correct_length = [word for word in self._valid_words if len(word) == length]
        return words_with_correct_length

    def set_letters_to_guess(self, encoded_word=''):
        if re.search('[a-zA-Z]', encoded_word):
            # print('Inside pattern get')
            self._words_with_correct_length = self.get_word_from_pattern(encoded_word)
            if len(self._words_with_correct_length) == 1:
                self.set_guess_whole_word()
                return 0
        stream_of_words = ''
        if self._missed_letters:
            for word in self._words_with_correct_length:
                # print(f'word: {word}, {self._missed_letters[-1]}')
                if self._missed_letters[-1] in word:
                    self._words_with_correct_length.remove(word)
                    # print('removed')
                else:
                    stream_of_words += word
            self._deleted_letters.append(self._missed_letters[-1])
        else:
            # print('Brak missed')
            for word in self._words_with_correct_length:
                stream_of_words += word
        ordered_set = sorted(set(stream_of_words))
        used_letters_counter = dict.fromkeys(ordered_set, 0)
        for letter in stream_of_words:
            used_letters_counter[letter] += 1
        ordered_used_letters_in_tuple = sorted(used_letters_counter.items(), key=operator.itemgetter(1), reverse=True)
        self._letters_to_guess = [''.join(letter[0]) for letter in ordered_used_letters_in_tuple]
        for letter in self._guessed_letters:
            if letter in self._letters_to_guess:
                self._letters_to_guess.remove(letter)

    def get_word_from_pattern(self, encoded_word):
        regular_expression = ''
        regular_expression += '^'
        for letter in encoded_word:
            if letter == '_':
                regular_expression += '.'
            elif letter:
                regular_expression += '[' + letter.lower() + ']'
        regular_expression += '$'
        # print(regular_expression)
        pattern_matched = []
        for word in self._words_with_correct_length:
            if re.match(r'{}'.format(regular_expression), word):
                pattern_matched.append(word)
        # print(pattern_matched)
        # input("...")

        return pattern_matched

    def guess_the_letter(self):
        letter = self._letters_to_guess[0]
        return letter

    def guess_the_word(self):
        word = self._words_with_correct_length[0]
        return word

    def append_missed(self, letter):
        self._missed_letters.append(letter)

    def append_guessed(self, letter):
        self._guessed_letters.append(letter)

    def set_guess_whole_word(self):
        self._guess_whole_word = True


if __name__ == '__main__':
    hangman = Hangman()
    secret_word_length = hangman.get_secret_word_length()
    iteration = 0
    max_iterations = hangman.get_maximum_iterations()
    original_iteration = max_iterations
    bot_player = BotPlayer(secret_word_length)
    bot_player.set_letters_to_guess()

    while iteration <= max_iterations:
        remained_iterations = max_iterations - iteration
        if hangman.is_word_guessed():
            print(hangman.print_encoded_word())
            hangman.finish_the_game('WIN')
            print(f'You\'ve finished after {original_iteration-max_iterations+iteration} tries')
            break
        elif remained_iterations is 0:
            hangman.finish_the_game()
            break
        else:
            hangman.print_game_status()
            print(f'{remained_iterations} iteration has remained')
            if bot_player.answer:
                word = bot_player.guess_the_word()
                print(f'Guessed word: {word}')
                if hangman.shoot(word=word):
                    hangman.decode_secret_word(word=word)
                    iteration -= 1
            else:
                letter = bot_player.guess_the_letter()
                print(f'Guessed letter: {letter}')
                # print(bot_player.words)
                # print(bot_player.guessed)
                if hangman.append_to_already_used(letter):
                    if hangman.shoot(letter=letter):
                        hangman.decode_secret_word(letter=letter)
                        bot_player.append_guessed(letter)
                        bot_player.guessed
                        iteration -= 1
                    else:
                        bot_player.append_missed(letter)
                    bot_player.missed
            bot_player.set_letters_to_guess(hangman.get_encoded_secret_word())
            # print(bot_player.ltg)
            # input("...")
        iteration += 1





