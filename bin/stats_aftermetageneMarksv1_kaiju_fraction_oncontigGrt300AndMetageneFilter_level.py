'''
After getting the resuts of metagene marks compiling it in t he dorection of contigs, theri length filters
'''
import sys
if len(sys.argv)!=6:
    print ('Please give raw contig File, metageneMarksFile, Arthropod contigs, and results of Kaiju, megan, outfile')
    sys.exit()
prog,contig,metagenresults, nonArthropodFile, kaijuResults, Meganresuslts, outfileSumm=sys.argv

fileout=open (outfileSumm+'kaiju_fraction_onMetageneMarksGrt300contigs','w') 

contigHas=cm.ReadContig(contig)
kaijuHas=cm.parseKaiju(kaijuResults)    
metageneHas=cm.parsing_metagenemarkTo3tags(metagenresults)

with open (nonArthropodFile) as fin:
    nonArthropodHas={i:0 for i in fin.read().split('\n') if len(i)>0}

fileout.write('Total reads:%s\n'%(len(contigHas)))
fileout.write('Combined assesment using kaiju and megan Only for arthropods leads to %s reads\n'%(len(nonArthropodHas)))

contigHasless300AfterArthropod={i:contigHas[i] for i in contigHas if contigHas[i][1]<300 and i not in nonArthropodHas}
contigHasgrt300AfterArthropod={i:contigHas[i] for i in contigHas if contigHas[i][1]>=300 and i not in nonArthropodHas}
fileout.write('\n\nFiltered contigs were %s, and %s were greater than or equal to 300 and %s were smaller than 300\n'%(len(contigHas)-len(nonArthropodHas), len(contigHasgrt300AfterArthropod),len(contigHasless300AfterArthropod) ))

metageneInterest={i:metageneHas[i] for i in metageneHas if i in contigHasgrt300AfterArthropod}


fileout.write('\n Among %s grt than 300 contigs, %s does have orfs associated\n'%(len(contigHasgrt300AfterArthropod), len(metageneInterest)))

temp1=sum([1 for i in metageneInterest if metageneInterest[i]==1])
temp0=sum([1 for i in metageneInterest if metageneInterest[i]==0])
temp2=sum([1 for i in metageneInterest if metageneInterest[i]==2])
fileout.write('\n and in them %s were category 2 %s were category 1, %s were category 0\n'%(temp2,temp1,temp0))

kaijuInterest={i:kaijuHas[i] for i in kaijuHas if i in metageneInterest}

fileout.write('in these %s reads (with oRFS in metagene) %s were characterized using kaiju against nr \n'%(len(metageneInterest),len(kaijuInterest)))

lis=['Fungi','Metamonada','Bacteria','Eukaryota','Archaea','Others']
hastax={i:0 for i in lis}
for i in kaijuInterest:
    hastax[kaijuInterest[i]]+=1
fileout.write('among them follwing is the subclassifiaction %s \n'%(hastax))




#python bin/stats_aftermetageneMarks.py query/modified/contigs results/metageneMArks.summ dataset/arthropod_kaiju_megan_nodeids dataset/kaiju_filterreads/Notarthropod ./ dataset/summary