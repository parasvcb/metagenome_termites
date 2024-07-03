import sys,re,os, subprocess
import common_modules as cm
if len(sys.argv)!=6:
    print ("Please neter correct args 1 summary 2 outkaijudefaut 3. taxongroupname 4 outfile 5 temptaxonfolder")
    sys.exit()
prog, summary, default, groupname, outfile, taxafold=sys.argv



def writefile(has,combined_taxas,fnameIn,fnameOut):
    grt300=0
    
    set2=set()
    with open (fnameOut,'w') as fout:
        fout.write('query\ttaxid\tclassification\n')
        with open (default) as fin:
            dat=[i for i in fin.read().split('\n') if len(i)>0]
        #print (len(dat))
        for i in dat:
            ele=i.split()
            if ele[0]=='C':
                set2|=set([ele[2]])
                #print (i[2])
                # print (ele)
                # sys.exit()
                if ele[2] in has:
                    if int(ele[1].split('_')[3])>=300:
                        grt300+=1
                    fout.write('%s\t%s\t%s\n'%(ele[1],ele[2],has[ele[2]]))
                if ele[2] not in combined_taxas:
                    unknown+=1
    print(grt300)
    return set2

'''
#summary
file	percent	reads	taxon_id	taxon_name
outkaiju_nr_Full_withoutAparam	7.832912	145061	157	cellular organisms;Bacteria;Spirochaetes;Spirochaetia;Spirochaetales;Spirochaetaceae;Treponema;
outkaiju_nr_Full_withoutAparam	1.750217	32413	156973	cellular organisms;Bacteria;FCB group;Bacteroidetes/Chlorobi group;Bacteroidetes;Bacteroidia;Bacteroidales;Dysgonomonadaceae;Dysgonomonas;
outkaiju_nr_Full_withoutAparam	1.452475	26899	
#5074

#outkaiju
U	NODE_205479_length_689_cov_3.36278	0
U	NODE_248599_length_609_cov_2.20758	0
U	NODE_378494_length_469_cov_1.64734	0
#35915
'''

with open (summary) as fin:
    dat=[ i for i in fin.read().split('\n')[1:] if len(i) >0]

has_groupname={}
has_else={}
#above two hashes will have the taxid (genera level) as key and their classification as value

for i in dat:
    ele=i.split('\t')
    if groupname.upper() in i or groupname.lower() in i or groupname.title() in i:
        has_groupname[ele[3].strip()]=ele[4]
    else:
        has_else[ele[3].strip()]=ele[4]

print (len(has_groupname))
has_groupname=cm.replaceTaxidToKids(taxafold,has_groupname)
print (len(has_groupname),'arthropod_done')
print (len(has_else))
has_else=cm.replaceTaxidToKids(taxafold,has_else)
print (len(has_else),'else_done')


combined_taxas={i:0 for i in list(has_groupname.keys())+list(has_else.keys())}
print ('interest')
set2=writefile(has_groupname,combined_taxas,default,outfile+'%s'%groupname)
print ('else')
set2=writefile(has_else,combined_taxas,default,outfile+'Not%s'%groupname)



#python bin/P3-kaijuSec__filtering_taxogroups_into2.py dataset/kaiju_summary_fullNR.tsv dataset/outkaiju_nr_Full_withoutAparam arthropod results/kaiju_filterreads/ dataset/taxonkit_temp
