#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import commands
import sys
from datetime import datetime
import time

macs = []
nomes = []
horario = []
arvore = []

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


def junta():
	for i in range(len(macs)):
		aux = []
		aux.append(macs[i].strip())
		'''aux.append(nomes[i])'''
		for ii in range(len(macs)):
			if macs[i] == macs[ii] and not jaTem(macs):
				aux.append(nomes[ii])
				aux.append(horario[ii])
		arvore.append(aux)

def jaTem(mac):
	for i in range(len(arvore)):
		if arvore[i][0] == mac:
			return True
	return False

def imprime():
	print '------------'
	for i in range(len(macs)):
		print macs[i]
		print nomes[i]
		print horario[i]
		print ''

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

def main():
	info = pegaMAC()
	info_vet = info.split('\n')
	del info_vet[0:4]
	separa(info_vet)
	tiraCell()
	tiraESSID()
	junta()
	imprimeArvore()
	escreverArquivo()

main()
