import cv2
import numpy as np
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys

class Funciones():
    def __init__(self):
        self.funciones = {
           'g': self.grisarCuadro,
           'x': self.comicCuadro
        }

    def guardarCuadro(self, cuadro):
        canales = len(cuadro.shape)

        if canales == 3:
            cv2.cvtColor(cuadro, cv2.COLOR_RGB2BGR, cuadro)

        cv2.imwrite('/tmp/nombre.png', cuadro)
        cv2.imshow("Ultimo cuadro guardado", cuadro)
        return

    def transformarCuadro(self, filtro, cuadro):
        #print "El filtro activo es " + filtro
        return self.funciones[filtro](cuadro)

    def grisarCuadro(self, cuadro):
        return cv2.cvtColor(cuadro, cv2.COLOR_BGR2GRAY)

    def comicCuadro(self, cuadro):
        print "A este cuadro hay que hacerlo comic"

        sigma = 0.33


        gray = cv2.cvtColor(cuadro, cv2.COLOR_BGRA2GRAY)
        edges = cv2.blur(gray, (3, 3)) # this blur gets rid of some noise

        v = np.median(edges)
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))

        edges = cv2.Canny(edges, lower, upper)
        kernel = np.ones((3,3), dtype=np.float) / 12.0
        edges = cv2.filter2D(edges, 0, kernel)
        edges = cv2.threshold(edges, 50, 255, 0)[1]
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        shifted = cv2.pyrMeanShiftFiltering(cuadro, 3, 20)

        return cv2.subtract(shifted, edges)
        

class Ventana(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        
        self.funciones = Funciones()

        self.imageLabel = QLabel()
        self.botonCapturar = QPushButton("Capturar")
        self.botonFiltros = QPushButton("Filtros")
        self.botonSalir = QPushButton("Salir")


        self.botonCapturar.setStyleSheet("font-size: 30px;background-color: #D9534F;line-height: 1;color: #FFF;text-align: center;white-space: nowrap;vertical-align: baseline;border-radius: 0.25em;")

        self.botonFiltros.setStyleSheet("font-size: 30px;background-color: #5CB85C;line-height: 1;color: #FFF;text-align: center;white-space: nowrap;vertical-align: baseline;border-radius: 0.25em;")
        self.botonSalir.setStyleSheet("font-size: 30px;background-color: #F0AD4E;line-height: 1;color: #FFF;text-align: center;white-space: nowrap;vertical-align: baseline;border-radius: 0.25em;")
        
        self.layoutGeneral = QGridLayout(self)
        self.layoutGeneral.addWidget(self.imageLabel, 0, 0, 3, 3)
        self.layoutGeneral.addWidget(self.botonCapturar, 3, 0)
        self.layoutGeneral.addWidget(self.botonFiltros, 3, 1)
        self.layoutGeneral.addWidget(self.botonSalir, 3, 2)

        self.setWindowTitle("Huayra Primaria Accion")
        self.show()

        self.camara = cv2.VideoCapture(0)

        self.filtroActivo = None

        self.frame = None
        self.frameFiltrado = None
        self.frameConvertir = None

        self.botonCapturar.clicked.connect(lambda: self.funciones.guardarCuadro(self.frame))
        self.botonFiltros.clicked.connect(self.mostrarFiltros)

        
        while True:
            (grabbed, self.frame) = self.camara.read()
            cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB, self.frame)

            if not grabbed:
                break

            if self.filtroActivo:
                self.frame = self.funciones.transformarCuadro(self.filtroActivo, self.frame)
            else:
                print "No hay filtro activo"

            canales = len(self.frame.shape)

            if canales == 3:
                formato = QImage.Format_RGB888
            else:
                formato = QImage.Format_Indexed8


            temp = QImage(self.frame.tostring(), self.frame.shape[1], self.frame.shape[0], formato)
            self.imageLabel.setPixmap(QPixmap.fromImage(temp))
            self.resize(temp.width(), temp.height())


            cv2.waitKey(100)

    def keyPressEvent(self, event):
        tecla = str(event.text())
        if tecla == 'c':
            self.funciones.guardarCuadro(self.frame)
        elif tecla == 'l':
            self.filtroActivo = None

        if tecla in self.funciones.funciones:
            self.activarFiltro(tecla)

    def mostrarFiltros(self):
        self.botonCapturar.setVisible(False)
        self.botonFiltros.setVisible(False)
        self.botonSalir.setVisible(False)


	self.botonFiltrosVolver = QPushButton("Volver")
	self.botonFiltrosReset = QPushButton("Reset")
	self.botonFiltrosGris = QPushButton("Gris")
	self.botonFiltrosComic = QPushButton("Comic")

        self.botonFiltrosVolver.setStyleSheet("font-size: 30px;background-color: #D9534F;line-height: 1;color: #FFF;text-align: center;white-space: nowrap;vertical-align: baseline;border-radius: 0.25em;")
        self.botonFiltrosReset.setStyleSheet("font-size: 30px;background-color: #337AB7;line-height: 1;color: #FFF;text-align: center;white-space: nowrap;vertical-align: baseline;border-radius: 0.25em;")
        self.botonFiltrosGris.setStyleSheet("font-size: 30px;background-color: #337AB7;line-height: 1;color: #FFF;text-align: center;white-space: nowrap;vertical-align: baseline;border-radius: 0.25em;")
        self.botonFiltrosComic.setStyleSheet("font-size: 30px;background-color: #337AB7;line-height: 1;color: #FFF;text-align: center;white-space: nowrap;vertical-align: baseline;border-radius: 0.25em;")


        self.layoutGeneral.addWidget(self.imageLabel, 0, 0, 4, 4)

        self.layoutGeneral.addWidget(self.botonFiltrosVolver, 4, 0)
        self.layoutGeneral.addWidget(self.botonFiltrosReset, 4, 1)
        self.layoutGeneral.addWidget(self.botonFiltrosGris, 4, 2)
        self.layoutGeneral.addWidget(self.botonFiltrosComic, 4, 3)

        self.botonFiltrosGris.clicked.connect(lambda: self.activarFiltro('g'))
        self.botonFiltrosReset.clicked.connect(lambda: self.activarFiltro(None))
        self.botonFiltrosComic.clicked.connect(lambda: self.activarFiltro('x'))

    def activarFiltro(self, filtro):
        self.filtroActivo = filtro
    



if __name__ == '__main__':
    app = QApplication(sys.argv)
    v = Ventana()
    v.show()
    app.exec_()
