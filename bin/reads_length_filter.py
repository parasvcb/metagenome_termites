import sys,re,os, subprocess
if len(sys.argv)!=4:
    print ("Please neter correct args 1 f1 2 f2 3outfile")
    sys.exit()
prog, f1,f2, out1=sys.argv

def readfile(fname):
    with open (fname) as fin:
        dat=[i for i in fin.read().split('\n')[1:] if len(i)>0]
    return dat

l1=readfile(f1)
l2=readfile(f2)

l=l1+l2

'''
NODE_26658_length_2529_cov_6.77688	2668072	cellular organisms;Archaea;Euryarchaeota;Stenosarchaea group;Halobacteria;Haloferacales;Halorubraceae;Halorubrum;
NODE_1420943_length_235_cov_2.07778	47311	cellular organisms;Archaea;Euryarchaeota;Methanomada group;Methanobacteria;Methanobacteriales;Methanobacteriaceae;Methanobrevibacter;
NODE_1267460_length_248_cov_0.974093	2207	cellular organisms;Archaea;Euryarchaeota;Stenosarchaea group;Methanomicrobia;Methanosarcinales;Methanosarcinaceae;Methanosarcina;
NODE_620333_length_356_cov_4.4186	54261	cellular organisms;Archaea;Euryarchaeota;Archaeoglobi;Archaeoglobales;Archaeoglobaceae;Ferroglobus;
NODE_1339420_length_242_cov_11.369	1638221	cellular organisms;Archaea;Euryarchaeota;Thermococci;Thermococcales;Thermococcaceae;Thermococcus;
NODE_660960_length_344_cov_1.6436	2234	cellular organisms;Archaea;Euryarchaeota;Archaeoglobi;Archaeoglobales;Archaeoglobaceae;Archaeoglobus;
'''
has={}
with open (out1,'w') as fout:
    fout.write('query\ttaxid\tclassification\ttag\n')
    for i in l:
        ele=i.split()
        length=int(ele[0].split('_')[3])
        if length>=300:

            match='Archaea' if 'Archaea' in i else 'Fungi' if 'Fungi' in i else 'Metamonada' if 'Metamonada' in i else 'Bacteria' if 'Bacteria' in i else 'Arthropoda' if 'Arthropoda' in i else 'Others'
            
            fout.write('%s\t%s\n'%(i,match))
        else:
            match='shorterReads'       
        
        if match not in has:
            has[match]=0
        has[match]+=1

for i in has:
    print (i,has[i],has[i]/sum(list(has.values())))

    
