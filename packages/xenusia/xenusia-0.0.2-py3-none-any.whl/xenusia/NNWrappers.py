#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2019 Gabriel Orlando <orlando.gabriele89@gmail.com>
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

from sklearn.metrics import roc_auc_score

import time
import numpy as np
import torch as t
import torch
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import Dataset, DataLoader

from sklearn.preprocessing import QuantileTransformer
from xenusia import models
from xenusia.vector_gen import vectorBuilder

class NNwrapper():

	def __init__(self,device='cpu',sequence_prediction=True):
		self.loss = weighted_binary_cross_entropy#torch.nn.BCELoss()

		self.model=models.gru1().to(device)
		self.features = ["backbone","helix","sheet","coil"]
		self.device = device
		self.vb = vectorBuilder()
		self.sequence_prediction = sequence_prediction

	def load(self):
		self.model.load()
	def save(self):
		self.model.save()

	def collateFunctionSingle(self, batch):  # [(X[i], [task1, task2, ...]),... ]
		x = []
		y = []
		for i in range(len(batch)):
			x += [batch[i][0]]
			y += [batch[i][1].unsqueeze(0)]

		y=torch.cat(y,dim=0)

		return x,y

	def collateFunctionSequence(self, batch):  # [(X[i], [task1, task2, ...]),... ]
		if len(batch[0])==2:
			x = []
			y = []
			for i in range(len(batch)):
				x += [batch[i][0]]
				y += [batch[i][1]]

			return x,y
		else:
			x = []
			for i in range(len(batch)):
				x += [batch[i][0]]
			return x
	def buildVector(self,inp):
		v=[]
		#print("build vector contact")
		vectors = self.vb.buildFullVector(inp,features=self.features)

		if type(vectors) == dict:
			for i in sorted(vectors.keys()):
				v+=[vectors[i]]
		else:
			v=vectors
		return v

	class myDataset(Dataset):
		def __init__(self, X, Y = None):
			self.X=X
			self.Y=Y
		def __len__(self):
			return len(self.X)
		def __getitem__(self, idx):
			o=[self.X[idx]]
			if self.Y is not None:
				o+=[self.Y[idx]]
			return tuple(o)

	def get_params(self,deep):
		return {}

	def fit_final_probability(self,ypred):
		self.probability_scaler = QuantileTransformer()
		self.probability_scaler.fit(np.array(ypred).reshape((-1,1)))
		return

	def fit(self, originalX, originalY, epochs = 1000, batch_size=500, weight_decay=0,learning_rate=0.0001):

		#self.pretraining(originalX,originalY,xtestOrig,ytestOrig)

		xvect = self.buildVector(originalX)

		dev=self.device
		self.model.train()
		#self.model.classifier.train()
		#self.model.BertCodon.eval()
		self.dev=dev
		#self.model.training = True

		if batch_size==None or batch_size>len(xvect):
			batch_size=len(xvect)
		print("training with batch",batch_size)

		#x,y,order,padding_lens=u.sortForPadding(originalX,originalY)#=sorted(originalX, key=len)
		x=[]
		#padding_lens=[]
		for i in xvect:
			x+=[torch.tensor(i,dtype=torch.float,device=dev)]

		if self.sequence_prediction:
			y=[]
			for i in originalY:
				y+=[torch.tensor(i,dtype=torch.float,device=dev)]
		else:
			y = torch.tensor(originalY).float().to(dev)

		del xvect

		dataset = self.myDataset(x, y)

		#######MODEL##############		
		parameters = list(self.model.parameters())
		p = []
		for i in parameters:
			p+= list(i.data.cpu().numpy().flat)

		print('\tNumber of parameters=',len(p))

		########OPTIMIZER##########

		optimizer = t.optim.Adam(self.model.parameters(),weight_decay=weight_decay,lr=learning_rate)
		#optimizer = t.optim.Adam(list(self.model.classifier.parameters())+list(self.model.bert.parameters()),weight_decay=weight_decay,lr=learning_rate)

		scheduler = t.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=20, verbose=True, threshold=0.0001, threshold_mode='rel', cooldown=0, min_lr=0, eps=1e-08)
		
		########DATALOADER#########
		if self.sequence_prediction:
			loader = DataLoader(dataset, batch_size=batch_size, shuffle=False, sampler=None, num_workers=0,collate_fn = self.collateFunctionSequence)
		else:
			loader = DataLoader(dataset, batch_size=batch_size, shuffle=False, sampler=None, num_workers=0,collate_fn = self.collateFunctionSingle)

		total_time=time.time()

		print("starting training")
		validation_every = 1
		for e in range(epochs):
			epoch_time=time.time()
			errTot = []
			totepoc=0.0
			start = time.time()
			optimizer.zero_grad()
			self.model.zero_grad()
			pr=[]
			tr=[]
			for sample in loader:

				xOrig, y1 = sample

				xOrig = pad_sequence(xOrig, padding_value=0, batch_first=True).to(dev)
				if self.sequence_prediction:
					y1 = pad_sequence(y1, padding_value=-1, batch_first=True).to(dev)

				yp = self.model(xOrig)
				mask = y1 != -1
				#print y1.shape,yp
				pr += yp[mask].data.cpu().tolist()
				tr += y1[mask].data.cpu().tolist()

				rate=torch.nonzero(y1[mask].data).shape[0]/float(y1[mask].shape[0])


				loss1 = self.loss(yp[mask],y1[mask],weights=[rate,1])
				#maskingloss = y1.sum(-1)==0
				#loss2 = self.loss(yp[maskingloss], y1[maskingloss])
				errTot += [loss1.data.cpu()]
				loss1.backward()
				optimizer.step()
				
				self.model.zero_grad()

			#scheduler.step(np.sum(errTot))
			end = time.time()		

			if e%1==0:
				print(" epoch",e,"loss:",np.mean(errTot),"AUC",round(roc_auc_score(tr, pr),2), "time",round(time.time()-epoch_time,2))
				#if roc_auc_score(tr, pr)>0.80:
				#	return

	def __call__(self,x):
		return self.predict(x)

	def predict(self,originalX,batch_size=100):
		xvect = self.buildVector(originalX)

		dev = self.device
		self.model.eval()


		if batch_size == None or batch_size > len(xvect):
			batch_size = len(xvect)

		x = []
		for i in xvect:
			x += [torch.tensor(i, dtype=torch.float, device=dev)]

		del xvect

		dataset = self.myDataset(x)


		########DATALOADER#########
		if self.sequence_prediction:
			loader = DataLoader(dataset, batch_size=batch_size, shuffle=False, sampler=None, num_workers=0,
								collate_fn=self.collateFunctionSequence)
		else:
			loader = DataLoader(dataset, batch_size=batch_size, shuffle=False, sampler=None, num_workers=0,
								collate_fn=self.collateFunctionSingle)

		pr = []
		for sample in loader:

			xOrig = sample

			xOrigPad = pad_sequence(xOrig, padding_value=0, batch_first=True).to(dev)

			yp = self.model(xOrigPad)

			# print y1.shape,yp
			if self.sequence_prediction:
				for i in range(len(xOrig)):
					pr += [yp[i][:len(xOrig[i])].data.cpu().tolist()]
			else:
				pr += yp.data.cpu().tolist()

		return pr

class NNwrapperDomain(NNwrapper):
	def __init__(self, device='cpu',extra_model = None):
		super(NNwrapperDomain, self).__init__()

		self.loss = weighted_binary_cross_entropy#torch.nn.BCELoss()

		self.model=models.nn1().to(device)
		self.features = ["earlyFolding","compressed","backbone","extraModelAtTheEnd"]
		self.device = device
		self.vb = vectorBuilder()
		self.sequence_prediction = True
		self.extra_model = extra_model

	def buildVector(self,inp):
		v=[]
		#print("build vector domain")
		vectors = self.vb.buildFullVector(inp,features=self.features,extra_model=self.extra_model, sliding_window=5)

		if type(vectors) == dict:
			for i in sorted(vectors.keys()):
				v+=[vectors[i]]
		else:
			v=vectors
		return v

def weighted_binary_cross_entropy(output, target, weights=None):
	if weights is not None:
		assert len(weights) == 2

		loss = weights[1] * (target * torch.log(output)) + \
			   weights[0] * ((1 - target) * torch.log(1 - output))
	else:
		loss = target * torch.log(output) + (1 - target) * torch.log(1 - output)

	return torch.neg(torch.mean(loss))
