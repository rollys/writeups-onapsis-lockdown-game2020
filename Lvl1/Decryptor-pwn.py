import sys
import random
from datetime import datetime
from passlib.hash import lmhash


M = '\xD8\xC7\xD8\xCA\xD5\xD2\xC0\xC1\xD5\xDF\xD4\xC6\xDB\xC8'

HASH = "9b3fd5c1db1e4cf7220525aa8174c2cf"

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


def iv(k):
	s= "\xFF"
	for i in range(14):
		s = s + chr(255)
	return xxr(k,s)


def vp(p):
	if (len(p)>14):
		print "The password cannot be longer than 14 characters, try again!"
		exit()
	for i in p:
		if (ord(i)<64 or ord(i)>95):
			print "Your password can only contain Uppercase letters (A-Z) and the following symbols: @[]\^_"
			exit()
	return True


def val(s):
	out = 0
	for i in s:
		out = out + ord(i)
	return out


def xxr(p, k):
	l = len(p)
	if (len(p) > len(k)):
		l = len(k)
	out = ""
	for i in range(l):
		out = out + chr(ord(p[i])^ord(k[i]))
	return out


def Key():
	return gk(datetime.now(), 96)


def Q(n, k):
	return xxr(gk(n, 64), k)


def ch(s):
	h = lmhash.hash(s)
	for k in range(len(h)):
		if (h[k] != HASH[k]):
			return h
	return True


def vif(s, q):
	return (0 == val(xxr(xxr(M,q),xxr(iv(gk(16448250, 64)), s))))


def dc(s, k):
	return xxr(s,k)


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

exploit()