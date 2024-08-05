
""" Libreria movimiento del paquete Prosigue
    realiza acciones secundarias bajo presion del tiempo """


"==========================================="

from prosigue.command import Prosigue

"==========================================="

class Metafisica:
    
    def __init__(self, obj_rest= None, reset= False):
        
        self.reset= reset
        self.obj_rest= obj_rest

    def grain_move(self, valor, time, mi_code):

        prosigue_1= Prosigue(valor.dato_1)

        my_end= prosigue_1.cloud_rain()
        my_end.put(valor.dato_2)
        
        prosigue_1.confirm(mi_code, True)
        
        prosigue_1.tiempo(time)
        reaccion= prosigue_1.close()
        
        '.................................'

        if prosigue_1.answer == 1:
            return reaccion

        else:
            
            if self.reset == True:
                
                prosigue_1.imagen_reset(self.obj_rest)
                return 0
            
            else:
                return 0

