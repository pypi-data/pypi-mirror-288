
""" Modulo de libreria Prosigue """


if True:

    #####################################################
    #                                                   #
    # Cuando "se vence el proceso secundario" no se     #
    # puede garantizar la fidelidad de los cambios      #
    # realizados y es posible restablecerlos con        #
    # el metodo 'imagen_reset'. Ejemplo:                #
    #                                                   #
    #        if prosigue_1.answer == 1:                 #
    #                                                   #
    #            print(configura.deteccion_01)          #
    #            print(config_01_back.deteccion_01)     #
    #                                                   #
    #        else:                                      #
    #            print("Se ha vencido el proceso")      #
    #            a_restab= Restituye()                  #
    #            prosigue_1.imagen_reset(a_restab)      #
    #                                                   #
    # configura.deteccion_01 es: o son, los valores del #
    # objeto mostrado a prosigue.                       #
    #                                                   #
    # config_01_back.deteccion_01 es una imagen del     #
    # objeto con los datos modificados a conveniencia   #
    # y es el retorno que entrega el metodo.close()     #
    #                                                   #
    # El (else) se debe a que algunas operaciones son...#
    # manejo de archivos u/o de otro tipo de operacion  #
    # externas.                                         #
    #                                                   #
    #####################################################

    pass

"==================================================="

from multiprocessing import Process, Queue, Value
from prosigue.do_hasta_time import Hasta_time
import os


class De_traspaso:
    
    def __init__(self):
        
        self.trasp_1= 0
        self.trasp_2= 2
            
"==================================================="

# Clases que realizan el proceso Prosigue

class Prosigue:
    
    def __init__(self, lo_previsto= None):

        self.acces= True
        
        self.sentencia= None
        self.answer= None
        
        self.previo_mega= lo_previsto
        self.time_2= None
        
        self.metaversion= True
        
        self.dato= De_traspaso()        
        self.balum= Hasta_time()
    
    def tiempo(self, time):

        self.time_2= time

    def confirm(self, el_code, salida_externa= False):
        
        self.sentencia= el_code
        
        if salida_externa == True:
            self.metaversion= False

        if salida_externa == False:
            self.iterador= Queue()
        
    def accion(self, iter):
        
        if self.metaversion == False:
            self.sentencia.empieza(self.previo_mega)
        else:
            self.sentencia.empieza(self.previo_mega, iter)
                    
    "......................................"
    
    def primero(self, puente, iter):

        my_id= os.getpid()
        puente.trasp_1.value= my_id
        
        self.accion(iter)
        self.procesando(puente)
    
    def procesando(self, puen):
                
        if self.acces is True: # Se esta confirmando...
            puen.trasp_2.value= 1

    "......................................"

    def cloud_rain(self):
        
        self.iterador= Queue()
        
        return self.iterador

    def close(self, finish= False):
        
        self.finish= finish # se termina cuando el script finaliza
        
        self.dato.trasp_1= Value("i", 0)
        self.dato.trasp_2= Value("i", 0)

        proceso_1= Process(target= self.primero, args= (self.dato, self.iterador,))
        proceso_1.start()

        confir_time= False
        while confir_time == False:
            
            if self.dato.trasp_2.value == 1: # puede ser inocuo
                if self.finish == True:
                    break   # porque ya se cerro se sale

            ya_esta= self.balum.acaso(self.time_2)
            
            if ya_esta == True:
                
                os.system("taskkill /PID {} /F".format(self.dato.trasp_1.value))
                self.acces= False
                confir_time= True
        
        "......................................"

        self.answer= self.dato.trasp_2.value
        
        my_data= None
        my_data= self.iterador.get()
        return my_data
    
    "......................................"

    def imagen_reset(self, proceso):
        
        proceso.termina(False)

