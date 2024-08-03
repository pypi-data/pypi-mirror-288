#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  pred1.py
#  
#  Copyright 2018 Daniele Raimondi <eddiewrc@vega>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
verbosity = 2
import numpy as np
import os

def sliding_w(vet,intorno=5):#[[1,2],[1,3],[1,2]]
	vetfin=[]

	for i in range(len(vet)):
		if i-intorno<0:
			iniz=0
		else:
			iniz=i-intorno
		if i+intorno+1>len(vet):
			fin=len(vet)
		else:
			fin=i+intorno+1
		a=np.mean(vet[iniz:fin])
		vetfin+=[a]
	return vetfin
def leggifasta(database):  # legge un file fasta e lo converte in un dizionario
	f = open(database)
	uniprot = f.readlines()
	f.close()
	dizio = {}
	for i in uniprot:

		if i[0] == '>':

			if '|' in i:
				uniprotid = i.strip('>\n').split('|')[1]

			elif ' ' in i:

				uniprotid = i.strip('>\n').split(' ')[0]

			else:
				uniprotid = i.strip('>\n')
			dizio[uniprotid] = ''
		else:
			dizio[uniprotid] = dizio[uniprotid] + i.strip('\n').upper()
	return dizio

def parse_uniprot_annotations(fil="/".join(os.path.realpath(__file__).split("/")[:-1])+'/dataset/all_seqs_dnabinding_uniprot.annotations'):
	diz={}
	salta=0
	for i in open(fil).readlines():
		a=i.split()
		try:
			bind_start=int(a[3])-1
			bind_end=int(a[4])
		except:
			salta+=1
			continue
		seq=a[1]
		p1=[0]*bind_start
		p2=[1]*(bind_end-bind_start)
		p3=[0]*(len(seq)-bind_end)
		p=p1+p2+p3
		assert len(p)==len(seq)
		diz[a[0]]=(seq,p)
	#print 'got ',len(diz),'predictions. Saltate',salta
	return diz

