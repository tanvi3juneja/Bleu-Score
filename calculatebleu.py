import sys
import os.path
import math
import glob

def unigram(sen):
	r = dict()
	for word in sen:
		if word in r:
			r[word] += 1
		else:
			r[word] = 1
	return r

def bigram(sen):
	r = dict()
	if len(sen) <= 1:
		return r

	for i in xrange(len(sen)-1):
		bi = sen[i] + " " + sen[i+1]
		if bi in r:
			r[bi] += 1
		else:
			r[bi] = 1
	return r

def trigram(sen):
    r=dict()
    if len(sen) <= 2:
        return r

    for i in xrange(len(sen) - 2):
        tri = sen[i] + " " + sen[i + 1] + " " + sen[i+2]
        if tri in r:
            r[tri] += 1
        else:
            r[tri] = 1
    return r

def quadgram(sen):
    r = dict()
    if len(sen) <= 3:
        return r
    for i in xrange(len(sen) - 3):
        quad = sen[i] + " " + sen[i + 1] + " " + sen[i + 2] + " " + sen[i + 3]
        if quad in r:
            r[quad] += 1
        else:
            r[quad] = 1
    return r

def count_bleu(rline,cline):
    #rline = rline.split()
    cline = cline.split()
    ref_count1=dict()
    for line in rline:
        duni=unigram(line.split())
        for word in duni:
            if word in ref_count1:
                ref_count1[word]=max(duni[word],ref_count1[word])
            else:
                ref_count1[word]=duni[word]

    ref_count2=dict()
    for line in rline:
        dbi=bigram(line.split())
        for word in dbi:
            if word in ref_count2:
                ref_count2[word]=max(dbi[word],ref_count2[word])
            else:
                ref_count2[word]=dbi[word]

    ref_count3 = dict()
    for line in rline:
        dtri = trigram(line.split())
        for word in dtri:
            if word in ref_count3:
                ref_count3[word] = max(dtri[word], ref_count3[word])
            else:
                ref_count3[word] = dtri[word]

    ref_count4 = dict()
    for line in rline:
        dquad = quadgram(line.split())
        for word in dquad:
            if word in ref_count4:
                ref_count4[word] = max(dquad[word], ref_count4[word])
            else:
                ref_count4[word] = dquad[word]

    #import pdb;pdb.set_trace()

    c1=0.0
    c2=0.0
    c3=0.0
    c4=0.0
    #ref_len = len(rline)
    cand_len = len(cline)
    #ref_count1 = unigram(rline)
    cand_count1 = unigram(cline)
    #ref_count2 = bigram(rline)
    cand_count2 = bigram(cline)
    #ref_count3 = trigram(rline)
    cand_count3 = trigram(cline)
    #ref_count4 = quadgram(rline)
    cand_count4 = quadgram(cline)
    for u in cand_count1:
        if u in ref_count1:
            c1 += min(cand_count1[u], ref_count1[u])
    for b in cand_count2:
        if b in ref_count2:
            c2 += min(cand_count2[b], ref_count2[b])
    for t in cand_count3:
        if t in ref_count3:
            c3 += min(cand_count3[t], ref_count3[t])
    for q in cand_count4:
        if q in ref_count4:
            c4 += min(cand_count4[q], ref_count4[q])

    return c1,c2,c3,c4,cand_len,(cand_len-1),(cand_len-2),(cand_len-3)
d=[]
cand_file=sys.argv[1]
ref_file=sys.argv[2]
#ref_file = 'C:/Users/tjune/Desktop/Spring 2016/NLP/hw8/d1'
#cand_file = 'C:/Users/tjune/Desktop/Spring 2016/NLP/hw8/candidate-4.txt'
output=open('bleu_out.txt','w')
#f1=open(ref_file,"r")
f2=open(cand_file,"r")
fl=f2.readlines()
clip1 = 0.0
clip2 = 0.0
clip3 = 0.0
clip4 = 0.0
count1 = 0.0
count2 = 0.0
count3 = 0.0
count4 = 0.0
r=0.0
c=0.0
if ref_file.endswith('.txt'):
    f1=open(ref_file,'r')
    d=map(lambda x: [x],f1.readlines())

else:
    #listofDocuments has all the reference files
    listOfDocuments = glob.glob(ref_file + '/*.txt')
    #for every candidate line
    for i in range (0,len(fl)):
        array=[]
        #reading every reference file at line i
        for file in listOfDocuments:
            f3=open(file,'r')
            l1=f3.readlines()
            array.append(l1[i])
        d.append(array)
#reading candidate lines one by one
#print len(fl)
#print len(d)
for k in range(0,len(fl)):
    cline = fl[k]
    #rline has all the appended lines one by one
    rline=d[k]
    #converting rline list into String for using the split function
    #rline1=''.join(rline)

    r += min(map(lambda x:len(x.split()),rline),key=lambda x:abs(x-len(cline.split())))
    c += len(cline.split())
    m, n, p, z, a1, a2, a3, a4 = count_bleu(rline, cline)
    clip1 += m
    clip2 += n
    clip3 += p
    clip4 += z
    count1 += a1
    count2 += a2
    count3 += a3
    count4 += a4
p1 = clip1 / count1
p2 = clip2 / count2
p3 = clip3 / count3
p4 = clip4 / count4
#print p1, p2, p3, p4
# sum1=p1 + p2 + p3 + p4
sum1 = 0.25 * (math.log(p1, math.e) + math.log(p2, math.e) + math.log(p3, math.e) + math.log(p4, math.e))
if c > r:
    bp = 1
else:
    bp = math.exp(1 - r / c)
bleu = bp * math.exp(sum1)
lb = min(1 - r / c, 0) + sum1
# final_bleu_score=bleu_score/lines
#print bleu
output.write(str(bleu))










