
print("\
\n\
LA LICENSIA ES: Mozilla Public License 2.0 (MPL 2.0) \n\
\n\
\n\
DOCUMENTACION\n\
==============================================================\n\
\n\
Español... mi lengua natal \n\
\n\
\n\
Paquete de librería distribuida para python, Versión: 1.4 \n\
Nombre: PROSIGUE \n\
\n\
dependencias de librerías incorporadas:\n\
\n\
    multiprocessing \n\
    time \n\
    os \n\
\n\
funcionalidades que puedo ver de PROSIGUE:\n\
\n\
    - Manejo de Sistema. \n\
    - Consulta a servidores externos. \n\
\n\
PROSIGUE es una librería que...\n\
\n\
    He decidido desarrollarla con el propósito de nutrir \n\
    más al mundo de la programación. \n\
    Es una librería que por supuesto \n\
    busca ser sencilla de ser empleada. \n\
    Y realiza una operación tan practica que podría desearse \n\
    en cualquier sistema informático o de computo. \n\
\n\
Forma de Ejecutar PROSIGUE:\n\
\n\
    utilice un formato similar al ejemplo siguiente: \n\
\n\
\n\
''' Muestro el funcionamiento de PROSIGUE '''\n\
\n\
\n\
'==========================================='\n\
\n\
from prosigue.command import Prosigue\n\
from prosigue.standard.principiofinal import Operador, Restituye\n\
\n\
def dato():\n\
\n\
    dicci= dict([\n\
        (1, 'camion'), (2, 'todo_terreno'), (3, 'deportivo')\n\
    ])\n\
\n\
    return dicci\n\
\n\
'==========================================='\n\
\n\
def sample():\n\
\n\
    ingreso= dato()\n\
    prosigue_1= Prosigue(ingreso)\n\
\n\
    mi_code= Operador()\n\
    prosigue_1.confirm(mi_code)\n\
\n\
    prosigue_1.tiempo(20)\n\
    reaccion= prosigue_1.close(True)\n\
\n\
    '.................................'\n\
\n\
    if prosigue_1.answer == 1:\n\
        print(reaccion)\n\
\n\
    else:\n\
        print('Se ha vencido el proceso')\n\
        a_restab= Restituye() \n\
        prosigue_1.imagen_reset(a_restab) \n\
\n\
    print()\n\
\n\
\n\
if __name__ == '__main__':\n\
    sample()\n\
\n\
\n\
\n\
    Puedes modificar el tiempo de espera en: \n\
    prosigue_1.tiempo(20) \n\
\n\
    Ademas, debes saber que este script se encuentra \n\
    usando un ejemplo de los bloques a ejecutar \n\
    (Clasicos de la libreria PROSIGUE)... \n\
    Operar: para hacer la tarea secundaria, \n\
    en: moviendo= Operador() & \n\
    Restablece: para corregir o volver a hacer una posible solicitud, \n\
    en: a_restab= Restituye() \n\
\n\
    La segunda tarea tiene un time.sleep(8) \n\
    en el objeto del ejemplo aqui, 'moviendo= Operador()' \n\
    asi que si usted da una espera menor de (5 por ejemplo) \n\
    hara que la segunda tarea se demore mas de lo esperado \n\
    por el diseñador del software, en este caso usted \n\
    y por tanto, que se venza. ejemplo simple de todo esto:\n\
\n\
    en vez de:  prosigue_1.tiempo(20) \n\
    usa:        prosigue_1.tiempo(5) \n\
\n\
    Nota: termine de leer la documentacion, ya que ademas, \n\
    debera hacer un ajuste en el metodo close de prosigue. \n\
    si es que quiere ver realmente como funciona. \n\
\n\
    Una tarea vencida por pasarse de tiempo podra \n\
    entrar a else (de utilizarse la instancia answer).\n\
\n\
    Sirvase reemplazar las dos clases 'clasicas' \n\
    de operacion para esta libreria, \n\
    a saber (Operador(), Restituye()) \n\
    por dos clases personales, donde pueda depositar el codigo \n\
    que efectue la tarea que usted desee realizar (su codigo).\n\
    recuerde que Operador o su remplazo \n\
    ejecutara una tarea (su codigo) \n\
    y Restituye o su remplazo deberia corregir o restableser \n\
    al estado primero, haya avanzado Operador lo que haya avanzado.\n\
\n\
    La clase que contendra el codigo (su codigo) para la segunda \n\
    tarea, debera tener un metodo llamado 'empieza' \n\
    dentro de este metodo coloque el codigo (su codigo). \n\
    Este metodo debera tener dos (2) atributo de entradas. \n\
    Que son: \n\
\n\
    1.El dato dado al instanciar la clase PROSIGUE,\n\
    (osea, 'dicci' en nuestro ejemplo) \n\
\n\
    2.Y el comando Queue de la libreria multiprocessing \n\
    (este lo ingresa internamente la libreria prosigue) \n\
    al correrse la libreria con el metodo.close \n\
\n\
    El metodo de entrada de Restituye se llamara 'termina'.\n\
    y este, debera tener un atributo de entrada\n\
    que debera ser de... (0) o False, principalmente. \n\
\n\
    El metodo 'empieza' debera ejecutar en su trayectoria \n\
    de ejecucion el siguiente script que será \n\
    el return del codigo de la segunda tarea: \n\
\n\
    su_nombre_argumento.put(nombre_variable_a_retornar) \n\
\n\
    Si el codigo (su codigo) no posee esta linea de comando \n\
    Se arrojara un error \n\
    por cierto, su_nombre_argumento es el segundo atributo \n\
    ingresado en el metodo empieza. \n\
\n\
    Si usted mantiene el argumento de entrada 'True' \n\
    en el metodo close, como muestra la siguiente linea... \n\
    apenas se termine de ejecutar todo el codigo (su codigo) \n\
    se saldra de prosigue, aun cuando haya impuesto un \n\
    plazo de tiempo. \n\
\n\
    reaccion= prosigue_1.close(True) \n\
\n\
    Pero si se lo quita, prosigue continuara esperando \n\
    que se cumpla el tiempo impuesto \n\
    para él (en este caso 20 segundos). \n\
    y despues de esto si se saldra. \n\
\n\
    Por ultimo: \n\
    cuando digo (su codigo) me estoy refiriendo al codigo \n\
    que se ejecutara dentro de la segunda tarea. \n\
\n\
\n\
==============================================================\n\
translated with google \n\
\n\
THE LICENSE IS: Mozilla Public License 2.0 (MPL 2.0) \n\
\n\
Distributed library package for python, Version: 1.4 \n\
Name: PROSIGUE \n\
\n\
Integrated library dependencies:\n\
\n\
    multiprocessing \n\
    time \n\
    os \n\
\n\
Functionalities that I can see from PROSIGUE:\n\
\n\
    - System management. \n\
    - Query to external servers. \n\
\n\
PROSIGUE is a library that...\n\
\n\
    I have decided to develop it with the purpose of nourishing \n\
    the programming world more. \n\
    It is a library that of course \n\
    seeks to be simple to use. \n\
    And it performs such a practical operation that it could be desired \n\
    in any computer system. \n\
\n\
How to run PROSIGUE:\n\
\n\
    use a format similar to the example above: \n\
\n\
\n\
    You can modify the timeout in: \n\
    prosigue_1.tiempo(20) \n\
\n\
    Also, you should know that this script is \n\
    using an example of the blocks to be executed \n\
    (Classics from the PROSIGUE library)... \n\
    Operar: to do the secondary task, \n\
    in: moviendo= Operador() & \n\
    Restablece: to correct or redo a possible request, \n\
    in: a_restab= Restituye() \n\
\n\
    The second task has a time.sleep(8) \n\
    in the example object here, 'moviendo= Operador()' \n\
    so if you give a wait less than (5 for example) \n\
    will cause the second task to take longer than expected \n\
    by the software designer, in this case you \n\
    and therefore, to expire. simple example of all this:\n\
\n\
    instead of:     prosigue_1.tiempo(20) \n\
    use:            prosigue_1.tiempo(5) \n\
\n\
    Note: finish reading the documentation, since in addition, \n\
    you will have to make an adjustment in the close method of prosigue. \n\
    if you really want to see how it works. \n\
\n\
    A task that is due to timeout may \n\
    enter ELSE (if the ANSWER instance is used).\n\
\n\
    Please replace the two 'classic' operation classes \n\
    for this library, namely (Operator(), Restore()) \n\
    with two personal classes, where you can deposit the code \n\
    that performs the task you want to perform (your code).\n\
    remember that Operador or its replacement will \n\
    execute a task (your code) \n\
    and Restituye or its replacement should correct or restore \n\
    the state first, no matter how far Operador has progressed.\n\
\n\
\n\
    The class that will contain the code (your code) for the second task, \n\
    should have a method called 'empieza' \n\
    inside this method place the code (your code). \n\
    This method should have two (2) input attributes. \n\
    Which are: \n\
\n\
    1. The data given when instantiating the PROSIGUE class,\n\
    (that is, 'dicci' in our example) \n\
\n\
    2. And the Queue command of the multiprocessing library \n\
    (this is entered internally by the Prosigue library) \n\
    when the library is run with the close method \n\
\n\
    The Restituye input method will be called 'termina'.\n\
    and this should have an input attribute\n\
    which should be... (0) or False, mainly. \n\
\n\
    The 'empieza' method should execute the following script in its execution path \n\
    which will be the return of the code of the second task: \n\
\n\
    your_argument_name.put(variable_name_to_return) \n\
\n\
    If the code (your code) does not have this command line \n\
    An error will be thrown \n\
    by the way, your_argument_name is the second attribute \n\
    entered in the empieza method. \n\
\n\
    If you keep the input argument 'True' \n\
    in the close method, as shown in the following line... \n\
    as soon as all the code is finished executing (your code), \n\
    prosigue will be exited, even if you have imposed a \n\
    time limit. \n\
\n\
    reaccion= prosigue_1.close(True) \n\
\n\
    But if you remove it, prosigue will continue waiting \n\
    for the time set for it to expire (in this case 20 seconds). \n\
    and after this it will exit. \n\
\n\
    Finally: \n\
    when I say (your code) I am referring to the code \n\
    that will be executed within the second task. \n\
\n\
")

