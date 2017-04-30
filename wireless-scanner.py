#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import commands
import sys
from datetime import datetime
import time
import platform

macs = []
nomes = []
horario = []
arvore = []

def detectaSO():
	so = platform.system()
	if so != "Linux":
		print "É necessário Linux para execução do script."
		sys.exit(0)

def pegaMAC():
	out= commands.getoutput('iwlist scan | grep -E "Address|ESSID"')
	return out

def separa(info_vet):
	for i in range(len(info_vet)):
		if i%2==0:
			macs.append(info_vet[i].strip())
		else:
			nomes.append(info_vet[i].strip())
		horario.append(datetime.now())

def tiraError(info_vet):
	for i in range(len(info_vet)):
		if "Interface doesn\'t support scanning." in info_vet[i]:
			print 'tem'
			print i
			info_vet.remove(info_vet[i])
	return info_vet

def tiraCell():
	aux = []
	for i in range(len(macs)):
		aux.append(macs[i])
	del macs[0:len(macs)]
	for i in range(len(aux)):
		straux = "Cell "
		if i < 9:
			straux = straux + "0" + str((i+1)) + " - Address: "
		else:
			straux = straux + str((i+1)) + " - Address: "	
		macs.append(aux[i].replace(straux,""))

def tiraESSID():
	aux = []
	for i in range(len(nomes)):
		aux.append(nomes[i])
	del nomes[0:len(nomes)]
	for i in range(len(aux)):
		nomes.append(aux[i].replace("ESSID:", "").replace("\"", ""))

def tiraRepetidos():
	for i in range(len(arvore)):
		for ii in range(len(arvore[i])):
			for iii in range(len(macs)):
				if arvore[i][0] == macs[iii] and arvore[i][ii] == nomes[iii]:
					del macs[iii]
					del nomes[iii]
					break

def junta():
	for i in range(len(macs)):
		tem = jaTem(macs[i])
		if tem != -1:# se ja tem entra aqui
			print 'ja tem'
			posicoes = jaTemBSSID(arvore[tem], nomes)
			for ii in range(len(posicoes)):
				arvore[tem].append(nomes[posicoes[ii]])
				arvore[tem].append(horario[posicoes[ii]])
		else:
			aux = []
			aux.append(macs[i].strip())
			aux.append(nomes[i])
			aux.append(horario[i])
			arvore.append(aux)
'''			for iii in range(len(macs)):
				if macs[i] == macs[iii] and jaTem(macs) == -1:
					aux.append(macs[i].strip())
					aux.append(nomes[iii])
					aux.append(horario[iii])'''

def jaTem(mac):
	for i in range(len(arvore)):
		if arvore[i][0] == mac:
			return i
	return -1

def jaTemBSSID(galho, bssid_list):
	posicoes = []
	for i in range(len(galho)):
		achou = False;
		aux = 0
		#if i == 0:
		#	i = i + 1
		for ii in range(len(bssid_list)):
			aux = ii
			if ii == 0:
				print 'galho ', galho[i], 'bssid ', bssid_list[ii]
			if galho[i] == bssid_list[ii] and galho[i][0] == macs[ii]:
				achou = True
				break
		if not achou:
			posicoes.append(ii)
	return posicoes

def imprime():
	for i in range(len(macs)):
		print macs[i]
		print nomes[i]
		print horario[i]
		print 

def imprimeArvore():
	for i in range(len(arvore)):
		print '┌──■', arvore[i][0]
		for ii in range(len(arvore[i])):
			if ii > 0 and ii < len(arvore[i])-1:
				print '├───────■ ', arvore[i][ii]
			elif ii == len(arvore[i])-1:
				print '└───────■ ', arvore[i][ii]
		print 

def escreverArquivo():
	arquivo = open('/home/bruno/Hacking/Ferramentas/sniffaps/aps.csv', 'a+')
	arquivo.write('MAC,BSSID,1ª VEZ VISTO PELO SCAN,\n')
	for i in range(len(arvore)):
		for ii in range(len(arvore[i])):
			if ii == 0:
				arquivo.write(arvore[i][0]+',')
			elif ii > 0:
				arquivo.write(str(arvore[i][ii])+',')
			if ii == len(arvore[i])-1:
				arquivo.write('\n')
	arquivo.close()

def loop():
	while True:
		print '========='
		info = pegaMAC()
		info_vet = info.split('\n')
		#info_vet = tiraError(info_vet)
		del info_vet[0:4]
		separa(info_vet)
		tiraCell()
		tiraESSID()
		tiraRepetidos()
		junta()
		os.system('clear')
		imprimeArvore()
		time.sleep(0)
		del macs[0:len(macs)]
		del nomes[0:len(nomes)]
		del horario[0:len(horario)]

def semloop():
	print '========='
	info = pegaMAC()
	info_vet = info.split('\n')
	#info_vet = tiraError(info_vet)
	del info_vet[0:4]
	separa(info_vet)
	tiraCell()
	tiraESSID()
	junta()
	os.system('clear')
	imprimeArvore()
	#time.sleep(10)
	macs = []
	nomes = []
	horario = []

def main():
	try:
		detectaSO()
		loop()
		#semloop()
		#escreverArquivo()
	except KeyboardInterrupt:
		sys.exit(0)
main()
