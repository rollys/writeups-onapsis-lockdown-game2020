# WriteUp Challenge Lvl2 – Onapsis Lockdown Game2020 - CTF

> Autor: [Rolly Sánchez](https://twitter.com/Pwnakil)

Challenge
========

> I love to play music games, but my friends hate 
when I play on their computers.


Análisis
========

Después de descomprimir el reto Lvl2.7z, encontramos un archivo  `knocking.py`, un archivo `.music` y un `Requeriments.txt`.

Después de instalar los requerimientos, ejecutamos el programa, le damos enter para empezar el juego, comienza a sonar una canción, aparentemente el juego consiste presionar una tecla(enter) en el segundo o los segundos correctos y así ganar el juego:

```
Hello rock fan!!! Here is a game you will like
Give me a minute to generate and load the chords...
Ok, im ready. Hit Intro to start playing the music and dont lose the pitch:



You Failed! You are not listening to the music... Practice some more and try again!
```

Entonces intentamos abrir el archivo `knocking.py`, vemos que no se puede(en el editor vscode).

Entonces verificamos que tipo de archivo es con el comando `file`

```
knocking.py: python 2.7 byte-compiled
```

Vemos que es un python compilado y para saber exactamente que es lo que hace el programa, tenemos que descompilar el binario y para ello bajaremos esta librería `uncompyle6`.

```
pip install uncompyle6
```

Renombramos el archivo `knocking.py` a `knocking.pyc` y procedemos a decompilarlo.

```
uncompyle6 knocking.pyc > knocking-dec.py
```

Analizamos el código fuente de `knocking-dec.py` y encontramos que el programa ejecuta una iteración de 20 y en que cada iteración llama a la función `chrKnock()` y el resultado debe ser diferente de `falso` para obtener el flag en base64, ya que líneas más abajo se ve decodeando el flag y mostrado en la pantalla.

```Python
for i in range(20):
    out = chrKnock(ini, i * 3)
    if out != False:
        f = f + out
    ...(code)...

time.sleep(7)
print '\nCongratulations, you Rock!!! Here you have your reward:'
print str(base64.b64decode(f))
# okay decompiling knocking.pyc
```

Luego analizamos la función `chrKnock()`.

```Python
def chrKnock(initial, tn):
    s = ''
    a = knock(initial, dat[tn])
    if a == False:
        return False
    b = knock(initial, dat[(tn + 1)])
    if b == False:
        return False
    c = knock(initial, dat[(tn + 2)])
    if c == False:
        return False
    if a != False:
        s = s + a
        if b != False:
            s = s + b
            if c != False:
                s = a + c
                return s
    return False
```

Vemos que aquí se llama a otra función `knock()` y que esta debe ser diferente de `falso` para obtener el flag y que se le pasa 2 parámetros, el que no es importa es el 2do parámetro que básicamente un array de array's y que parece que tiene nuestro flag encodeado.

```Python
dat = [
 [
  61, 'Z'], [61, '4'], [61, 'm'], [68, 'x'], [68, 'b'], [68, 'h'], [75, 'Z'], [75, 'a'], [76, 'y'], [82, 'B'], [82, 'd'], [83, 'P'], [148, 'T'], [148, '8'], [149, 'k'], [155, 'F'], [156, 'c'], [156, '7'], [162, 'S'], [163, '9'], [163, '2'], [170, '4'], [170, '2'], [170, 'w'], [234, 'K'], [235, '0'], [235, 'G'], [241, 't'], [242, '7'], [242, 'p'], [249, 'b'], [249, '5'], [250, 'l'], [256, '9'], [256, 'b'], [257, 'J'], [263, 'b'], [264, '4'], [264, 'n'], [271, 'R'], [271, 'd'], [271, 'S'], [278, 'M'], [278, 'f'], [278, 'F'], [285, '9'], [285, 'e'], [286, 'I'], [292, 'Z'], [292, '7'], [293, 'T'], [299, 'R'], [300, '0'], [300, '2'], [306, 'Z'], [307, 'a'], [307, 'U'], [314, '5'], [314, '2'], [314, '9']]
```

Ahora pasamos analizar la función `knock()` y vemos que aquí nos pide presionar una tecla con `raw_input()` y que está asignada a una variable `k` que no es usada, luego vemos una condicional de la variable `delta` que debe ser menor que `2` para retornar el segundo valor de unos de los array's de `dat` y no un valor falso, que es lo que queremos evitar.

```Python
def knock(initial, tr):
    k = raw_input()
    b = datetime.now()
    delta = b - initial
    delta = abs(delta.seconds - tr[0])
    if delta < 2:
        return tr[1]
    return False
```

Conclusión
========


1. Hacer que la función `knock()` siempre vuelva un valor diferente de `false`
2. La variable `dat` tiene nuestro flag encodeado.

Solución
========

Para hacer que la función `knock()` nos vuelva un valor diferente de `falso`, tenemos que modificar 1 línea de código y comentar algunas cosas para que no haya interacción con la consola.


Primero comentaremos las líneas de código para quitar la interacción con el programa.

```Python
...(code)...

def knock(initial, tr):
    #k = raw_input()
    b = datetime.now()
    delta = b - initial
    delta = abs(delta.seconds - tr[0])
    if delta < 2:
        return tr[1]
    return False


...(code)...

print 'Ok, im ready. Hit Intro to start playing the music and dont lose the pitch:'
#raw_input()
player = vlc.MediaPlayer('.KnockinOnHeavensDoor.mp3')
player.play()
ini = datetime.now()
f = ''

...(code)...

#time.sleep(7)
print '\nCongratulations, you Rock!!! Here you have your reward:'
print str(base64.b64decode(f))
```
Como se observa, he comentado todo las funciones `raw_input()` y el sleep `time.sleep(7)` que hace que el programa se pause 7 segundos.

Ahora modificamos el valor de la variable `delta` en la función `knock()` y le asígnamos un valor menor que `2`, en este caso `1`.

```Python
def knock(initial, tr):
    k = raw_input()
    b = datetime.now()
    delta = b - initial
    delta = 1 #abs(delta.seconds - tr[0])
    if delta < 2:
        return tr[1]
    return False
```

Y con esto tenemos todo los cambios necesarios, happy hacking!!!


Your Flag
========

El resultado es:

```
Hello rock fan!!! Here is a game you will like
Give me a minute to generate and load the chords...
Ok, im ready. Hit Intro to start playing the music and dont lose the pitch:

Congratulations, you Rock!!! Here you have your reward:
flag ONA{Kn0(kin_IntR0_He4veN}
```
