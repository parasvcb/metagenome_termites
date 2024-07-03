import os
import sys
if len(sys.argv)!=3:
    print ('Please enter correct cmd input query File, outputdir')
    sys.exit()
source,inpfile,outdir=sys.argv
def multifastaToFasta(filename, outdir,chunks):    
    def chunks(lst, n):
        # Yield successive n-sized chunks from lst. """
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    def writeFilefasta(key,val,lis):
        key=key.strip()
        lis+=[[key,"".join(val).strip()]]
        val=[]
        key=''
        return [lis,key,val]

    lis=[]

    with open(filename) as fin:
        key=''
        val=[]
        for line in fin:
            if line[0]=='>':
                if key and val:
                    lis,key,val = writeFilefasta(key,val,lis)
                key=line
            else:
                val+=[line]
        if key and val:
            lis,key,val = writeFilefasta(key,val,lis)
    
    chunks_lis=list(chunks(lis,5000))
    for i in range (0,len(chunks_lis)):
        fname=os.path.join(outdir,str(i+1)+'.chunk')
        with open (fname,'w') as fout:
            for j in chunks_lis[i]:
                
                fout.write('%s\n%s\n'%(j[0],j[1]))
    return

multifastaToFasta(inpfile,outdir,1000)
