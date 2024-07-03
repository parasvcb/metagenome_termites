'''
After getting the resuts of metagene marks compiling it in t he dorection of contigs, theri length filters
'''
import sys
import common_modules as cm
if len(sys.argv)!=7:
    print ('Please give raw contig File, metageneMarksFile, Arthropod contigs, and results of Kaiju, megan, outfile')
    sys.exit()
prog,contig,metagenresults, arthropodFile, kaijuResults, Meganresuslts, outfileSumm=sys.argv

fileout=open (outfileSumm + 'kaiju_fraction_Grt300contigs','w') 

contigHas=cm.ReadContig()
kaijuHas=cm.parseKaiju()


with open (arthropodFile) as fin:
    ArthropodHas={i:0 for i in fin.read().split('\n') if len(i)>0}
print (len(ArthropodHas))
fileout.write('Total reads:%s\n'%(len(contigHas)))
fileout.write('Combined assesment using kaiju and megan for arthropods leads to %s reads\n'%(len(ArthropodHas)))

contigHasless300AfterArthropod={i:contigHas[i] for i in contigHas if contigHas[i][1]<300 and i not in ArthropodHas}
contigHasgrt300AfterArthropod={i:contigHas[i] for i in contigHas if contigHas[i][1]>=300 and i not in ArthropodHas}
fileout.write('\n\nFiltered contigs were %s, and %s were greater than or equal to 300 and %s were smaller than 300\n'%(len(contigHas)-len(ArthropodHas), len(contigHasgrt300AfterArthropod),len(contigHasless300AfterArthropod) ))

kaijuInterest={i:kaijuHas[i] for i in kaijuHas if i in contigHasgrt300AfterArthropod}

fileout.write('in these %s reads (grt 300), %s were characterized using kaiju against nr \n'%(len(contigHasgrt300AfterArthropod),len(kaijuInterest)))

lis=['Fungi','Metamonada','Bacteria','Eukaryota','Archaea','Others']
hastax_count={i:0 for i in lis}
for i in kaijuInterest:
    hastax_count[kaijuInterest[i]]+=1
fileout.write('among them follwing is the subclassifiaction %s \n'%(hastax_count))

with open (outfileSumm+'ContigIdsInterest(>300)_noOrfKnowledge.contigs','w') as fout:
    temp_has={i for i in contigHasgrt300AfterArthropod if i in kaijuHas and kaijuHas[i] in ['Bacteria','Archaea']}
    for i in temp_has:
            fout.write('>%s\n%s\n'%(i,contigHas[i][0]))
#above should be deleted if confusion arises

fileout.close()
#python bin/stats_aftermetageneMarksv2_kaiju_fraction_oncontigGrt300_level.py query/modified/contigs dataset/metageneMArks.stats.summ dataset/arthropod_kaiju_megan_nodeids dataset/kaiju_filterreads/Notarthropod ./ dataset/summary
# 335538 328009 528175
# 335538 328009 374075