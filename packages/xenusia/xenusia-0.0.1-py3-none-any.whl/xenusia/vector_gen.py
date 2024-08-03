import requests,random,string,json,time
import numpy as np
class vectorBuilder():
    def __init__(self):
        self.bio2byteUrl = 'https://bio2byte.be/msatools/api/'
        self.maxTries = 10

    def get_compressed(self,seqsTot):
        compressed = {'A': [1, 0, 0, 0, 0, 0],
                      'C': [0, 1, 0, 0, 0, 0],
                      'E': [0, 0, 1, 0, 0, 0],
                      'D': [0, 0, 1, 0, 0, 0],
                      'G': [1, 0, 0, 0, 0, 0],
                      'F': [0, 0, 0, 1, 0, 0],
                      'I': [0, 0, 0, 0, 0, 1],
                      'H': [0, 0, 0, 0, 1, 0],
                      'K': [0, 0, 0, 0, 1, 0],
                      'M': [0, 0, 0, 0, 0, 1],
                      'L': [0, 0, 0, 0, 0, 1],
                      'N': [0, 0, 1, 0, 0, 0],
                      'Q': [0, 0, 1, 0, 0, 0],
                      'P': [1, 0, 0, 0, 0, 0],
                      'S': [1, 0, 0, 0, 0, 0],
                      'R': [0, 0, 0, 0, 1, 0],
                      'T': [1, 0, 0, 0, 0, 0],
                      'W': [0, 0, 0, 1, 0, 0],
                      'V': [0, 0, 0, 0, 0, 1],
                      'X': [0, 0, 0, 0, 0, 0],
                      'Z': [0, 0, 0, 0, 0, 0],
                      'Y': [0, 0, 0, 1, 0, 0]}

        if type(seqsTot)==list:
            seqsTotal={}
            for k in range(len(seqsTot)):
                seqsTotal[k]=seqsTot[k]
        else:
            seqsTotal=seqsTot

        dafare = list(seqsTotal.keys())

        vects = {}
        for id in dafare:
            vects[id] = [compressed[k] if k in compressed else compressed["X"] for k in seqsTotal[id]]

        return vects
    def bio2byte_predictions(self,seqsTot,verbose=0):
        if type(seqsTot)==list:
            seqsTotal={}
            for k in range(len(seqsTot)):
                seqsTotal[k]=seqsTot[k]
        else:
            seqsTotal=seqsTot
        dafare = list(seqsTotal.keys())
        seqPerChunks=50
        chunks=[]
        for i in range(0, len(dafare), seqPerChunks):
            chunks+= [dafare[i:i + seqPerChunks]]
        resultsFinal ={}
        for c in chunks:
            seqs = {i:seqsTotal[i] for i in c}
            seqs= dict(seqs)
            token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=11))
            seqs["tool_list"] = ["efoldmine"]
            seqs["token"] = token

            over=False
            tries=0
            while not over and tries<self.maxTries:
                try:
                    x = requests.post(self.bio2byteUrl, json=seqs)
                    over=True
                except:
                    tries += 1
                    time.sleep(2)
            if x.status_code!=202:
                raise Exception('Unable to connect to the Bio2byte website for the EFoldMine predictions')

            hashID = str(json.loads(x.text)["hash_id"])

            #time.sleep(5)
            over=False
            tries=0

            while not over and tries<self.maxTries:
                try:
                    results = requests.get(self.bio2byteUrl + hashID)
                    resultsDiz = json.loads(results.text)
                except:
                    resultsDiz={}

                if resultsDiz!={}:
                    over=True
                    resultsDiz=resultsDiz["results"]
                    if verbose > 1:
                        print("predictions of Efoldmine obtained")
                else:
                    if verbose>1:
                        print("failed retriving predictions of Efoldmine at attempt",tries,"retrying...")
                    tries+=1
                    time.sleep(2)


            #resultsDiz = json.loads(results.text)["results"]

            resultsFinal.update({i["proteinID"]: {"backbone":i["backbone"],
                                        "helix": i["helix"],
                                        "sheet": i["sheet"],
                                        "coil": i["coil"],
                                        "earlyFolding": i["earlyFolding"]
                                        } for i in resultsDiz})
        return resultsFinal
    def buildFullVector(self,seqsTot,features=["backbone","helix","sheet","coil"],extra_model=None,sliding_window=5):

        if type(seqsTot)==list:
            seqs={}
            for k in range(len(seqsTot)):
                seqs[k]=seqsTot[k]
        else:
            seqs=seqsTot

        compressed = self.get_compressed(seqs)
        predictions = self.bio2byte_predictions(seqs)

        if extra_model is not None:
            if type(seqsTot)==list:
                names= range(len(seqsTot))
            else:
                names = sorted(seqsTot.keys())
            other_model_prediction = extra_model.predict(seqsTot)
            other_model_prediction = { names[i]: other_model_prediction[i] for i in range(len(names)) }

        if type(seqsTot)==list:
            newPred = {int(i):predictions[i] for i in predictions.keys()}
            predictions = newPred

        vectors={}
        for id in seqs.keys():
            if not id in predictions:
                fatto=False
                while not fatto:
                    #print("reduing", id)
                    a = self.bio2byte_predictions({"redo":seqs[id]})
                    if "redo" in a:
                        fatto=True
                        predictions.update({id:a["redo"]})

            for k,curr_fea in enumerate(features):
                if curr_fea=="extraModelAtTheEnd":
                    continue
                if k==0:

                    if curr_fea in predictions[id]:
                        vectors[id] = [[i] for i in predictions[id][curr_fea]]
                    elif curr_fea == "compressed":
                        vectors[id] = [i for i in compressed[id]]

                    elif curr_fea == "extraModel":
                        vectors[id] = [[i] for i in other_model_prediction[id]]
                    else:
                        raise Exception('Feature', curr_fea, "not recognized")


                else:
                    for i in range(len(vectors[id])):
                        if curr_fea in predictions[id]:
                            vectors[id][i]+=[predictions[id][curr_fea][i]]
                        elif curr_fea == "compressed":
                            vectors[id][i] += [compressed[id][i]]
                        elif curr_fea == "extraModel":
                            vectors[id][i] += [other_model_prediction[id][i]]
                        else:
                            raise Exception('Feature',curr_fea,"not recognized")


        for id in sorted(list(vectors.keys())):
            vectors[id] = self.make_sliding_window(vectors[id],intorno = sliding_window)

        if "extraModelAtTheEnd" in features:
            #print("build vector extra")
            for id in seqs.keys():
                for i in range(len(vectors[id])):
                    vectors[id][i] = [other_model_prediction[id][i]] + vectors[id][i]

        return vectors
    def make_sliding_window(self,vetIniz, intorno=3):
        vet = []
        #vetIniz=np.array(vetIniz)
        nfea = len(vetIniz[0])

        for fea in range(len(vetIniz[0])):
            if type(vetIniz[0][fea])==list:
                nfea = len(vetIniz[0][fea])
            else:
                nfea=1
            for i in range(len(vetIniz)):
                tmp=[]
                for s in range(-intorno, intorno + 1):
                    if i + s < 0:
                        tmp += [0]*nfea
                    elif i + s >= len(vetIniz):
                        tmp += [0]*nfea
                    else:
                        if nfea==1:
                            tmp += [vetIniz[i + s][fea]]
                        else:
                            tmp += vetIniz[i + s][fea]
                if fea==0:
                    vet+=[tmp]
                else:
                    vet[i]+=tmp

        return vet


if __name__ == '__main__':
    a=vectorBuilder()
    a.buildFullVector({"culo":"AAADDDDAAAADDDDAAAAAAAAAAAAAAAAFFFFFFFFFFFFAAAAAAAAAAAAAAAAAA","culo2":"AAADDDDAAAADDFFFFDDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"})