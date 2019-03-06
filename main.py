import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton , QMainWindow , QFileDialog , QLabel ,QGridLayout , QSpinBox
from PyQt5.QtGui import QPixmap ,QColor


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(500,385)
        self.imported_image = QLabel(self)
        self.modified_image = QLabel(self)
        self.search_image_button = QPushButton("Selecione a Imagem",self)
        self.search_image_button.move(20,340)
        self.search_image_button.setMinimumSize(160,30)
        self.bright_button = QPushButton("ajustar brilho",self)
        self.bright_button.setVisible(False)
        self.bright_button.move(200,340)
        self.spinner_brightness = QSpinBox(self)
        self.spinner_brightness.setMaximum(255)
        self.spinner_brightness.setMinimum(-255)
        self.spinner_brightness.setMinimumSize(60,30)
        self.spinner_brightness.move(370, 340)
        self.spinner_brightness.setVisible(False)
        self.spinner_label = QLabel("brilho: ",self)
        self.spinner_label.move(320,340)
        self.spinner_label.setMinimumSize(60 ,30)
        self.spinner_label.setVisible(False)
        self.histogram_generator = QPushButton("Gerar histograma de escala de cinza",self)
        self.histogram_generator.setVisible(False)
        self.histogram_generator.setMinimumSize(280 ,30)
        self.histogram_generator.move(110, 385)

        self.setWindowTitle("GreyScale Project")
        self.search_image_button.clicked.connect(self.search_image_clicked)
        self.bright_button.clicked.connect(self.bright_button_clicked)
        self.show()

    def search_image_clicked(self):
        file_name,_ = QFileDialog.getOpenFileName(self, 'Open file', './', 'Image Files(*.png *.jpg *.jpeg *.bmp )' )
        if file_name:
            image = QPixmap(file_name)
            image = image.scaledToHeight(300)
            self.imported_image.setPixmap(image)
            self.imported_image.show()
            self.imported_image.resize(image.width(), image.height())
            self.imported_image.move(20,20)
            if not self.bright_button.isVisible():
                self.bright_button.setVisible(True)
            self.setMinimumSize(image.width() * 2 + 60 , 425)
            self.setMaximumSize(image.width() * 2 + 60 , 425)
            self.modified_image.setPixmap(image)
            self.modified_image.resize(image.width(), image.height())
            self.modified_image.move(image.width()+40,20)
            self.modified_image.show()
            self.spinner_brightness.show()
            self.spinner_label.show()
            self.histogram_generator.show()

    def bright_button_clicked(self):
        constant = self.spinner_brightness.value()
        qimage = self.imported_image.pixmap().toImage()
        for x in range(0 , qimage.width()):
            for y in  range(0 , qimage.height()):
                current_pixel =  qimage.pixel(x,y)
                cur_color = QColor(current_pixel)
                red = self.adjust_to_limit(cur_color.red() + constant)
                green = self.adjust_to_limit(cur_color.green() + constant)
                blue = self.adjust_to_limit(cur_color.blue() + constant)
                value = QColor(red-constant,green-constant,blue-constant)
                qimage.setPixel(x,y,value.rgb())
        new_pixmap = QPixmap.fromImage(qimage)
        self.modified_image.setPixmap(new_pixmap)
    
    def adjust_to_limit(self, value ):
        if value >= 255:
            return 255
        elif value < 0:
            return 0
        else:
            return value


if __name__ == "__main__":
    application = QApplication([])
    main = Main()
    main.show()
    sys.exit(application.exec_())