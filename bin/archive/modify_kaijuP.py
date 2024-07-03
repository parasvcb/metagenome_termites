import sys
if len(sys.argv)!=2:
    print('Please enter correct args, 1.inputfile ')
    sys.exit()
prog,inp=sys.argv


'''
U	gene_34|GeneMark.hmm|70_aa|-|3|212
C	gene_361|GeneMark.hmm|70_aa|-|2|211	158	WP_187620355.1_2593411,TYZ19634.1_2593411,	
'''
with open (inp+'.taxaAdded','w') as fout:
    with open (inp) as fin:
        for i in fin:
            ele=i.strip().split()
            if len(ele)>0 and ele[0]=='C':
                taxa=ele[3].split(',')[0].split('_')[-1]
                fout.write('%s\n'%"\t".join(ele[:2]+[taxa]))
            else:
                fout.write('%s\t0\n'%(i.strip()))

    