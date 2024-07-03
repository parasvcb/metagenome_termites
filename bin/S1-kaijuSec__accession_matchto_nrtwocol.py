'''
Tihs progra will take combined accession file with taxid listed in sep col,
every record accezion (1st col) will be mathed against two col file, (read that as hash), second col as key, first as val,
if match, will write val, and taxid in file
'''
import sys
combined_acc='../dataset/taxa_wise_accessions_taxonkit/combined_acc2ttaxid'
#this is a file having accessions from taxa_10239/          taxa_1912919/        taxa_2/              taxa_2157/           taxa_2611341/
twocolfile='../results/nr_headers_twocol'
# the above file contains these many entries 489036027
subsetFile='../results/nr_headers_subsetneeded_withtax'
def giveDict(fname):
    print ('here')
    has={}
    with open (fname) as fin:
        for i in fin:
            try:
                ele=i.strip().split()
                has[ele[1]]=ele[0]
            except:
                pass
    print (len(has),'keys_has')
    return has

from progress.bar import Bar
import subprocess

num_lines = subprocess.check_output(['wc','-l',combined_acc]).decode().split()[0]
print (num_lines,'numlines')

dictTwocol=giveDict(twocolfile)
#saving all the accessions as keys and their taxids as values

bar=Bar('processing:',max=int(num_lines)) 
with open (subsetFile,'w') as fout:
    with open (combined_acc) as fin:
        for record in fin:
            bar.next()
            record_mod=record.strip()
            if len(record_mod)>0:
                acc,tax=record_mod.split()
                if acc in dictTwocol:
                    fout.write('%s\t%s\n'%(dictTwocol[acc],tax))
bar.finish()
