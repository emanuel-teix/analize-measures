import os

text="""#!/bin/bash 
#SBATCH -n 1 # Number of cores 
#SBATCH -N 1 # Number of nodes
#SBATCH -t 90-00:00 # Tempo limite de execucao (D-HH:MM)
#SBATCH -p long # Partition to submit to 
#SBATCH --qos qos_long # QOS 
####SBATCH --qos normal # QOS
./a.out {:10.6f} {:10.6f} {:10.6f} {:10.6f} {:10.6f} {:10.6f} {:10.6f} {:10.6f} {:10.6f} {:10.6f} {:10.6f} {:10.6f} {:10.6f} {:10.6f} {:10.6f} {:10.6f} {:10.6f} {:10.6f} {:10.6f}  
#echo  $V0 $DR $W $PHI $N $rc_ext $radh $ea $el $ec $eadh11 $eadh22 $eadh21 $eadh_base $p0_base $p01 $p02 $red_endo $green_ecto 
"""

V0 = [1.0]
DR = [1.0]
W = [0.0]
PHI = [0.1]
N = [400]
rc_ext = [2.0]
radh = [3.0]
ea = [1500.0]
el = [20.0]
ec = [20.0]
eadh11 = [1.0]
eadh22 = [1.0]
eadh21 = [1.0]
eadh_base = [0.0,2.0,3.5,4.0,4.5,5.0]
p01 = [1.0]
p02 = [1.0]
p0_base = [3.3,3.7,4.3]
red_endo = [2]
green_ecto = [2]

par=[]

for i1 in V0:
    for i2 in DR:
        for i3 in W:
            for i4 in PHI:
                for i5 in N:
                    for i6 in rc_ext:
                        for i7 in radh:
                            for i8 in ea:
                                for i9 in el:
                                    for i10 in ec:
                                        for i11 in eadh11:
                                            for i12 in eadh22:
                                                for i13 in eadh21:
                                                    for i14 in eadh_base:
                                                        for i15 in p0_base:
                                                            for i16 in p01:
                                                                for i17 in p02:
                                                                    for i18 in red_endo:
                                                                        for i19 in green_ecto:
                                                                            par.append([i1,i2,i3,i4,i5,i6,i7,i8,i9,i10,i11,i12,i13,i14,i15,i16,i17,i18,i19])	
														
for i in par:
	
	o=open('torun.scpt','w')
	o.write(text.format(*i))
	#o.write("#!/bin/bash \n")
	#o.write("#SBATCH -n 1 # Number of cores\n")
	#o.write("#SBATCH -N 1 # Number of nodes\n")
	#o.write("#SBATCH -t 03-00:00 # Tempo limite de execucao (D-HH:MM)\n")
	#o.write("#SBATCH -p short # Partition to submit to \n")
	#o.write("#SBATCH --qos qos_short # QOS\n")
	#o.write("./a.out %f %f %f %f %f %f %f\n"%(i[0],i[1],i[2],i[3],i[4],i[5],i[7]))
	o.close()	
	#os.system('sbatch torun.scpt')
        os.system('sbatch torun.scpt')



