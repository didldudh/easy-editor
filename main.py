import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PIL import Image
from PIL.ImageFilter import SHARPEN

app = QApplication([])
win = QWidget()
win.resize(900, 500)
win.move(0, 0)
win.setWindowTitle('Easy Editor')
win.setStyleSheet('color: lime;'
                  'background-color: black;')
lb_image = QLabel("🖼")
lb_image.setFont(QFont('Mistral', 300))
lb_image.setStyleSheet("color: #00ff9d;"
                       "border: 5px solid lime;"
                       "background-color: #515151")
btn_dir = QPushButton("📂")
btn_dir.setFont(QFont('Segou UI', 30))
btn_dir.setStyleSheet('background-color: lime;'
                      'color: black')
lw_files = QListWidget()
lw_files.setFont(QFont('Segou UI', 10))
lw_files.setStyleSheet("color: lime;"
                       "border: 3px solid lime;"
                       "background-color: #515151")
btn_left = QPushButton("↺")
btn_left.setFont(QFont('Segou UI', 20))
btn_left.setStyleSheet('background-color: lime;'
                       'color: black')
btn_right = QPushButton("↻")
btn_right.setFont(QFont('Segou UI', 20))
btn_right.setStyleSheet('background-color: lime;'
                        'color: black')
btn_flip = QPushButton("↹")
btn_flip.setFont(QFont('Segou UI', 20))
btn_flip.setStyleSheet('background-color: lime;'
                       'color: black')
btn_sharp = QPushButton("▦")
btn_sharp.setFont(QFont('Segou UI', 20))
btn_sharp.setStyleSheet('background-color: lime;'
                        'color: black')
btn_bw = QPushButton("⬛️⬜️")
btn_bw.setFont(QFont('Segou UI', 19))
btn_bw.setStyleSheet('background-color: lime;'
                     'color: black')


row = QHBoxLayout()  # Основная строка
col1 = QVBoxLayout()  # делится на два столбца
col2 = QVBoxLayout()
col1.addWidget(btn_dir)  # в первом - кнопка выбора директории
col1.addWidget(lw_files)  # и список файлов
col2.addWidget(lb_image, 95)  # вo втором - картинка
row_tools = QHBoxLayout()
# и строка кнопок
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools)

row.addLayout(col1, 20)
row.addLayout(col2, 80)
win.setLayout(row)

win.show()

workdir = ''


def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result


def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()


def showFilenamesList():
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)

    lw_files.clear()
    for filename in filenames:
        lw_files.addItem(filename)


btn_dir.clicked.connect(showFilenamesList)


class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = 'Modified/'

    def loadimage(self, dir, filename):
        self.dir = dir  # C:\Users\bilol\Desktop\start2\Part 3\Part 3\my vacation
        self.filename = filename  # /field.png
        image_path = os.path.join(dir, filename)  # C:\Users\bilol\Desktop\start2\Part 3\Part 3\my vacation\field.png
        self.image = Image.open(image_path)

    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        # C:\Users\bilol\Desktop\start2\Part 3\Part 3\my vacation\Modified\field.png
        self.showimage(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showimage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showimage(image_path)

    def do_flip(self):
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
            self.saveImage()
            image_path = os.path.join(self.dir, self.save_dir, self.filename)
            self.showimage(image_path)

    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showimage(image_path)

    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        # C:\Users\bilol\Desktop\start2\Part 3\Part 3\my vacation\Modified
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.mkdir((path))
        image_path = os.path.join(path, self.filename)
        # C:\Users\bilol\Desktop\start2\Part 3\Part 3\my vacation\Modified\field.png
        self.image.save(image_path)

    def showimage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()


def showChosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        workimage.loadimage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showimage(image_path)


workimage = ImageProcessor()
lw_files.currentRowChanged.connect(showChosenImage)
btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_sharpen)
btn_flip.clicked.connect(workimage.do_flip)

app.exec()