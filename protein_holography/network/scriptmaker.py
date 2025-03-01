import datetime
import os

date = datetime.date.today()

throwaway_script = 'batch_script.slurm'
group = 'spe'

k_vals = [0.0001]
l_vals = [6]
d_vals = [10.0]

for k in k_vals:
    for l in l_vals:
        for d in d_vals:
            f = open(throwaway_script,'w')
            job_name = 'train_hgram_l='+str(l)+'_k='+str(k)+'_d='+str(d)
            f.write("#!/bin/bash\n\
## Job Name\n\
#SBATCH --job-name="+job_name+'_'+str(date)+'\n\
## Allocation Definition\n\
## The account and partition options should be the same except in a few cases (e.g. ckpt queue and genpool queue).\n\
#SBATCH --account='+group+'\n\
#SBATCH --partition='+group+'\n\
## Resources\n\
## Total number of Nodes\n\
#SBATCH --nodes=1   \n\
## Number of cores per node\n\
#SBATCH --ntasks-per-node=20\n\
## Walltime (3 hours). Do not specify a walltime substantially more than your job needs.\n\
#SBATCH --time=10:00:00\n\
## Memory per node. It is important to specify the memory since the default memory is very small.\n\
## For mox, --mem may be more than 100G depending on the memory of your nodes.\n\
## For ikt, --mem may be 58G or more depending on the memory of your nodes.\n\
## See above section on "Specifying memory" for choices for --mem.\n\
#SBATCH --mem=10G\n\
## Specify the working directory for this jo\n\
#SBATCH --chdir=/gscratch/spe/mpun/hnn_tests\n\
##turn on e-mail notification\n\
#SBATCH --mail-type=ALL\n\
#SBATCH --mail-user=mpun@uw.edu\n\
## export all your environment variables to the batch job session\n\
#SBATCH --export=all\n\
#SBATCH -e '+job_name+'_'+str(date)+'.e\n\
#SBATCH -o '+job_name+'_'+str(date)+'.o\n\
\n\
cd /gscratch/spe/mpun/protein_holography/network\n\
python -u train.py \n')

            f.close()

            print('Submitting script')
            os.system('sbatch ' + throwaway_script)
            print('Deleting script')
            #os.system('rm ' +throwaway_script)

print('Program terminating succesfully')
