# -*- coding: utf-8 -*-
import sys
import os
import time
import trie
import string
import nltk
from operator import itemgetter
from nltk.tokenize import TweetTokenizer
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMenu, QVBoxLayout,
    QSizePolicy, QMessageBox, QPushButton, QWidget, QSlider, QLabel,
    QGridLayout, QGroupBox, QLineEdit, QCheckBox, QRadioButton, QListWidget,
                             QListWidgetItem, QComboBox, QLineEdit,
                             QPlainTextEdit, QProgressBar, QSplashScreen)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, Qt, QRectF, QThread, pyqtSignal

class Window(QWidget):

    def __init__(self, parent = None):
        super(Window, self).__init__(parent = parent)
        self.left = 10
        self.top = 10
        self.title = 'Spell Checking System'
        self.width = 720
        self.height = 480
        self.initUI()
        self.cnt = 0

    def initUI(self):
        print('Init UI')
        grid = QGridLayout()

        self.textbox = QPlainTextEdit(self)
        self.textbox.resize(640, 480)
        grid.addWidget(self.textbox, 0, 0, 6, 3)

        self.button_check = QPushButton('Check!', self)
        self.button_check.clicked.connect(self.button_check_event)
        self.button_check.setEnabled(True)
        self.button_check.setFixedSize(100, 40)
        grid.addWidget(self.button_check, 0, 4)

        self.button_clear = QPushButton('Clear Input', self)
        self.button_clear.clicked.connect(self.button_clear_event)
        self.button_clear.setEnabled(True)
        self.button_clear.setFixedSize(100, 40)
        grid.addWidget(self.button_clear, 0, 5)

        self.checkbox = QCheckBox('Auto correction', self)
        self.checkbox.setChecked(True)
        grid.addWidget(self.checkbox, 1, 4, 1, 2)

        self.words_label = QLabel('Words that have suggestion(s):')
        grid.addWidget(self.words_label, 2, 4, 1, 2)

        self.words_list = QListWidget()
        self.words_list.setFixedSize(210, 240)
        self.words_list.itemActivated.connect(self.word_list_item_event)
        grid.addWidget(self.words_list, 3, 4, 1, 2)

        self.suggestions_label = QLabel('Suggestion(s):')
        grid.addWidget(self.suggestions_label, 4, 4, 1, 2)

        self.suggestions_list = QListWidget()
        self.suggestions_list.setFixedSize(210, 180)
        self.suggestions_list.itemActivated.connect(self.correction_event)
        grid.addWidget(self.suggestions_list, 5, 4, 1, 2)

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setLayout(grid)
        self.show()

    def add_item_to_words_list(self, item):
        self.words_list.addItem(item)
        QApplication.processEvents()

    def button_check_event(self):
        self.words_list.clear()
        self.suggestions_list.clear()
        print('Got inputed text:')
        text = self.textbox.toPlainText()
        text = text.replace('\n', ' ').strip()
        tokenizer = TweetTokenizer()
        self.text = tokenizer.tokenize(text)
        print(self.text)
        if len(self.text) != 0:
            self.suggest_list_of_all_words = check_text(self.text)
            for i in range(len(self.text)):
                if len(self.suggest_list_of_all_words[i]) == 0:
                    continue
                print('Adding a word:' + self.text[i])
                item = QListWidgetItem(self.text[i], parent = None, type = i)
                self.words_list.addItem(item)
                if self.checkbox.isChecked() == True and self.suggest_list_of_all_words[i][0][0] != 'No suggestion':
                    self.text[i] = self.suggest_list_of_all_words[i][0][0]
                #self.words_list.addItem(self.text[i])
        if self.checkbox.isChecked() == True:
            self.textbox.setPlainText(' '.join(self.text))

    def word_list_item_event(self, item):
        self.suggestions_list.clear()
        print('Selected ' + item.text() + ', id:' + repr(item.type()))
        for suggestion in self.suggest_list_of_all_words[item.type()]:
            item = QListWidgetItem(suggestion[0], parent = None, type = item.type())
            self.suggestions_list.addItem(item)

    def correction_event(self, item):
        print('Correcting ' + repr(item.type()) + ' ' + item.text())
        self.text[item.type()] = item.text()
        self.textbox.setPlainText(' '.join(self.text))

    def button_clear_event(self):
        self.textbox.setPlainText('')
        self.words_list.clear()
        self.suggestions_list.clear()

class MyCustomWidget(QWidget):

    def __init__(self, parent=None):
        super(MyCustomWidget, self).__init__(parent)
        layout = QVBoxLayout(self)

        # Create a progress bar and a button and add them to the main layout
        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0,1)
        layout.addWidget(self.progressBar)
        button = QPushButton("Start", self)
        layout.addWidget(button)

        button.clicked.connect(self.onStart)

        self.myLongTask = TaskThread()
        self.myLongTask.taskFinished.connect(self.onFinished)

    def onStart(self):
        self.progressBar.setRange(0,0)
        self.myLongTask.start()

    def onFinished(self):
        # Stop the pulsation
        self.progressBar.setRange(0,1)
        self.close()
        print(1)
        window = Window()
        print(2)
        window.show()
        print(3)
        self.show()

class TaskThread(QThread):
    taskFinished = pyqtSignal()
    def run(self):
        time.sleep(3)
        self.taskFinished.emit()

def check_word(trie, word):
    suggest_list = []
    suggest_list_without_rank = []
    print(check_dictionary(trie, word))
    check_result, word_rank = check_dictionary(trie, word)
    if check_result == False:
        edited_word_list = word
        for i in range(3):
            if len(suggest_list) >= 8:
                break
            edited_word_list = edit_word(edited_word_list, i + 1)
            for edited_word in edited_word_list:
                if edited_word in suggest_list_without_rank:
                    continue
                if len(suggest_list) >= 8:
                    break
                check_result, word_rank = check_dictionary(trie, edited_word)
                if check_result == True:
                    suggest_list.append((edited_word, i, word_rank))
                    suggest_list_without_rank.append(edited_word)
        suggest_list = sorted(suggest_list, key=itemgetter(1, 2))
        if len(suggest_list) == 0:
            suggest_list.append(('No suggestion', 9, 99999))
    return suggest_list

def edit_word(word_or_list, edit_distance):
    if edit_distance <= 1:
        return edit_word_once(word_or_list)
    else:
        edited_list = []
        for edited_word in word_or_list:
            if len(edited_list) > 100000:
                break
            edited_list += edit_word_once(edited_word)
        return edited_list

def edit_word_once(word):
    splits = []
    delete_list = []
    traspose_list = []
    replace_list = []
    insert_list = []
    result = []
    for i in range(len(word) + 1):
        splits.append((word[0:i], word[i:]))
    for (a, b) in splits:
        if len(b) >= 1:
            delete_list.append(a + b[1:])
            for c in string.ascii_lowercase:
                replaced_word = a + c + b[1:]
                if word == replaced_word:
                    continue
                replace_list.append(replaced_word)
        if len(b) >= 2:
            second_half = b[1] + b[0] + b[2:]
            traspose_list.append(a + second_half)
        for c in string.ascii_lowercase:
            insert_list.append(a + c + b)
    result = traspose_list + delete_list + replace_list + insert_list
#    print(splits)
#    print(delete_list)
#    print(traspose_list)
#    print(replace_list)
#    print(insert_list)
#    print(result)
    return result

def check_dictionary(trie, word):
    return trie.find(word)

def load_dictionary_from_json(filepath):
    with open(filepath) as dictionary_file:
        words = set(dictionary_file.read().split())
    return words

def load_dictionary_from_txt(filepath):
    with open(filepath) as dictionary_file:
        words = dictionary_file.readlines()
    words = [word.split() for word in words]
    return words

def load_dictionary_to_trie(words, trie):
    for word, rank in words:
        trie.insert(word.strip(), rank.strip())

def check_text(text):
    global trie_basic
    global trie_235k
    suggest_list_of_all_words = []
    for i in range(len(text)):
        suggest_list_of_all_words.append([])
        if text[i] in string.punctuation:
            continue
        print('Finding suggestions with respesct to ' + text[i])
        if text[i] == 'i':
            suggest_list_of_all_words[i].append('I')
            continue
        #suggest_list_of_all_words[i] = check_word(trie_basic, text[i])
        suggest_list_of_all_words[i] = check_word(trie_235k, text[i])
    print(suggest_list_of_all_words)
    return suggest_list_of_all_words


if __name__ == '__main__':
    global trie_basic
    global trie_235k
    trie_basic = trie.Trie()
    trie_235k = trie.Trie()
    words = load_dictionary_from_txt('data/freq.txt')
    #words = load_dictionary_from_txt('data/google-10000-english-usa.txt')
    load_dictionary_to_trie(words, trie_basic)
    words = load_dictionary_from_txt('data/en1.txt')
    load_dictionary_to_trie(words, trie_235k)
    ##print(trie.find('ternary'))
    ##print(trie.find('aa'))
    ##edit_word_once('test')
    ##print(check_word(trie, 'tesa'))
    #text = input('input text:')
    ##tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    #tokenizer = TweetTokenizer()
    #s = tokenizer.tokenize(text)
    ##print(s)
    #for word in s:
    #    print(word + repr(check_word(trie, word)))
    application = QApplication(sys.argv)
    #splash_pix = QPixmap('splash_loading.png')
    #splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    #splash.setMask(splash_pix.mask())
    #splash.show()
    #application.processEvents()

    ## Simulate something that takes time
    #time.sleep(2)
    #progress_bar = MyCustomWidget()
    #progress_bar.resize(850, 480)
    #progress_bar.show()
    ex = Window()
    #ex.show()
    #splash.finish(ex)
    sys.exit(application.exec_())
