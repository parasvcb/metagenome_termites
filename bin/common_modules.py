import os,subprocess
def ReadContig(contig):
    def storeHas(has,key,val):
        key=key.strip()[1:]
        val="".join([i.strip() for i in val])
        if key not in has:
            has[key]=[val,len(val)]
        return has
    has={}
    with open (contig) as fin:
        key=''
        val=[]

        for line in fin:
            if line[0]=='>':
                if key and val:
                    has = storeHas(has, key,val)
                    val=[]
                key=line
            else:
                val+=[line]
        if key and val:
            has = storeHas(has,key,val)
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

def parsing_metagenemarkTo3tags(metagenresults):
    has={}
    with open (metagenresults) as fin:
        dat=[i for i in fin.read().split('\n')[1:] if len(i)>0]
    #print (dat[:5])
    for i in dat:
        #print (i)
        contigId,tag0,tag1,tag2,sumtag=i.split('\t')
        tag0=int(tag0)
        tag1=int(tag1)
        tag2=int(tag2)

        if tag2:
            has[contigId]=2
        elif tag1:
            has[contigId]=1
        else:
            has[contigId]=0
    return has

def parseKaiju(kaijuResults, lis=['Fungi','Metamonada','Bacteria','Eukaryota','Archaea']):
    with open(kaijuResults) as fin:
         dat=[i for i in fin.read().split('\n')[1:] if len(i)>0]
    has={}
    for i in dat:
        flag=1
        contig,tax,classification=i.split('\t')
        for j in lis:
            if j in classification:
                has[contig]=j
                flag=0
                break
        if flag:
            has[contig]='Others'
    return has




def replaceTaxidToKids(taxonsublistFolder,has):
    print ('here')
    hasnew={}
    for i in has:
        #print (i)
        if i=='1801835':
            print ('yes')
        filename=os.path.join(taxonsublistFolder,i)
        if not os.path.isfile(filename):
            subprocess.call(['taxonkit list --ids %s --indent "" >%s'%(i,filename)],shell=True)
    for i in has:
        filename=os.path.join(taxonsublistFolder,i)
        with open (filename) as fin:
            dat=[j for j in fin.read().split('\n') if len(j)>0]
        for j in dat:
            hasnew[j]=has[i]        
    return hasnew