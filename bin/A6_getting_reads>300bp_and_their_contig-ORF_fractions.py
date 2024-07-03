
import sys,os
import common_modules as cm
if len(sys.argv)!=6:
    print ('Please give raw contig File, metageneMarksSequqncesFile, Kaiju_classification_file_notarthropod, listOftagstoMtach or tags, outfile')
    sys.exit()
prog,contig,metagenresults, kaijuFile, tagsFile, outfileSumm=sys.argv

if os.path.isfile(tagsFile):
    with open (tagsFile) as fin:
        tags=[i.strip() for i in fin.read().split('\n') if len(i)>0]
    tagName='protists'
else:
    tags=[tagsFile]
    tagName=tags
kaijuHas=cm.parseKaiju(kaijuFile,tags)
print (set(kaijuHas.values()))

kaijuHas={i:kaijuHas[i] for i in kaijuHas if kaijuHas[i]!='Others'}
#this will give all the contigs matching the given tags

contigHas=cm.ReadContig(contig)

contigHasForGroupInterest={i:contigHas[i] for i in contigHas if i in kaijuHas and contigHas[i][1]>=300}

with open (outfileSumm+'%s_noOrfKnowledge_grteq100.contigs'%tagName,'w') as fout:
    for i in contigHasForGroupInterest:
        fout.write('>%s\n%s\n'%(i,contigHasForGroupInterest[i][0]))

metageneHas=cm.ReadFasta(metagenresults,value='advanced')
print ('Contigs from kaiju were %s'%(len(contigHasForGroupInterest)))

metageneInterest={i:metageneHas[i] for i in metageneHas if i in contigHasForGroupInterest}
#has[key1]+=[(header,val)]
added=0
notadded=0
with open (outfileSumm+'%s_OrfsInContigsgrteq300AminoAcid.faa'%tagName,'w') as fout:
    for i in metageneInterest:
        for j in metageneInterest[i]:
            contig,seq=j
            headerOrf=i
            if len(seq)>=100:
                added+=1
                fout.write('>%s\n%s\n'%(contig+':::'+headerOrf,seq))
            else:
                notadded+=1
print ('contigs_having_ORFS were %s'%(len(metageneInterest)))
print ('length>=100 orfs were %s, and less than were %s'%(added,notadded))
#python bin/A6_getting_reads\>300bp_and_their_contig-ORF_fractions.py query/modified/contigs query/modified/predicted_genes.prot results/kaiju_filterreads/Notarthropod results/protists_genera results/
