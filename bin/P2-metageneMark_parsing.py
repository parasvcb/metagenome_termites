#/home/manisha/projects/manisha_metagenome/ORFs/SO_9758_Termite_predicted.fnn
# previous name ORF_filtering.py
import sys,re,os, subprocess
if len(sys.argv)!=3:
    print ("Please neter correct args 1.metageneMarkmodifiedFile 2.outfile")
    #gene_5|GeneMark.hmm|768_nt|+|1|768:::NODE_131840_length_921_cov_5.03695
    #modified file should have header like that
    sys.exit()
prog, f1, out1=sys.argv

def reverseStrandVerification(has,key,val):
    key=key.strip()
    val="".join(val).strip()
    start=0
    stop=0
    #code=0
    #print (key,val)
    if val[:3] in ['ATG', 'GTG','TTG']:
        start=1
        #print ('yes')
        #sys.exit()
    if val [-3:] in ['TAA', 'TGA', 'TAG']:
        stop=1
        #print ('no')
        #sys.exit()
    if start and stop:
        code = 2
        #print (key)
    elif start or  stop:
        code = 1
    else:
        code=0
    metaId,contigId=key.split(':::')
    metaId=metaId[1:]
    length=len(val)/3
    if length>=100:    
        if contigId not in has:
            has[contigId]=[]
            has2[contigId]={0:0,1:0,2:0}
        has[contigId]+=[metaId+','+str(code)+','+ str(length)]
        has2[contigId][code]+=1
    return has
    #will give code 1 if either of stop and start codon is defined 2 if both and 0 if none
    #ATG, GTG and TTG as starts codons and TAA, TGA and TAG as stop codon

has={}
has2={}
#has 2 is updated via () above, global scope
with open(f1) as fin:
    key=''
    val=[]
    for line in fin:
        if line[0]=='>':
            if key and val:
                has = reverseStrandVerification(has, key,val)
                val=[]
            key=line

        else:
            val+=[line]
    if key and val:
        has = reverseStrandVerification(has,key,val)


with open (out1,'w') as fout:
    fout.write('contig\torfs\n')
    for i in has:
        fout.write('%s\t%s\n'%(i,":".join(has[i])))
#save for every contigId, the number of ORS's associated, type of orf, aa length:, repeat

with open (out1+'.summ','w') as fout:
    fout.write('contig\t0\t1\t2\tsumm\n')
    for i in has2:
        fout.write('%s\t%s\t%s\t%s\t%s\n'%(i,has2[i][0],has2[i][1],has2[i][2],sum(has2[i].values())))
    #for every contig the type of ORF's and their count and cumultive count
    

# print (sum([1 for i in has2 if has2[i][2]]), 'unique contigs')
# print (sum([has2[i][2] for i in has2 if has2[i][2]]), 'totals contigs')
def writeAsperFlag(has):
    has_refined={'both':[],'single':[],'none':[]}
    for i in has:
        if has[i][2]:
            has_refined['both']+=[i]
        elif has[i][1]:
            has_refined['single']+=[i]
        else:
            has_refined['none']+=[i]
    for i in has_refined:
        print (i,len(has_refined[i]))
        with open (out1+'.tag%s'%i,'w') as fout:
            for j in has_refined[i]:
                fout.write('%s\n'%j)
    return

writeAsperFlag(has2)
#python bin/ORF_filtering.py query/modified/predicted_genes.nuc dataset/metageneMArks