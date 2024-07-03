#this will take in the ideal contig file (with fasta) and the corresponding orf (having protein fasta) file 
import sys
if len(sys.argv)!=5:
    print ('Please enter 1. contigs 2. ORF 3. startstopcodonInfo 4 outfile ')
    sys.exit()
prog, contigFile, metageneMark, orftypeInfo, outfile = sys.argv


'''
==> results/metageneMArks <==
contig	orfs
NODE_520770_length_391_cov_2.17262	gene_1|GeneMark.hmm|390_nt|-|2|391,0,130.0
NODE_119461_length_980_cov_3.84	gene_3|GeneMark.hmm|558_nt|-|3|560,1,186.0:gene_4|GeneMark.hmm|312_nt|-|640|951,2,104.0
NODE_131840_length_921_cov_5.03695	gene_5|GeneMark.hmm|768_nt|+|1|768,1,256.0
NODE_851963_length_301_cov_26.4959	gene_7|GeneMark.hmm|300_nt|-|2|301,0,100.0
NODE_112271_length_1021_cov_4.63561	gene_10|GeneMark.hmm|741_nt|-|281|1021,1,247.0
NODE_77748_length_1290_cov_7.93036	gene_11|GeneMark.hmm|357_nt|-|300|656,2,119.0:gene_12|GeneMark.hmm|510_nt|+|781|1290,1,170.0

'''

def orfType(fname):
    with open (fname) as fin:
        dat=[i for i in fin.read().split('\n')[1:] if len(i) >0]
    has={}
    for i in dat:
        contig,orfs=i.split('\t')
        for moreOrfs in orfs.split(':'):
            header,typeOrf,length=moreOrfs.split(',')
            subeleHeader=header.split("|")
            # fractochange=subeleHeader[2].split('_')[0]
            # subeleHeader[2]=str(int(int(fractochange)/3))+'_aa'
            header="|".join(subeleHeader[:2]+subeleHeader[3:])
            typeOrf=int(typeOrf)
            has[header]=typeOrf
    has2={0:0,1:0,2:0}
    for i in has:
        has2[has[i]]+=1
    print (has2)
    return has



def ReadFasta(contig,value='normal'):
    def storeHasNormal(has,key,val):
        key=key.strip()[1:]
        val="".join([i.strip() for i in val])
        if key not in has:
            has[key]=0
        return has
    def storeHasAdvanced(has,key,val):
        #key should be like >gene_1|GeneMark.hmm|130_aa|-|2|391:::NODE_520770_length_391_cov_2.17262

        orfId,key1=key.strip()[1:].split(':::')
        subeleHeader=orfId.split("|")
        header="|".join(subeleHeader[:2]+subeleHeader[3:])
        val="".join([i.strip() for i in val])
        if key1 not in has:
            has[key1]=[]
        has[key1]+=[(header,val)]
        return has
    has={}
    with open (contig) as fin:
        key=''
        val=[]
        func=storeHasNormal if value == 'normal' else storeHasAdvanced
        for line in fin:
            if line[0]=='>':
                if key and val:
                    has = func(has, key,val)
                    val=[]
                key=line
            else:
                val+=[line]
        if key and val:
            has = func(has,key,val)
    return has

orfwithTags=orfType(orftypeInfo)
#reading the tags, and storing such tag as value per key as orf id, (coberted to aa)

contig_has=ReadFasta(contigFile,'normal')
#stores contig as key and its nt seq as value
#reading the subset of contigs or complete set, contigs as keys and values as orfs in them

orfHas=ReadFasta(metageneMark,'advanced')
#for every contig, use it as key then the orfs pair as values, (orfid,length of orf) 

keyslist=list(orfwithTags.keys())
for i in keyslist[:5]:
    print (i,orfwithTags[i])
print (len(orfwithTags))
# this is nt
count=0

MergedOrfs_typeboth={}
MergedOrfs_notTypeBoth={}
for contigs in orfHas:
    if contigs in contig_has:
        for orfs in orfHas[contigs]:
            if orfs[0] in orfwithTags:
                if orfwithTags[orfs[0]]==2:
                    if contigs not in MergedOrfs_typeboth:
                        MergedOrfs_typeboth[contigs]=[]
                    MergedOrfs_typeboth[contigs]+=[orfs]
                else:
                    if contigs not in MergedOrfs_notTypeBoth:
                        MergedOrfs_notTypeBoth[contigs]=[]
                    MergedOrfs_notTypeBoth[contigs]+=[orfs]
print (len(MergedOrfs_notTypeBoth))
print (len(MergedOrfs_typeboth))
                
# MergedOrfs_typeboth={i:[j for i in orfHas for j in orfhas[i] if i in contig_has and j[0] == 2]}
# MergedOrfs_notTypeBoth={i:[j for i in orfHas for j in orfhas[i] if i in contig_has and j[0] != 2]}


def writeORFS(fname,has): 
    count=0
    with open (fname,'w') as fout:
        for i in has:
            for j in has[i]:
                if len(j[1])>100:    
                    count+=1
                    fout.write('>%s\n%s\n'%(i+':::'+j[0],j[1]))


writeORFS(outfile+'grt100aa_bothStartStopCodons',MergedOrfs_typeboth)
writeORFS(outfile+'grt100aa_notBothStartStopCodons',MergedOrfs_notTypeBoth)

# python bin/contigs_to_orfs.py dataset/summaryContigIdsInterest\(\>300\)_noOrfKnowledge.contigs query/modified/predicted_genes.prot results/metageneMArks dataset/summaryContigIdsInterest\(\>300\)_noOrfKnowledge.ORFProteins