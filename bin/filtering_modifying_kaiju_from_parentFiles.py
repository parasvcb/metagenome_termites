import sys,re,os, subprocess
import common_modules as cm
if len(sys.argv)!=6:
    print ("Please neter correct args 1 summary 2 outkaijudefaut 3. excluded_list(arthropods) 4 outfile 5 temptaxonfolder")
    sys.exit()
prog, summary, default, nonArthropodFile, outfile, taxafold=sys.argv
'''
#summary
file	percent	reads	taxon_id	taxon_name
outkaiju_nr_Full_withoutAparam	7.832912	145061	157	cellular organisms;Bacteria;Spirochaetes;Spirochaetia;Spirochaetales;Spirochaetaceae;Treponema;
outkaiju_nr_Full_withoutAparam	1.750217	32413	156973	cellular organisms;Bacteria;FCB group;Bacteroidetes/Chlorobi group;Bacteroidetes;Bacteroidia;Bacteroidales;Dysgonomonadaceae;Dysgonomonas;
outkaiju_nr_Full_withoutAparam	1.452475	26899	
#5074
'''
'''
#outkaiju
U	NODE_205479_length_689_cov_3.36278	0
U	NODE_248599_length_609_cov_2.20758	0
U	NODE_378494_length_469_cov_1.64734	0
#35915
'''
with open (nonArthropodFile) as fin:
    nonArthropodHas={i:0 for i in fin.read().split('\n') if len(i)>0}

print (len(nonArthropodHas),'arthropdContigs')
def writefile(has,has_classified,fnameIn,fnameOut):
    classified=0 
    involved=0   
    set2=set()
    print (fnameOut,'OUT')
    with open (fnameOut,'w') as fout:
        fout.write('query\ttaxid\tclassification\n')
        for i in has_classified:
            taxa=has_classified[i]
            if taxa in has:
                #print ('yes')
                fout.write('%s\t%s\t%s\n'%(i,taxa,has[taxa]))
    return set2


count_length=0
count_class=0
count_both=0
has_classified={}
with open (default) as fin:
    default_dat=[i for i in fin.read().split('\n') if len(i)>0]
    for i in default_dat:
        #i is U	NODE_378494_length_469_cov_1.64734	0
        ele=i.split()
        tag,nodeid,taxa=ele
        if nodeid not in nonArthropodHas:
            length=int(ele[1].split('_')[3])
            f1=0
            f2=0
            if length>=300:
                count_length+=1
                f1=1
            if ele[0]=='C':
                f2=1
                count_class+=1
            if f1 and f2:
                count_both+=1
                has_classified[nodeid]=taxa


print ('count_total=%s,count_lengthgrt300=%s,count_classified=%s,count_classified_and_grt300=%s'%(len(default_dat),count_length,count_class,count_both))


def writefile_kraken_summary_copy(has,has_classified,fnameIn,fnameOut):
    #has contains tax level species as key and classification till genera
    #has_classified conains species level taxid as value and nodeid as key
    print (len(has),len(has_classified))
    count_written=0
    count_cumulative=0
    has_total={}
    for i in has_classified:
        taxa=has_classified[i]
        if taxa in has:
            classi=has[taxa]
            if classi not in has_total:
                has_total[classi]=0
            has_total[classi]+=1
    
    total=sum(list(has_total.values()))
    print (total,'contigs considered, cumulative phyla"s were ' ,len(has_total) )
    has_total_fraction={i:(has_total[i],round(has_total[i]/total,3)) for i in has_total}
    #above has key as classification
    done_already={}
    print ('contigs_record_written:%s'%(len(has_total_fraction)))
    with open (fnameOut,'w') as fout:
        fout.write('totalReads\tfraction\tclassification\n')
        for i in has_total_fraction:
            class_detail=i
            total,frac=has_total_fraction[i]
            fout.write('%s\t%s\t%s\n'%(total,frac,class_detail))
    

def update_summ_has(has,key,val):
    has[key]=val
    return has

with open (summary) as fin:
    dat=[ i for i in fin.read().split('\n')[1:] if len(i) >0]
#recording the lines with positive length

has_else={}
#print (len(dat))
set1=set()

for i in dat:
    ele=i.split('\t')
    has_else=update_summ_has(has_else,key=ele[3].strip(),val=ele[4])

#has else has genus level taxid as key and then the calssification as string

# here i secured all the taxonIds's from summary file (keys) and recorded their trajectory in the value
# same taxon ID is there in the case of the viruses and the unclassified category and i have done the follwing, made the values a list and appended the information there
print (len(has_else),'length else and interest')
has_else=cm.replaceTaxidToKids(taxafold,has_else)
print (len(has_else),'length else and interest2')
#this now has species level taxid as key, and same string as new key

groupname='Arthropod'
writefile(has_else,has_classified, default,outfile+'kaiju_filetered_length300plus_classifiedwithcompleteTaxa_excludedbothMeganKaiju_Not%s_contig_wise_classification_kaiju_grt300'%groupname)
writefile_kraken_summary_copy(has_else,has_classified, default,outfile+'kaiju_filetered_length300plus_classifiedwithcompleteTaxa_excludedbothMeganKaiju_Not%s_summary_kaiju_grt300'%groupname)


#python bin/filtering_modifying_kaiju_from_parentFiles.py dataset/kaiju_summary_fullNR.tsv dataset/outkaiju_nr_Full_withoutAparam arthropod results/kaiju_filterreads/ dataset/taxonkit_temp
#python bin/filtering_modifying_kaiju_from_parentFiles.py dataset/kaiju_summary_fullNR.tsv dataset/outkaiju_nr_Full_withoutAparam dataset/arthropod_kaiju_megan_nodeids results/kaiju_filterreads/ dataset/taxonkit_temp