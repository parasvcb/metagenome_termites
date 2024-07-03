'''
After getting the resuts of metagene marks compiling it in t he dorection of contigs, theri length filters
'''
import sys
import common_modules as cm
if len(sys.argv)!=5:
    print ('Please give raw contig File, metageneMarksSequqncesFile, Kaiju_classification_file_notarthropod, outfile')
    sys.exit()
prog,contig,metagenresults, kaijuFile, outfileSumm=sys.argv


kaijuHas=cm.parseKaiju(kaijuFile)
#this will give all the contigs matching the given tags

contigHas=cm.ReadContig(contig)
contigHasInterest={i:contigHas[i] for i in contigHas if i not in kaijuHas}

with open (outfileSumm+'ContigNucSeq_UNCHARACTERIZED_noOrfKnowledge.contigs','w') as fout:
    for i in contigHasInterest:
        fout.write('>%s\n%s\n'%(i,contigHasInterest[i][0]))

metageneHas=cm.ReadFasta(metagenresults,value='advanced')
print ('Contigs not characterized from kaiju were %s'%(len(contigHasInterest)))

metageneInterest={i:metageneHas[i] for i in metageneHas if i in contigHasInterest}
#has[key1]+=[(header,val)]
added=0
notadded=0
with open (outfileSumm+'OrfsInContigSeqAminoAcid_UNCHHARACTERIZED.faa','w') as fout:
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
# python bin/A5_getting_nonchsracterized_contigs.py query/modified/contigs query/modified/predicted_genes.prot results/kaiju_filterreads/combined_arthnotarth results/
# Contigs not characterized from kaiju were 1237818
# contigs_having_ORFS were 702347
# length>=100 orfs were 261162, and less than were 559221