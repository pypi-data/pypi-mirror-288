

for i in range(1, 73):

    cmd = 'srun -n 1 python3 00_DataNeeded/BLCA/2.blca_main.py -x -p 1 -r 00_DataNeeded/db_GTDB214.1/ssu_all_r214_BLCAparsed.taxonomy -q 00_DataNeeded/db_GTDB214.1/ssu_all_r214_BLCAparsed.fasta -i b_rep_set_%s.fa -o b_rep_set_%s_BLCA_out.1.txt &' % (i, i)
    print(cmd)
