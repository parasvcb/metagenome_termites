'''
#previous name was complete_NR_with_taxon.py
'''
import pickle
import os,re
def read_pickle(filename):
    with open (filename,'rb') as fin:
        dat=pickle.load(fin)
    return dat

def write_pickle(filename,data):
    with open (filename,'wb') as fin:
        pickle.dump(data,fin)

from progress.bar import Bar
def giveDict(fname):
    '''
    #fname looks like that
    accession       accession.version       taxid   gi
    A0A009IHW8      A0A009IHW8.1    1310613 1835922267
    A0A023FBW4      A0A023FBW4.1    34607   1939884164
    A0A023FBW7      A0A023FBW7.1    34607   1939884197
    A0A023FDY8      A0A023FDY8.1    34607   1939884201
    A0A023FF81      A0A023FF81.1    34607   1939884159
    A0A023FFB5      A0A023FFB5.2    34607   1939884210
    '''
    bar=Bar('reading_prot_todict....',max=933717462)
    print ('here')
    has={}
    with open (fname) as fin:
        for i in fin:
            try:
                ele=i.strip().split()
                has[ele[0]]=ele[2]
            except:
                pass
            bar.next()
    bar.finish()
    print (len(has),'keys_has')
    return has

def writeFilefasta(key,val,fout,has,counter, taxa_unknown):

        '''
        For every header, it will screen if its accession without version has the annotated taxid in prot2accesion.taxid or not, 
        '''
        list_acc=key.strip().split(']')
        #splitting for every repeated name 
        list_acc=[i.split('.')[0] for i in list_acc]
        #saved the  accession in startng of line or juts after pecies description enclosedin the []
        eleTobeExcepted=list_acc[0]
        list_acc[0]=list_acc[0][1:]
        hasAccWoVerion={fstring.split('.')[0]:fstring for fstring in list_acc}
        #accesions without the version as keys and accesionwith version as values
        key_in_prot_headers=False
        taxa=False
        for accWoVersion in hasAccWoVerion:
            if accWoVersion in has:
                key_in_prot_headers=hasAccWoVerion[accWoVersion]
                taxa=has[accWoVersion]
                break
        if key_in_prot_headers:
            counter+=1
            fout.write('>%s_%s\n%s\n'%(key_in_prot_headers,taxa,"".join(val).strip()))
        else:
            taxa_unknown+=[eleTobeExcepted]
        val=[]
        key=''
        return [key,val,counter,taxa_unknown]

def subsetMultifasta(inpfile, hasAcc, outfile):
    notaxa_list=[]
    counter=0
    bar=Bar('reading_nr',max=274384441)
    fout=open (outfile,'w')
    with open(inpfile) as fin:
        key=''
        val=[]
        for line in fin:
            if line[0]=='>':
                if key and val:
                    bar.next()
                    key,val,counter,notaxa_list = writeFilefasta(key,val,fout,hasAcc,counter,notaxa_list)
                key=line
            else:
                val+=[line]
        if key and val:
            bar.next()
            key,val,counter,notaxa_list = writeFilefasta(key,val,fout,hasAcc,counter,notaxa_list)
    bar.finish()
    fout.close()
    return [counter,notaxa_list]

inpfile='../dataset/nr_NCBI.faa'
AccFile='../dataset/prot.accession2taxid'
hasAccLocal='../dataset/prot.accessionWoVersion2taxid.pickle'
if os.path.isfile(hasAccLocal):
    print('reading_pickle')
    hasAcc=read_pickle(hasAccLocal)
else:
    hasAcc=giveDict(AccFile)
    write_pickle(hasAccLocal,hasAcc)

'''
For every accession without verison the taxa is recirded as vallue there and saved for the whole prot.accession2.taxid file (tremendous)
'''

outfile='../dataset/kaiju_fullNR/nr_NCBI_completeAnnotatedWithTaxon.faa'
counter,notaxa_list=subsetMultifasta(inpfile,hasAcc,outfile)
print (counter)
print ('notaxa_found_for_%s_accessions: %s '%(len(notaxa_list),"\n".join(notaxa_list)))

