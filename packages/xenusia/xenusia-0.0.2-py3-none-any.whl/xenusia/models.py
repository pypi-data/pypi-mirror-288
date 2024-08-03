#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright 2017 Gabriele Orlando <orlando.gabriele89@gmail.com>
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

import torch,os
from torch import nn
import warnings
warnings.filterwarnings("ignore")
class gru1(nn.Module):

	def __init__(self, n_features=44, max_batch=5, hidden_dim=7, cuda=False, hidden_layers=2, reinitialize_hidden=True):
		super(gru1, self).__init__()
		self.reinitialize_hidden = reinitialize_hidden
		self.cuda = cuda
		self.batch_size = max_batch
		self.hidden_layers = hidden_layers
		self.sigmoid = nn.Sigmoid()
		self.relu = nn.ReLU()
		self.hidden_dim = hidden_dim
		self.hidden1 = self.init_hidden()
		self.hidden2 = self.init_hidden()
		self.hidden3 = self.init_hidden()

		if self.cuda:
			self.gru = nn.GRU(n_features, hidden_dim, num_layers=hidden_layers, bidirectional=True,
							  batch_first=True).cuda()
			self.gru1 = nn.GRU(1, hidden_dim, num_layers=hidden_layers, bidirectional=True, batch_first=True).cuda()
			self.gru2 = nn.GRU(1, hidden_dim, num_layers=hidden_layers, bidirectional=True, batch_first=True).cuda()
		else:
			self.gru = nn.GRU(n_features, hidden_dim, num_layers=hidden_layers, bidirectional=True, batch_first=True)
			self.gru1 = nn.GRU(1, hidden_dim, num_layers=hidden_layers, bidirectional=True, batch_first=True)
			self.gru2 = nn.GRU(1, hidden_dim, num_layers=hidden_layers, bidirectional=True, batch_first=True)
		self.pooling = nn.MaxPool1d(2 * hidden_dim)

	def init_hidden(self):
		if self.cuda:
			return torch.randn(2 * self.hidden_layers, self.batch_size, self.hidden_dim).cuda()
		else:
			return torch.randn(2 * self.hidden_layers, self.batch_size, self.hidden_dim)  # 2 perch+ bidirectional

	def forward(self, sentence):
		if self.reinitialize_hidden:
			self.hidden1 = self.init_hidden()
			self.hidden2 = self.init_hidden()
			self.hidden3 = self.init_hidden()

		### blocco 1 ###
		gru_out, h = self.gru(sentence)
		if self.cuda:
			self.hidden1 = h.data.cuda()
		else:
			self.hidden1 =h.data

		gru_out = self.relu(gru_out)
		gru_out = self.pooling(gru_out)

		gru_out = self.sigmoid(gru_out)
		gru_out = gru_out.view((len(gru_out), -1))

		return gru_out  # ,hidden1,hidden2,hidden3

	def load(self):
		self.load_state_dict(torch.load("/".join(os.path.realpath(__file__).split("/")[:-1])+"/models/nn4_final_state_dict_contact.mtorch"))

	def save(self):
		torch.save(self.state_dict(),"/".join(os.path.realpath(__file__).split("/")[:-1])+"/models/nn4_final_state_dict_contact.mtorch")

class nn1(torch.nn.Module):

	def __init__(self, n_features=89, hidden_dim=70, device="cpu"):
		super(nn1, self).__init__()
		self.device = device

		self.net = torch.nn.Sequential(
			torch.nn.Linear(n_features, hidden_dim),
			torch.nn.ReLU(),
			torch.nn.Linear(hidden_dim, 1),
			torch.nn.Sigmoid()
		).to(self.device)

	def load(self):
		self.load_state_dict(torch.load("/".join(os.path.realpath(__file__).split("/")[:-1])+"/models/nn4_final_state_dict_domain.mtorch"))

	def save(self):
		torch.save(self.state_dict(),"/".join(os.path.realpath(__file__).split("/")[:-1])+"/models/nn4_final_state_dict_domain.mtorch")

	def forward(self, sentence):
		# print sentence

		# print sentence.view(len(sentence),-1)

		out = self.net(sentence)
		return out.squeeze(-1)