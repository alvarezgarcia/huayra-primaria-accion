import argparse
import cv2


def guardarCuadro(nombre, cuadro):
    print "guardarCuadro con nombre %s" % nombre
    cv2.imwrite(nombre, cuadro)
    cv2.imshow("Ultimo cuadro guardado", cuadro)
    return

def grisarCuadro(cuadro):
    print "grisarCuadro"
    return cv2.cvtColor(cuadro, cv2.COLOR_BGR2GRAY)

def main():

    filtroActivo = None
    cuadroFinal = None

    atajos = {
        'c': guardarCuadro,
        'g': grisarCuadro
    }

    opciones = {
        "prefijoArchivo": "captura-",
        "directorio": "/tmp/",
        "extension": "png"
    }

    iteradorCaptura = 0

    camera = cv2.VideoCapture(0)

    while True:
        (grabbed, frame) = camera.read()

        if not grabbed:
            break

        if filtroActivo:
            cuadroFinal = atajos[filtroActivo](frame)
        else:
            cuadroFinal = frame

        cv2.imshow("Huayra Primaria Accion", cuadroFinal)
        teclaRaw = cv2.waitKey(10)

        if teclaRaw == -1:
            continue

        tecla = chr(teclaRaw & 255)

        try:
            if tecla is 'c':
                nombreFinal = opciones["directorio"] + "/" + opciones['prefijoArchivo'] + str(iteradorCaptura) + "." + opciones['extension']
                atajos[tecla](nombreFinal, cuadroFinal)
                iteradorCaptura += 1
            elif tecla is 'g':
                filtroActivo = tecla
            elif tecla is 'l':
                print "Limpio filtros"
                filtroActivo = None
            else:
                atajos[tecla](frame)

        except KeyError:
            continue

if __name__ == '__main__':
    main()
