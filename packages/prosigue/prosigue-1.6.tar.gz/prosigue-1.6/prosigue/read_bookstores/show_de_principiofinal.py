
print("\
\n\
'' Proceso que se realiza al entrar \n\
a un comando prosigue ''' \n\
\n\
\n\
'=====================================' \n\
\n\
import time \n\
\n\
'=====================================' \n\
\n\
class Operador: \n\
\n\
    def empieza(self, configura, iter): \n\
\n\
        configura[1]= 'mi_carro'  # o, se puede modificar una instancia \n\
        iter.put(configura) \n\
\n\
        time.sleep(8) \n\
\n\
\n\
class Restituye: \n\
\n\
    def termina(self, caso): \n\
\n\
        if caso == False: \n\
\n\
            print() \n\
            print('Usted estaria \\n\
            restableciendo los datos') \n\
\n\
            print('sirvase emplear \\n\
            una clase personal \\n\
            en reemplazo de Restituye.') \n\
\n\
\n\
")

