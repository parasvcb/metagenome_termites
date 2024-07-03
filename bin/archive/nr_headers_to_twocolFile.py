headers_nr='../dataset/nr_NCBI.faa.headers'
headers_nr_test='../dataset/head_nr_NCBI.faa.headers'
twocolfile='../results/nr_headers_twocol'
from progress.bar import Bar
import subprocess

subprocess.check_output(['head -10000 '+headers_nr + ' > '+headers_nr_test],shell=True)
headers_nr_test=headers_nr
#commnet above to test
num_lines = subprocess.check_output(['wc','-l',headers_nr_test]).decode().split()[0]
print (num_lines)
bar=Bar('processing:',max=int(num_lines)) 
with open (twocolfile,'w') as fout:
    with open (headers_nr_test) as fin:
        for record in fin:
            bar.next()
            record_mod=record.strip()
            ele=[i for i in record_mod.split(']') if len(i)>0]
            primkey=ele[0][1:].split()[0]
            primval=ele[0][1:].split()[0]
            fout.write('%s\t%s\n'%(primkey,primval))
            if len(ele)>1:
                for i in ele[1:]:
                    #print (ele)
                    #val=i.split()[0].strip()
                    #val=i.split()[0].replace('^A','')
                    val=''.join(e for e in i.split()[0] if e.isalnum())
                    fout.write('%s\t%s\n'%(primkey,val))
bar.finish()
#add progress bar to above, 
#match its second column to the accession list


'''
ile1:

AT1G56430
AT3G55190
AT3G22880

file2:

AT1G01010|GO:0043090|RCA
AT1G56430|GO:0010233|IGI 
AT1G56430|GO:0009555|IGI 
AT1G56430|GO:0030418|IGI

expected output

AT1G56430|GO:0010233|IGI 
AT1G56430|GO:0009555|IGI 
AT1G56430|GO:0030418|IGI

awk -F',' 'NR==FNR{primkey[$2]=$1;val[$2]=$2;next}; ($1==val[$1]){print primkey[$1] "," val[$1]}' test.nr_headers_twocol1 test.pattern1
Above command will work hurray
'''
