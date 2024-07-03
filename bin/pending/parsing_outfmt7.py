'''
# BLASTN 2.11.0+
# Query: NODE_1706734_length_215_cov_2.625
# Database: ../../common_db/ncbi_nt_26_jun21_fromncbi_ftpsite/nt
# 0 hits found
# BLASTN 2.11.0+
# Query: NODE_402343_length_452_cov_2.56675
# Database: ../../common_db/ncbi_nt_26_jun21_fromncbi_ftpsite/nt
# Fields: query id, query length, q. start, q. end, subject id, subject length, s. start, s. end, % identity, evalue, % positives, % query coverage per subject, bit score, gap opens, mismatches, alignment length, subject sci name, subject tax id
# 334 hits found
NODE_402343_length_452_cov_2.56675      452     2       444     gi|1830009471|gb|CP050966.1|    4817482 1345059 1345501 89.391  1.15e-154       89.39   98      558     0       47      443     N/A     2545798
'''
#' subject length',  subject id, ' % identity', ' evalue', ' % query coverage per subject',' alignment length',' subject sci name'
#

import subprocess,time,re,sys,os
if len(sys.argv)!=3:
    print ('Please enter correct cmd prog...py 1 inpdir 2outfile ')
    sys.exit()
prog, inpdir, outfile = sys.argv

flist=os.listdir(inpdir)

def update_has(final_has,fname):
    with open (fname) as fin:
        dat=fin.read().split('# BLASTN 2.11.0+')
    for chunk in dat:
        if len(chunk)>0:
            #print(chunk)
            hits=int(re.search('# \d+ hits found',chunk).group().split()[1])
            #print (hits)
            query=re.search(r'^# Query: .*$',chunk, flags=re.MULTILINE).group().split()[2]
            #print (query)
            
            if hits:
                fields=re.search(r'^# Fields: .*$',chunk, flags=re.MULTILINE).group().split(',')
                fields[0]=fields[0].split()[2]
                hfields={i:fields[i] for i in range (len(fields))}
                lines=[i for i in chunk.split('\n') if len(i)>0 and i[0]!='#']
                lis=[]
                for line in lines:
                    ele=line.split()
                    thas={hfields[i]:ele[i] for i in range(len(ele))}
                    lis+=[[thas[' % identity'],thas[' % query coverage per subject'],hits,thas ]]
                lisidenity=lis.copy()
                liscov=lis.copy()
            
                lisidenity.sort(key=lambda x: x[0])
                liscov.sort(key=lambda x: x[1])
                final_has[query]=[lisidenity[-1][-1], liscov[-1][-1], liscov[0][2]]
            else:
                final_has[query]=[]
    return final_has

def writeTofile(has,fname):
    print(len(has))
    keys=[' subject length', ' subject id',' % identity', ' evalue', ' % query coverage per subject',' alignment length',' subject sci name']
    string='query id\thits\tsubject length\tsubject id\t% identity\tevalue\t% query coverage per subject\talignment length\tsubject sci name\t\t\tsubject length\tsubject id\t% identity\tevalue\t% query coverage per subject\talignment length\tsubject sci name\n'
    fout2=open(fname+'NULL_entries.tsv','w')
    fout2.write(string)
    with open(fname,'w') as fout:
        fout.write(string)
        for i in has:
            query=i
            if has[i]:
                identity=has[i][0]
                cov=has[i][1]
                hits=has[i][2]
                idvals="\t".join([identity[i] for i in keys])
                covvals="\t".join([cov[i] for i in keys])
                fout.write('%s\t%s\t%s\t\t\t%s\n'%(query,hits,idvals,covvals))
            else:
                idvals="\t".join(['0']*7)
                covvals="\t".join(['0']*7)
                hits=0
                fout2.write('%s\t%s\t%s\t\t\t%s\n'%(query,hits,idvals,covvals))
    fout2.close()

has={}
for i in flist:
    fname=os.path.join(inpdir,i)
    has=update_has(has,fname)
    #break

writeTofile(has,outfile)