import subprocess,time,sys,os,multiprocessing,tqdm
def update(a):
    pbar.update()
    
def blast(input_query_file,dblocation):
    #print (1)
    inputfile=os.path.join(inpdir,input_query_file)
    outfile=os.path.join(outdir,input_query_file+'.blastn')
    command='blastn_menten -db %s -query %s -out %s -outfmt 0 -evalue 0.001 -num_threads %s'%(dblocation, inputfile, outfile, cores)
    #print (command)
    if not os.path.isfile(outfile):
        subprocess.call([command],shell=True)
    return
    
if __name__ == "__main__":
    if len(sys.argv)!=6:
        print ('Please enter correct args dbloc,inpdir,outdir,cores,pools')
        sys.exit()

    prog,dbloc,inpdir,outdir,cores,pools =sys.argv
    iteration_count=3
    cores=int(cores)
    pools=int(pools)

    
    
    if 1:
        print ('inside')
        #now input source location is the inpdir_batch_loc
        target_files=os.listdir(inpdir)
        print (len(target_files),'length')
        pool = multiprocessing.Pool(processes=pools)
        pbar = tqdm.tqdm(total=len(target_files))
        st=time.time()
        for inst in target_files:
            pool.apply_async(blast, args=(inst, dbloc), callback=update)
        pool.close()
        pool.join()
        pbar.close()
        print (time.time()-st)
    else:
        print ('exiting on user demand')

