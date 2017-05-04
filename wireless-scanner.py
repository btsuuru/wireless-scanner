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
	out= commands.getoutput('iwlist wlan0 scan | grep -E "Address|ESSID"')
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

class Dispositivo:
	def __init__(self):
		self.mac = ""
		self.bssid = []
		self.qtBssid = 0
		self.horarios1 = []
		self.horarios2 = []

	def novo(self, m, b, h1, h2): # m = MAC; b = BSSID; h = HORARIO
		self.mac = m
		self.bssid.append(b)
		self.qtBssid = 1
		self.horarios1.append(h1)
		self.horarios2.append(h2)

	def atualizaHorario(hr, pos):
		self.horarios2[pos] = hr

	def insereBSSID(self, bssid, h1, h2):
		self.bssid.append(bssid)
		self.horarios1.append(h1)
		self.horarios2.append(h2)
		self.qtBssid = self.qtBssid + 1

class Arvore:
	def __init__(self):
		self.dispositivos = []
		self.quantidade = 0

	def insere(self, m, b, h1, h2):
		disp = Dispositivo()
		disp.novo(m, b, h1, h2)
		self.dispositivos.append(disp)
		self.quantidade = self.quantidade + 1

	def imprimeArvore(self):
		for dispositivo in self.dispositivos:
			print '┌──■', dispositivo.mac
			for i in range(len(dispositivo.bssid)):
				if i != dispositivo.qtBssid-1:
					print '├───────■ BSSID: ', dispositivo.bssid[i]
					print '├───────■ HR INICIO: ', str(dispositivo.horarios1[i])[0:19]
					print '├───────■ HR FIM:    ', str(dispositivo.horarios2[i])[0:19]
				else:
					print '├───────■ BSSID: ', dispositivo.bssid[i]
					print '├───────■ HR INICIO: ', str(dispositivo.horarios1[i])[0:19]
					print '└───────■ HR FIM:    ', str(dispositivo.horarios2[i])[0:19]
			print

	def insereArvore(self, m, b, h1, h2):
		for dispositivo in self.dispositivos:
			if dispositivo.mac == m:
				for i in range(len(dispositivo.bssid)):
					if dispositivo.bssid[i] == b:
						dispositivo.horarios2[i] = h2
						return
				dispositivo.insereBSSID(b, h1, h2)
				return
		self.insere(m, b, h1, h2)

def escreverArquivo(arvore):
	arquivo = open('/home/bruno/Hacking/Ferramentas/sniffaps/aps.csv', 'a+')
	arquivo.write('MAC,BSSID,1ª VEZ VISTO PELO SCAN,ULTIMA VEZ VISTO PELO SCAN,TEMPO ONLINE,\n')
	for dispositivo in arvore.dispositivos:
		for i in range(len(dispositivo.bssid)):
			arquivo.write(dispositivo.mac +',')
			arquivo.write(dispositivo.bssid[i]+',')
			arquivo.write(str(dispositivo.horarios1[i])[0:19]+',')
			arquivo.write(str(dispositivo.horarios2[i])[0:19]+',')
			arquivo.write(str(dispositivo.horarios2[i]-dispositivo.horarios1[i])[0:7]+'\n')
	arquivo.close()

def loop(arvore):
	while True:
		info = pegaMAC()
		print '-'
		info_vet = info.split('\n')
		#info_vet = tiraError(info_vet)
		#del info_vet[0:4]
		separa(info_vet)
		tiraCell()
		tiraESSID()
		hrScan = datetime.now()
		for i in range(len(macs)):
			arvore.insereArvore(macs[i], nomes[i], horario[i], hrScan)
		os.system('clear')
		arvore.imprimeArvore()
		time.sleep(0)
		del macs[0:len(macs)]
		del nomes[0:len(nomes)]
		del horario[0:len(horario)]

def semloop():
	info = pegaMAC()
	print '-'
	info_vet = info.split('\n')
	#info_vet = tiraError(info_vet)
	del info_vet[0:4]
	separa(info_vet)
	tiraCell()
	tiraESSID()
	hrScan = datetime.now()
	for i in range(len(macs)):
		arvore.insereArvore(macs[i], nomes[i], horario[i], hrScan)
	arvore.imprimeArvore()
	#os.system('clear')
	time.sleep(0)
	del macs[0:len(macs)]
	del nomes[0:len(nomes)]
	del horario[0:len(horario)]

def main():
	try:
		detectaSO()
		arvore = Arvore()
		loop(arvore)
		#escreverArquivo()
	except KeyboardInterrupt:
		op = raw_input("\rDeseja escrever a saída em um arquivo?[S/n]: ")
		if op == 'S' or op == '':
			escreverArquivo(arvore)
		sys.exit(0)
main()
