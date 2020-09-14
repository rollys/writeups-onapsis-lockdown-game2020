# WriteUp Challenge Lvl1 – Onapsis Lockdown Game2020 - CTF

> Autor: [Rolly Sánchez](https://twitter.com/Pwnakil)

Challenge
========

> One of our developers hid it using this python script, but now he can't recover it.
It seems like the password will change in each run...


Análisis
========

Después de descomprimir el reto Lvl1.7z, vemos que tenemos un archivo python `Decryptor.py`

Cuando se ejecuta el archivo python, te pide ingresar una contraseña que te dará el flag. Escribo una contraseña cualquiera, en este caso ingreso `A` y este es el resultado:
```
python Decryptor.py
```

```
Generating crypto Key...
The Key to generate the password is:
j`~dtpdbxd|lnz

Enter the password to decrypt the Flag:
A
Decrypting the key using the provided password... XOR is the best!

Your flag is:
C

Hmmm... I think thats not the correct flag. Try with a different password.
I used this flag as my OS password many years ago... My windows told me that the hash for it was:
9b3fd5c1db1e4cf7 220525aa8174c2cf
But the hash for your flag is:
f9393d97e7a1873c aad3b435b51404ee
```

Y cada vez que ejecutas el archivo, tu `Crypto Key` va a cambiar, por la pista del reto y por lo mencionado, se deduce que la contraseña para obtener el flag va a ser diferente cada vez que ejecutemos el archivo.

Entonces analizamos el código fuente y nos percatamos 

```Python
print "Generating crypto Key..."
r = Key()
```

que esta parte de código es donde se llama y se genera el `Crypto Key`, revisamos dicha función `Key()`

```Python
def Key():
	return gk(datetime.now(), 96)
```
luego la función `gk()`

```Python
def gk(d, s):
	random.seed(d)
	m = ""
	for i in range(14):
		o = int((random.random()*1000))%32
		o = o+s
		if (o < 32):
			o = o+72
			if (o>92):
				return "ONA(keep_looking)"
		m = m + chr(o & 254)
	return m
```

vemos que esta función recibe una semilla para generar de forma aleatoria el `Crypto Key`, la semilla es la fecha y hora en el momento que se ejecuta el programa, por ello es que la contraseña siempre va a cambiar cada vez que este se ejecute.

También encontramos esta función `vif()`:

```Python
def vif(s, q):
	return (0 == val(xxr(xxr(M,q),xxr(iv(gk(16448250, 64)), s))))
```
En la cual llama una función `xxr()` que hace un xor de la `contraseña ingresada` con el `Crypto Key` y me percaté que podemos tener partes del flag sin ingresar la contraseña completa.

Conclusión
========


1. Existe una contraseña por fecha de ejecución del programa.
2. Vemos que tiene un límite de caracteres para la contraseña.

```
The password cannot be longer than 14 characters, try again!
```
3. Vemos que la contraseña solo debe contener algunos caracteres.

```
Your password can only contain Uppercase letters (A-Z) and the following symbols: @[]\^_
```
4. Se puede obtener partes del flag sin ingresar la contraseña completa

Solución
========

Sabemos que hay una contraseña por fecha de ejecución del programa, entonces comenté y agregué unas líneas código al programa para obtener el flag acuerdo a una contraseña que obedece a la fecha en la que se ejecuté el programa.

Estás son las líneas que comenté del código para que no sea interactivo al ejecutar el programa:

```Python
'''
print "Generating crypto Key..."
r = Key()
k = Q(0xfafafa, r)

print "The Key to generate the password is:\n"+str(r)+"\n"
print "Enter the password to decrypt the Flag:"
p = str(raw_input())
vp(p)

print "Decrypting the key using the provided password... XOR is the best!\n"
f = dc(k, p).upper()

print "Your flag is:\n"+f
if (vif(p,k)):
	print "Correct, now you have the Flag!"
else:
	h = ch(f)
	if (h != True):
		print "\nHmmm... I think thats not the correct flag. Try with a different password."
		print "I used this flag as my OS password many years ago... My windows told me that the hash for it was:\n"+HASH[:16]+" "+HASH[16:]
		print "But the hash for your flag is:\n"+h[:16]+" "+h[16:]
		print
'''
```
Y agregué las siguientes funciones:

`run()` básicamente son las mismas líneas de código que comente anteriormente, con la diferencia que no se ingresa manualmente la contraseña y que retorna 2 valores (La validación y el flag). Esta función acepta 2 parámetros, la `Contraseña` y el `Crypto Key`.

```Python
def run(pswd, key):
	r = key
	k = Q(0xfafafa, r) # 0xfafafa = 16448250
	p = pswd
	vp(p)
	f = dc(k, p).upper()
	validate = vif(p,k)
	if (validate):
		return [validate, f]
	return [False, '']
```

`exploit()` es la función que encarga de generar la contraseña para obtener el flag.

```Python
def exploit():
	ABC = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ@[]\^_'
	password = ''
	your_flag = ''
	key = Key()
	for i in range(14):
		for letter in ABC:
			pswd = password + letter
			[validate, flag] = run(pswd, key)
			if(validate):
				password += letter
				your_flag = flag
				break
	print "Password:\n"+password
	print "Your flag is:\n"+your_flag
```

Explicaré algunas líneas de código de la función mencionada. 

Sabemos que la contraseña tiene ciertos caracteres, por ello creamos un abecedario con los caracteres permitidos que nos dice el programa y llamamos a la función `Key()` para que nos genere un `Crypto Key` único para todas las iteraciones que haremos más adelante y así evitaremos tener una contraseña diferente.

```Python
ABC = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ@[]\^_'
...(code)...
key = Key()
```

También sabemos que la cantidad máxima de caracteres de la contraseña es de 14 caracteres, por ello hacemos una iteración con límite 14 y otra iteración del abecedario para generar una contraseña válida y obtener el flag, para ello en cada iteración concatenamos cada letra del abecedario que posiblemente puede ser una contraseña válida, llamamos la función `run()` pasándole la posible contraseña y el `Crypto Key` único ya generado, esta función validará si la contraseña es correcta.

```Python
for i in range(14):
    for letter in ABC:
        pswd = password + letter
        [validate, flag] = run(pswd, key)
        if(validate):
            password += letter
            your_flag = flag
            break

```

Ya tenemos todo los ingredientes, llamamos a la función `exploit()` y happy hacking!!!

```Python
exploit()
```

Your Flag
========

El resultado es:

```
Password:
ORS]^MU@ZLGYTI
Your flag is:
ONA{HASH||GO~}
```
