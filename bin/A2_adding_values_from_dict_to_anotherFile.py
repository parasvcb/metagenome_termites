import sys,os
from itertools import combinations as cb
if len(sys.argv)!=4:

    print('Please emter correct args, 1.f1(having_keyIDpair) 2 fileThatNeedsColumn 3 outfile')
    sys.exit()
prog, classFile, genFile,outfile=sys.argv

lis_gen=[]
with open (genFile) as fin:
    '''
    Gene_ID	HMM_Profile
    NODE_10014_length_4451_cov_4.55027:::gene_120077|GeneMark.hmm|319_aa|+|3495|4451	GH13.hmm
    NODE_100357_length_1097_cov_8.66411:::gene_63805|GeneMark.hmm|289_aa|-|2|868	AA4.hmm
    NODE_100373_length_1096_cov_2.63593:::gene_256595|GeneMark.hmm|345_aa|+|1|1038	GH10.hmm
    '''
    datPrimary = [i for i in fin.read().split('\n')[1:] if len(i)>0]
    dictPrimary = {i.split()[0].split(':::')[0]: i.split()[1] for i in datPrimary}


with open (classFile) as fin:
    '''
    query   taxid   classification
    NODE_3512_length_7431_cov_7.43181       51160   cellular organisms;Bacteria;Spirochaetes;Spirochaetia;Spirochaetales;Spirochaetaceae;Treponema;
    NODE_423380_length_439_cov_2.71354      150829  cellular organisms;Bacteria;Spirochaetes;Spirochaetia;Spirochaetales;Spirochaetaceae;Treponema;
    NODE_518596_length_392_cov_2.47478      398037  cellular organisms;Bacteria;FCB group;Bacteroidetes/Chlorobi group;Bacteroidetes;Chitinopha
    '''
    dictSecondary={i.split('\t')[0]: i.split('\t')[2] for i in fin.read().split('\n')[1:] if len(i)>0}

with open (outfile,'w') as fout:
    for i in datPrimary:
        contigId=i.split()[0].split(':::')[0]
        val=dictSecondary[contigId] if contigId in dictSecondary else 'NOT FOUND'
        fout.write('%s\t%s\n'%(i, val))


#python bin/A2_adding_values_from_dict_to_anotherFile.py results/kaiju_filterreads/kaiju_filetered_length300plus_classifiedwithcompleteTaxa_excludedbothMeganKaiju_NotArthropod_contig_wise_classification_kaiju_grt300 results/hmmer_results_raw.txt results/cazy_with_taxonomy_A2