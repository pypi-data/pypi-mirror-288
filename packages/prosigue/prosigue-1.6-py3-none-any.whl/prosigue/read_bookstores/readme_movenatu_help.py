
print("\
\n\
libreria de apoyo a la libreria prosigue, \n\
dentro del mismo paquete. \n\
\n\
Esta libreria se encuentra bajo la misma \n\
licencia de prosigue. \n\
\n\
\n\
Esta libreria debe ejecutarse bajo el comando: \n\
if __name__ == '__main__': \n\
ya que si no se hace asi, no funcionará, \n\
al igual que la libreria prosigue. \n\
\n\
Ademas, debera tener preparada dos clases mas... \n\
u objetos. \n\
\n\
1.una para contener el codigo que quiere ejecutar \n\
en la segunda tarea (su codigo). \n\
Y... con el metodo 'empieza'... \n\
Este metodo aqui, en esta libreria solo debera \n\
recibir un argumento. \n\
\n\
2.La otra clase debera contener dos instancias \n\
-una 'self.dato_1' que sera la entrada. \n\
La entrada de la primera clase, por cierto. \n\
(el argumento que se le pasa) \n\
-la otra instancia es 'self.dato_2' que sera \n\
la salida. \n\
\n\
Esta salida regresara (0) si no logra hacerse \n\
la segunda tarea. Pero si se realiza, \n\
esta salida podra usarse para modificar algo \n\
en epecifico, usted desida que. \n\
\n\
veamos un ejemplo de como debe implementarse \n\
todo esto: \n\
\n\
from prosigue.movenatu import Metafisica \n\
\n\
if __name__ == '__main__': \n\
\n\
    particula= Metafisica() \n\
    saliendo= particula.grain_move(info, 3, imag) \n\
\n\
    if saliendo == 0: \n\
        pass \n\
    else: \n\
        print('configuro una base_datos, por ejemplo') \n\
\n\
    print() \n\
\n\
\n\
En este ejemplo 'info' es el objeto de la clase que \n\
contiene la entrada y la salida. \n\
e 'imag' es el objeto de la clase que contiene el \n\
metodo empieza y el codigo de la segunda tarea. \n\
El numero (3) es por supuesto el tiempo que se le da \n\
a la libreria para determinar si se puede \n\
ejecutar el script o codigo alojado en 'imag' o no. \n\
\n\
por ultimo: \n\
Si usted ingresa (resti, True) en el constructor \n\
de la clase Metafisica... \n\
\n\
esto:		particula= Metafisica(resti, True) \n\
en vez de:	particula= Metafisica() \n\
\n\
Aqui 'resti' es el objeto de Restituye() \n\
la clase que tambien se puede emplear \n\
en la libreria prosigue. \n\
\n\
usted podra revertir lo poco que se halla podido hacer \n\
segun lo eficiente que pueda ser su codigo de corregir \n\
\n\
\n\
#Ejemplo de Restituye() creado para movenatu: \n\
\n\
import time \n\
\n\
class Mi_alternativa_a_Restituye: \n\
\n\
    def empieza(self, entrada): \n\
\n\
        self.ent= entrada \n\
        self.mas_cosas() \n\
\n\
        time.sleep(3) \n\
\n\
    def mas_cosas(self): \n\
        print('return_ya') \n\
\n\
")

