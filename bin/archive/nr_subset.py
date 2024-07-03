'''
take the file having nr first accesion and taxid as tab separated values.
read the nr fasta on your own, if match, modify the header from dict above and write
dict matches should be 169158570
'''
def giveDict(fname):
    print ('here')
    has={}
    with open (fname) as fin:
        for i in fin:
            try:
                ele=i.strip().split()
                has[ele[0]]=ele[1]
            except:
                pass
    print (len(has),'keys_has')
    return has

def subsetMultifasta(inpfile, hasAcc, outfile):
    def writeFilefasta(key,val,fout,has,counter):
        fstring=key.split()[0][1:].strip()
        if fstring in has:
            counter+=1
            fout.write('>%s_%s\n%s\n'%(fstring,has[fstring],"".join(val).strip()))
        val=[]
        key=''
        return [key,val,counter]
    counter=0
    fout=open (outfile,'w')
    with open(inpfile) as fin:
        key=''
        val=[]
        for line in fin:
            if line[0]=='>':
                if key and val:
                    key,val,counter = writeFilefasta(key,val,fout,hasAcc,counter)
                key=line
            else:
                val+=[line]
        if key and val:
            key,val,counter = writeFilefasta(key,val,fout,hasAcc,counter)
    fout.close()
    return counter

inpfile='../dataset/nr_NCBI.faa'
hasAccFile='../results/nr_headers_subsetneeded_withtax'
# this is a file with the accessionwitheversion as 1st col and taxid as 2nd
hasAcc=giveDict(hasAccFile)
#store the accessionwithversion as key and taxid as value 
outfile='../dataset/nr_NCBI_subset.faa'
counter=subsetMultifasta(inpfile,hasAcc,outfile)
print (counter)

# the program was ran through the metagen server(2.94) and contents of the files were 
'''
#nr_NCBI.faa
>KJX92028.1 hypothetical protein TI39_contig5958g00003 [Zymoseptoria brevis]
MAWTRQLVPLMLLFCGAHGLQRSSTATDQLSNSALQALGSHADLAAFVNDVEAVPEIANVILAHRGITIMAPVDSAWLRV
DAIKRRNPAFLAWHIMNANVLTSDVPLVQYEQHPGITIPTFLSGSKNWTYSGEPASLISGGQSLTAITLKTEDNVIWVSG
ASNVSYIKQANISYDRGIIHKIDPALQFPTSAYETAFAVGLYSYCWAVFTAGLDQEIRRIPNSTFLLPINEAFHAALPFL
LGASREEFKRIVYRHVIPGRVLWSHEFYNASHETFEGSIVQIRGGNGRRWFVDDAMILDGSDKPLYNGVGHVVNKVLLPT
>EFG1759503.1 decarboxylating NADP(+)-dependent phosphogluconate dehydrogenase [Escherichia coli]EGJ4377881.1 decarboxylating NADP(+)-dependent phosphogluconate dehydrogenase [Escherichia coli]
LKPYLDKGDIIIDGGNTFFQDTIRRNRELSAEGFNFIGTGVSGGEEGALKGPSIMPGGQKEAYELVAPILTKIAAVAEDG
EPCVTYIGADGAGHYVKMVHNGIEYGDMQLIAEAYSLLKGGLNLTNEELAQTFTEWNNGELSSYLIDITKDIFTKKDEDG
NYLVDVILDEAANKGTGKWTSQSALDLGEPLSLITESVFARYISSLKEQRVAASKVLSGPQAQPAGDKGEFIEKVRRALY
LGKIVSYAQGFSQLRAASEEYNWDLNYGEIAKIFRAGCIIRAQFLQKITDAYIENPQIANLLLAPYFKQIADNYQQALRE


(base) [ph15040@jbod dataset]$ head ../results/nr_headers_*
==> ../results/nr_headers_subsetneeded_withtax <==
A0A024B7W1.1	2043570
A0A0U5AF03.1	1772250
A0A142I5B9.1	2316109
A0A1L4BKP6.1	1406341
A0A1L4BKS3.1	1406341
A0MD28.2	857306
A0MD31.1	857306
A0MD32.1	857306
A0MD33.1	857306
A0MD35.1	857306

==> ../results/nr_headers_twocol <==
KJX92028.1	KJX92028.1
EFG1759503.1	EFG1759503.1
EFG1759503.1	EGJ43778811
WP_198835266.1	WP_198835266.1
WP_198835266.1	MBJ21496271
MBD3193859.1	MBD3193859.1
MBD3193859.1	MBD31987411
PYI97175.1	PYI97175.1
PYI97175.1	PYJ338621
WP_137987990.1	WP_137987990.1
(base) [ph15040@jbod dataset]$ wc -l ../results/nr_headers_*
  169158570 ../results/nr_headers_subsetneeded_withtax
  489036027 ../results/nr_headers_twocol
  658194597 total
(base) [ph15040@jbod dataset]$ 


#nr_headers_subsetneeded_withtax was created from the bin/1-kaijuSec__accession_matchto_nrtwocol.py
# read all the combined proteins repository from the taxa of choosen organizsms (),
#filtered every such entry such that the 


'''

