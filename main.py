import sys
import os
import torch, torchvision
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, \
    QPushButton, QTextEdit, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import trainpredict

class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()
        
        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Drop Image Here \n\n')
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa
            }
        ''')

    def setPixmap(self, image):
        super().setPixmap(image)
textpredict='Value'
class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(680, 400)
        self.setAcceptDrops(True)
        
        vLayout_1 = QVBoxLayout()
        self.photoViewer = ImageLabel()
        vLayout_1.addWidget(self.photoViewer)
        self.detect = QPushButton('CLassification')
        vLayout_1.addWidget(self.detect)
        self.detect.clicked.connect(self.classify)
#        self.setLayout(mainLayout)
        self.textEdit = QLabel(text=textpredict)
        self.btn_clear = QPushButton('Clear')
        vLayout_2 = QVBoxLayout()
        vLayout_2.addWidget(self.textEdit)
        vLayout_2.addWidget(self.btn_clear)
        
        mainLayout = QHBoxLayout(self)
        mainLayout.addLayout(vLayout_1, stretch=3)
        mainLayout.setSpacing(20)
        mainLayout.addLayout(vLayout_2, stretch=2)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()
            
    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()
           
    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            self.file_path = event.mimeData().urls()[0].toLocalFile()
            self.set_image(self.file_path)
            path_file=str(self.file_path)
            print('drop file:',path_file)
            event.accept()
        else:
            event.ignore()  
        
         
            
    def set_image(self, file_path):
        pixmap = QPixmap(file_path)
        pixmap= pixmap.scaledToWidth(250)
        self.photoViewer.setPixmap(pixmap)
        
    def classify(self):
        print('hello')
        
        print('classify: ',self.file_path)
        model = torch.load('data_model_47.pt')
        
        textpredict=trainpredict.predict(model, self.file_path)
        self.textEdit.setText(textpredict)
        print(textpredict)
        
app = QApplication(sys.argv)
demo = AppDemo()
demo.show()
sys.exit(app.exec_())