#this will take in the ideal contig file (with fasta) and the corresponding orf (having protein fasta) file 
import sys
if len(sys.argv)!=4:
    print ('Please enter 1. contigs 2. ORF 3 outfile ')
    sys.exit()
prog, contig, metageneMark, outfile = sys.argv

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
        val="".join([i.strip() for i in val])
        if key1 not in has:
            has[key1]=[]
        has[key1]+=[(orfId,val)]
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

contig_has=ReadFasta(contig,'normal')
orfHas=ReadFasta(metageneMark,'advanced')

count=0
MergedOrfs={i:orfHas[i] for i in orfHas if i in contig_has}

with open (outfile+'grt100aa','w') as fout:
    for i in MergedOrfs:
        for j in MergedOrfs[i]:
            if len(j[1])>100:    
                count+=1
                fout.write('>%s\n%s\n'%(i+':::'+j[0],j[1]))

print (len(contig_has),len(MergedOrfs),count)

# python bin/contigs_to_orfs.py dataset/summaryContigIdsInterest\(\>300\)_noOrfKnowledge.contigs query/modified/predicted_genes.prot dataset/summaryContigIdsInterest\(\>300\)_noOrfKnowledge.ORFProteins
#340335 332012 535118
#340335 332012 378447

#Only bacteria and archaea
#335538 328009 528175
#335538 328009 374075