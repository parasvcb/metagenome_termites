import subprocess,time,sys,os
if len(sys.argv)!=5:
    print ('Please enter correct cmd prog...py 1 blastp or blastx, 2 database_loc, 3 input_benchmakr_loc, 4 outputloc ')
    sys.exit()
prog, blasttype, db, inpdir, outdir = sys.argv

cores=[4,10,20,30]


filelis=['top10.faa','top50.faa','top100.faa','top500.faa','top1000.faa']
has_timings={}
for filen in filelis:
    for core in cores:
        print (core,filen)
        start=time.time()
        inpfile=os.path.join(inpdir,filen)
        out_f=os.path.join(outdir,filen+'.out')
        call_inst='%s -query %s -db %s -out %s -num_threads %s -evalue .001 -outfmt 10'%(blasttype, inpfile,db,out_f,core)
        print (call_inst)
        subprocess.call([call_inst],shell=True)
        has_timings['%s_%s'%(filen,core)]=(time.time()-start)/60
print (has_timings)
result_file=os.path.join(outdir,blasttype+'.stats')

with open (result_file,'w') as fout:
    keys=list(has_timings.keys())
    keys.sort()
    for i in keys:
        fout.write('%s\t%s\n'%(i,has_timings[i]))
        
        


