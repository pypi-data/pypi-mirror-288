#!/usr/bin/env python
# -*- coding: utf-8 -*-
from xenusia import utils,NNWrappers

def predict(sequences,device="cpu"):
	"""
	:param sequences: dictionary of protein sequences {ID1:proteinSeq1,ID2:proteinSeq2,ID3:proteinSeq3}
	:param device: cpu or cuda
	:return: predictions as a dictionary {ID1:score1,ID2:score2,ID3:score3}
	"""
	print("Testing ",len(sequences),"proteins")
	contactModel = NNWrappers.NNwrapper(device=device)
	contactModel.load()
	model = NNWrappers.NNwrapperDomain(device=device, extra_model=contactModel)
	model.load()

	names = sorted(sequences.keys())
	resu = model.predict(sequences)
	x=[]
	for i in range(len(resu)):
		cc = utils.sliding_w(list(resu[i]))
		x += [max(cc)]

	return {names[i]: x[i] for i in range(len(names))}
