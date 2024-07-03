'''
After getting the resuts of metagene marks, compiling it in the direction of contigs, their length filters
'''
import sys
import common_modules as cm
if len(sys.argv)!=6:
    print ('Please give raw contig File, metageneMarksSequqncesFile, Arthropod contigs, megan, outfile')
    sys.exit()
prog,contig,metagenresults, arthropodFile, Meganresuslts, outfileSumm=sys.argv
#arthropodFile has combined contigs belonging to them using kaiju and megan

contigHas=cm.ReadContig(contig)
with open (arthropodFile) as fin:
    ArthropodHas={i:0 for i in fin.read().split('\n') if len(i)>0}
print (len(ArthropodHas))


contigHasForArthropod={i:contigHas[i] for i in contigHas if i in ArthropodHas}

with open (outfileSumm+'ContigNucSeq_arthropods_noOrfKnowledge.contigs','w') as fout:
    for i in contigHasForArthropod:
        fout.write('>%s\n%s\n'%(i,contigHasForArthropod[i][0]))

metageneHas=cm.ReadFasta(metagenresults,value='advanced')
print ('Contigs from blast and kaiju were %s'%(len(contigHasForArthropod)))

metageneInterest={i:metageneHas[i] for i in metageneHas if i in contigHasForArthropod}
#has[key1]+=[(header,val)]
added=0
notadded=0
with open (outfileSumm+'OrfsInContigSeqAminoAcid_arthropods.faa','w') as fout:
    for i in metageneInterest:
        for j in metageneInterest[i]:
            contig,seq=j
            headerOrf=i
            if len(seq)>=100:
                added+=1
                fout.write('>%s\n%s\n'%(contig+':::'+headerOrf,seq))
            else:
                notadded+=1
print ('contigs_having_ORFS from blast and kaiju were %s'%(len(metageneInterest)))
print ('length>=100 orfs were %s, and less than were %s'%(added,notadded))
#python bin/stats_aftermetageneMarksv2_kaiju_fraction_oncontigGrt300_level.py query/modified/contigs query/modified/predicted_genes.prot dataset/arthropod_kaiju_megan_nodeids dataset/kaiju_filterreads/Notarthropod ./ dataset/summary