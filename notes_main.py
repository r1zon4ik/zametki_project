from PyQt5.QtCore import Qt
import json
from PyQt5.QtWidgets import (QApplication,QWidget,QPushButton,QLabel,QListWidget,
    QLineEdit,QTextEdit,QHBoxLayout,QVBoxLayout,QInputDialog,QInputDialog)
#окно приложения
app = QApplication([])
notes_win = QWidget()


notes = {
    'Заметка1': 
        {'текст':'Очень важный текст заметки',
        'теги':['черновик','мысли']},
    'Заметка2':
        {'текст':'первая заметка',
        'теги':['первая','один']},
    'Заметка3':
        {'текст':'вторая заметка',
        'теги':['вторая','два']}
}

#перезаполнение списков
#with open('notes_data.json','r') as file:
#    notes = json.load(file)


#виджеты
note_info_widget = QTextEdit()
note_list_label_widget = QLabel()
note_list_widget = QListWidget()
create_note_widget = QPushButton()
delete_note_widget = QPushButton()
save_note_widget = QPushButton()

tag_list_widget = QListWidget()
tag_list_label_widget = QLabel()
tag_input_widget = QLineEdit()
add_tag_widget = QPushButton()
delete_tag_widget = QPushButton()
search_tag_widget = QPushButton()


for key in notes:
    note_list_widget.addItem(key)
#лайауты
main_layout = QHBoxLayout()
settings_layout = QVBoxLayout()
settings_note = QVBoxLayout()
settings_note_buttons = QHBoxLayout()

settings_tag = QVBoxLayout()
settings_tag_buttons = QHBoxLayout()

#прикрепление лайаутов
main_layout.addWidget(note_info_widget)

settings_note_buttons.addWidget(create_note_widget)
settings_note_buttons.addWidget(delete_note_widget)
settings_note.addWidget(note_list_label_widget)
settings_note.addWidget(note_list_widget)
settings_note.addLayout(settings_note_buttons)
settings_note.addWidget(save_note_widget)

settings_layout.addLayout(settings_note)
main_layout.addLayout(settings_layout)
notes_win.setLayout(main_layout)

settings_tag_buttons.addWidget(add_tag_widget)
settings_tag_buttons.addWidget(delete_tag_widget)
settings_tag.addWidget(tag_list_label_widget)
settings_tag.addWidget(tag_list_widget)
settings_tag.addWidget(tag_input_widget)
settings_tag.addLayout(settings_tag_buttons)
settings_tag.addWidget(search_tag_widget)

settings_layout.addLayout(settings_tag)
main_layout.addLayout(settings_layout)
notes_win.setLayout(main_layout)

#установка надписей
note_list_label_widget.setText('Список заметок')
create_note_widget.setText('Создать заметку')
delete_note_widget.setText('Удалить заметку')
save_note_widget.setText('Сохранить заметку')

tag_list_label_widget.setText('Список тегов')
delete_tag_widget.setText('Открепить от заметки')
add_tag_widget.setText('Добавить к заметке')
search_tag_widget.setText('Искать заметки по тегу')
tag_input_widget.setPlaceholderText('Введите тег...')


#функции 
def show_results():
    note_text = note_list_widget.selectedItems()[0].text()
    note_info_widget.clear()
    note_info_widget.setText(notes[note_text]['текст'])
    tags = notes[note_text]['теги']
    tag_list_widget.clear()
    for tag in tags:
        tag_list_widget.addItem(tag)
  
def del_note():
    try:
        note_text = note_list_widget.selectedItems()[0].text()
        del notes[note_text]
    except:
        print('Заметка не выбрана!')
    note_list_widget.clear()
    tag_list_widget.clear()
    note_info_widget.clear()
    for key in notes:
        note_list_widget.addItem(key)

def save_note():
    note_text = note_list_widget.selectedItems()[0].text()
    notes[note_text]['текст'] = note_info_widget.toPlainText()

def create_note():
    new_note_text,btn_ok_is_clicked = QInputDialog.getText(notes_win,'Новая заметка','Название заметки:')
    if btn_ok_is_clicked and new_note_text != '':
        notes[new_note_text] = {'текст':'','теги':[]}
        note_list_widget.clear()
        tag_list_widget.clear()
        note_info_widget.clear()
        for key in notes:
            note_list_widget.addItem(key)

def add_tag():
    tags = tag_input_widget.text()
    if tag_input_widget.text() != '':
        note_text = note_list_widget.selectedItems()[0].text()
        notes[note_text]['теги'].append(tags)
        tags = notes[note_text]['теги']
        tag_list_widget.clear()
        tag_input_widget.clear()
        for tag in tags:
            tag_list_widget.addItem(tag)

def del_tag():
    tag_text = tag_list_widget.selectedItems()[0].text()
    note_text = note_list_widget.selectedItems()[0].text()
    notes[note_text]['теги'].remove(tag_text)
    tag_list_widget.clear()
    tags = notes[note_text]['теги']                                                                                                                           
    for tag in tags:
        tag_list_widget.addItem(tag)

def search_tag():
    tag = tag_input_widget.text()
    note_list_widget.clear()
    tag_list_widget.clear()
    note_info_widget.clear()
    if tag != '':
        for k,v in notes.items():
            if tag in v['теги']:
                note_list_widget.addItem(k)
    else:
        for key in notes:
            note_list_widget.addItem(key)


note_list_widget.clicked.connect(show_results)
delete_note_widget.clicked.connect(del_note)
save_note_widget.clicked.connect(save_note)
create_note_widget.clicked.connect(create_note)
delete_tag_widget.clicked.connect(del_tag)
add_tag_widget.clicked.connect(add_tag)
search_tag_widget.clicked.connect(search_tag)

notes_win.show()
app.exec()

with open('notes_data.json','w') as file:
    json.dump(notes, file)