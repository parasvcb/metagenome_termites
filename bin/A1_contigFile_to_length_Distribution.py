import sys
import numpy as np
from scipy import stats
if len(sys.argv)!=3:
    print ("Please enter contig file and name of the outfile")
    sys.exit()
prog,contigFile,outfile=sys.argv

def ReadFasta(contig):
    def storeHasNormal(haslocal,key,val):
        key=key.strip()[1:]
        val="".join([i.strip() for i in val])
        if key not in haslocal and len(key)>1:
            haslocal[key]=len(val)
        else:
            print ('repeat',key)
        return haslocal
    has={}
    with open (contig) as fin:
        # dat=fin.read().split('\n')
        key=''
        val=[]
        func=storeHasNormal
        for line in fin:
            if len(line) and line[0]=='>':
                if key and val:
                    has = func(has, key, val)
                    val=[]
                    key=''
                key=line
            else:
                val+=[line]
        if key and val:
            has = func(has,key,val)
    return has

def protein_length(has_object,fout):
    all_tup=[]
    has_bins={(200,300):0,(301,500):0,(501,1000):0,(1001,5000):0,(5001,10000):0,(10001,100000):0,(100001,400000):0}
    for i in has_object:
        for key in has_bins:
            if key[0] <= has_object[i] <= key[1]:
                has_bins[key] += 1
                break
    values=list(has_object.values())
    print (np.mean(values),np.median(values),np.std(values),stats.mode(values))

    values = has_bins.values()
    su = sum(values)
    print (su)
    keys = list(has_bins.keys())
    with open(fout, "w") as fin:
        fin.write("Length_range,Total,Frequency\n")
        keys.sort()
        for i in keys:
            val=round(has_bins[i]/su, 3) if (has_bins[i]/su, 3) else 0
            fin.write("%s,%s,%s\n" %("-".join(map(str,i)), has_bins[i], val))
            print ("%s,%s,%s    " %("-".join(map(str,i)), has_bins[i], val))
            
contigHas=ReadFasta(contigFile)

with open ('outtest') as fout:
    dat=[i[1:].strip() for i in fout.read().split('\n') if len(i)>1]

print (dat[-5:])
print (list(contigHas.keys())[-5:])
print ('contighas',len(contigHas),len(set(contigHas)))
print ('dat',len(dat),len(set(dat)))
print (set(contigHas.keys())-set(dat))
print (set(dat)-set(contigHas.keys()))
protein_length(contigHas,outfile)


#python bin/A1_contigFile_to_length_Distribution.py dataset/query/Termite_contig_kaiju.nuc.fasta results/distribution_lenth.csv