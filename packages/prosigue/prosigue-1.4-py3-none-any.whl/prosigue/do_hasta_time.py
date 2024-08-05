
""" Hasta_time es una libreria creada para comprobar hechos durante un
    lapsus de tiempo """


"======================================================"

import time

class Lujan:
    
    def __init__(self):
        
        self.inicio= False
        self.star= None
    
"======================================================"

class Hasta_time:
    
    def __init__(self):
        
        self.sinta= Lujan()

    def acaso(self, largo):

        if self.sinta.inicio == True:

            paso= time.perf_counter()
            
            timer= paso - self.sinta.star
            
            if timer >= largo:
                
                self.sinta.inicio= False
                self.sinta.star= None

                return True
            
            else:
                return False
            
        else:
            
            self.sinta.star= time.perf_counter()
            self.sinta.inicio= True
            
            return False

    def reini(self):
        
        self.sinta.inicio= False
        self.sinta.star= None
        
