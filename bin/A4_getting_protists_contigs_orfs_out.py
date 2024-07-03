'''
After getting the resuts of metagene marks compiling it in t he dorection of contigs, theri length filters
'''
import sys
import common_modules as cm
if len(sys.argv)!=6:
    print ('Please give raw contig File, metageneMarksSequqncesFile, Kaiju_classification_file_notarthropod, listOftagstoMtach, outfile')
    sys.exit()
prog,contig,metagenresults, kaijuFile, tagsFile, outfileSumm=sys.argv


with open (tagsFile) as fin:
    tags=[i.strip() for i in fin.read().split('\n') if len(i)>0]
kaijuHas=cm.parseKaiju(kaijuFile,tags)
kaijuHas={i:kaijuHas[i] for i in kaijuHas if kaijuHas[i]!='Others'}
#this will give all the contigs matching the given tags

contigHas=cm.ReadContig(contig)

contigHasForprotists={i:contigHas[i] for i in contigHas if i in kaijuHas}

with open (outfileSumm+'ContigNucSeq_protists_noOrfKnowledge.contigs','w') as fout:
    for i in contigHasForprotists:
        fout.write('>%s\n%s\n'%(i,contigHasForprotists[i][0]))

metageneHas=cm.ReadFasta(metagenresults,value='advanced')
print ('Contigs from kaiju were %s'%(len(contigHasForprotists)))

metageneInterest={i:metageneHas[i] for i in metageneHas if i in contigHasForprotists}
#has[key1]+=[(header,val)]
added=0
notadded=0
with open (outfileSumm+'OrfsInContigSeqAminoAcid_protists.faa','w') as fout:
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
#python bin/A4_getting_protists_contigs_orfs_out.py query/modified/contigs query/modified/predicted_genes.prot results/kaiju_filterreads/Notarthropod results/protists_genera results/