#!/usr/bin/python
'''
This script generates IETsim input files from a DFTB conformation scan output.
It also generates submission scripts for each IETsim calculation, and an input 
stream file to submit all the jobs at once. 
'''

#-----------------USER INPUT SECTION-----------------!
cluster='henry'                 # henry, murgas
queue='single_chassis'          # name of queue
complex='biCA_slab_'            # complex name
steps='4000.0'                  # simulation steps
cube=False                      # generate cube file?
#----------------------------------------------------!

import sys
import os
import shutil as sh
import subprocess


# generate submission scripts
def gen_subscript(cluster,queue,conf,state):
    sfile='subdynamics_'+complex+conf
    if cluster == 'henry':
        subtext='\
#!/usr/bin/bash\n\
#BSUB -R "model != L5535"\n\
#BSUB -R span[ptile=8]\n\
#BSUB -R "mem>16100"\n\
#BSUB -q '+queue+'\n\
#BSUB -n 2\n\
#BSUB -W 96:00\n\
#BSUB -J '+conf+'_'+state+'\n\
#BSUB -o output\n\
#BSUB -e error\n\
\n\
echo jobid = $LSB_JOBID\n\
echo hosts = $LSB_HOSTS\n\
\n\
date\n\
dynamics '+conf+'.bind\n\
date\n\n' 

    if cluster == 'murgas':                                             
        subtext='\
#!/bin/bash\n\
#These commands set up the Grid Environment for your job:\n\
#PBS -jeo\n\
#PBS -o output\n\
#PBS -e error\n\
#PBS -N '+conf+'_'+state+'\n\
#PBS -l pmem=2GB,nodes=1:ppn=1,walltime=300:00:00\n\
#########\n\
\n\
RUNDIR=$PBS_O_WORKDIR\n\
export RUNDIR\n\
cd $RUNDIR\n\
\n\
date\n\
dynamics '+conf+'.bind\n\
date\n\n'
    
    with open(sfile,'w') as fo:
        fo.write(subtext)
    os.chmod(sfile,0755)


# generate bottom of bind file depending on the complex
def make_bottomBind(bindmode,stpes,cube):
    # add cube keyword if needed
    if cube == True:
        cubedyn='\
Cube\n\n'
    if cube == False:
        cubedyn=''

    # dynamics section
    dynamics='\
Dynamics\n\
0.1 '+steps+'\n\n'

    # occupation + absorption potential
    if 'biCA' in bindmode:
        occ='\
Occupation\n\
865\n\
1,2-865\n\n'
        abspot='\
Absorbing\n\
432 0.100\n\
161, 162, 163, 164, 165, 166, 167, 168, 169, 170   \ \n\
171, 172, 173, 174, 175, 176, 177, 178, 179, 180   \ \n\
181, 182, 183, 184, 185, 186, 187, 643, 644, 645   \ \n\
646, 647, 648, 649, 650, 651, 652, 653, 654, 655   \ \n\
656, 657, 658, 659, 660, 661, 662, 663, 664, 665   \ \n\
666, 667, 668, 669, 670, 671, 672, 673, 674, 675   \ \n\
676, 677, 678, 679, 680, 681, 682, 683, 684, 685   \ \n\
686, 687, 688, 689, 690, 691, 692, 693, 694, 695   \ \n\
696, 1575, 1576, 1577, 1578, 1579, 1580, 1581, 1582, 1583   \  \n\
1584, 1585, 1586, 1587, 1588, 1589, 1590, 1591, 1592, 1593   \ \n\
1594, 1595, 1596, 1597, 1598, 1599, 1600, 1601, 1602, 1603   \ \n\
1604, 1605, 1606, 1607, 1608, 1609, 1610, 1791, 1792, 1793   \ \n\
1794, 1795, 1796, 1797, 1798, 1799, 1800, 1801, 1802, 1803   \ \n\
1804, 1805, 1806, 1807, 1808, 1809, 1810, 1811, 1812, 1813   \ \n\
1814, 1815, 1816, 1817, 1818, 1819, 1820, 1821, 1822, 1823   \ \n\
1824, 1825, 1826, 1827, 1828, 1829, 1830, 1831, 1832, 1833   \ \n\
1834, 1835, 1836, 1837, 1838, 1839, 1840, 1841, 1842, 1843   \ \n\
1844, 1845, 1846, 1847, 1848, 1849, 1850, 1851, 1852, 1853   \ \n\
1854, 1855, 1856, 1857, 1858, 1859, 1860, 1861, 1862, 1863   \ \n\
1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 3494, 3495   \ \n\
3496, 3497, 3498, 3499, 3500, 3501, 3502, 3503, 3504, 3505   \ \n\
3506, 3507, 3508, 3509, 3510, 3511, 3512, 3513, 3514, 3515   \ \n\
3516, 3517, 3518, 3519, 3520, 3521, 3522, 3523, 3524, 3525   \ \n\
3526, 3527, 3528, 3529, 3530, 3531, 3532, 3533, 3534, 3535   \ \n\
3536, 3537, 3538, 3539, 3540, 3541, 3542, 3543, 3544, 3545   \ \n\
3546, 3547, 3548, 3549, 3550, 3551, 3552, 3553, 3554, 3555   \ \n\
3556, 3557, 3558, 3559, 3560, 3561, 3562, 3563, 3564, 3565   \ \n\
3926, 3927, 3928, 3929, 3930, 3931, 3932, 3933, 3934, 3935   \ \n\
3936, 3937, 3938, 3939, 3940, 3941, 3942, 3943, 3944, 3945   \ \n\
3946, 3947, 3948, 3949, 3950, 3951, 3952, 3953, 3954, 3955   \ \n\
3956, 3957, 3958, 3959, 3960, 3961, 3962, 3963, 3964, 3965   \ \n\
3966, 3967, 3968, 3969, 3970, 3971, 3972, 3973, 3974, 3975   \ \n\
3976, 3977, 3978, 3979, 3980, 3981, 3982, 3983, 3984, 3985   \ \n\
3986, 3987, 3988, 3989, 3990, 3991, 3992, 3993, 3994, 3995   \ \n\
3996, 3997, 3998, 3999, 4000, 4001, 4002, 4003, 4004, 4005   \ \n\
4006, 4007, 4008, 4009, 4010, 4011, 4012, 4013, 4014, 4015   \ \n\
4016, 4017, 4018, 4019, 4020, 4021, 4022, 4023, 4024, 4025   \ \n\
4026, 4027, 4028, 4029, 4030, 4031, 4032, 4033, 4034, 4035   \ \n\
4036, 4037, 4038, 4039, 4040, 4041, 4042, 4043, 4044, 4045   \ \n\
4046, 4047, 4048, 4049, 4050, 4051, 4052, 4053, 4054, 4055   \ \n\
4056, 4057, 4058, 4059, 4060, 4061, 4062, 4063, 4064, 4065   \ \n\
4066, 4067, 4068, 4069, 4070, 4071, 4072, 4073, 4074, 4075   \ \n\
4076, 4077, 4078, 4079, 4080, 4081, 4082, 4083, 4084, 4085   \ \n\
4086, 4087\n\n'

    if 'mono' in bindmode:
        occ='\
Occupation\n\
864\n\
1,2-864\n\n'
        abspot='\
Absorbing\n\
432 0.100\n\
1, 2, 3, 4, 5, 6, 7, 8, 9, 10   \ \n\
11, 12, 13, 14, 15, 16, 17, 18, 19, 20   \ \n\
21, 22, 23, 24, 25, 26, 27, 28, 29, 30   \ \n\
31, 32, 33, 34, 35, 36, 393, 394, 395, 396   \ \n\
397, 398, 399, 400, 401, 402, 403, 404, 405, 406   \ \n\
407, 408, 409, 410, 411, 412, 413, 414, 415, 416   \ \n\
417, 418, 419, 420, 421, 422, 423, 424, 425, 426   \ \n\
427, 428, 609, 610, 611, 612, 613, 614, 615, 616   \ \n\
617, 618, 619, 620, 621, 622, 623, 624, 625, 626   \ \n\
627, 628, 629, 630, 631, 632, 633, 634, 635, 636   \ \n\
637, 638, 639, 640, 641, 642, 643, 644, 645, 646   \ \n\
647, 648, 649, 650, 651, 652, 653, 654, 655, 656   \ \n\
657, 658, 659, 660, 661, 662, 663, 664, 665, 666   \ \n\
667, 668, 669, 670, 671, 672, 673, 674, 675, 676   \ \n\
677, 678, 679, 680, 1633, 1634, 1635, 1636, 1637, 1638   \ \n\
1639, 1640, 1641, 1642, 1643, 1644, 1645, 1646, 1647, 1648   \ \n\
1649, 1650, 1651, 1652, 1653, 1654, 1655, 1656, 1657, 1658   \ \n\
1659, 1660, 1661, 1662, 1663, 1664, 1665, 1666, 1667, 1668   \ \n\
1669, 1670, 1671, 1672, 1673, 1674, 1675, 1676, 1677, 1678   \ \n\
1679, 1680, 1681, 1682, 1683, 1684, 1685, 1686, 1687, 1688   \ \n\
1689, 1690, 1691, 1692, 1693, 1694, 1695, 1696, 1697, 1698   \ \n\
1699, 1700, 1701, 1702, 1703, 1704, 2417, 2418, 2419, 2420   \ \n\
2421, 2422, 2423, 2424, 2425, 2426, 2427, 2428, 2429, 2430   \ \n\
2431, 2432, 2433, 2434, 2435, 2436, 2437, 2438, 2439, 2440   \ \n\
2441, 2442, 2443, 2444, 2445, 2446, 2447, 2448, 2449, 2450   \ \n\
2451, 2452, 2453, 2454, 2455, 2456, 2457, 2458, 2459, 2460   \ \n\
2461, 2462, 2463, 2464, 2465, 2466, 2467, 2468, 2469, 2470   \ \n\
2471, 2472, 2473, 2474, 2475, 2476, 2477, 2478, 2479, 2480   \ \n\
2481, 2482, 2483, 2484, 2485, 2486, 2487, 2488, 2849, 2850   \ \n\
2851, 2852, 2853, 2854, 2855, 2856, 2857, 2858, 2859, 2860   \ \n\
2861, 2862, 2863, 2864, 2865, 2866, 2867, 2868, 2869, 2870   \ \n\
2871, 2872, 2873, 2874, 2875, 2876, 2877, 2878, 2879, 2880   \ \n\
2881, 2882, 2883, 2884, 2885, 2886, 2887, 2888, 2889, 2890   \ \n\
2891, 2892, 2893, 2894, 2895, 2896, 2897, 2898, 2899, 2900   \ \n\
2901, 2902, 2903, 2904, 2905, 2906, 2907, 2908, 2909, 2910   \ \n\
2911, 2912, 2913, 2914, 2915, 2916, 2917, 2918, 2919, 2920   \ \n\
2921, 2922, 2923, 2924, 2925, 2926, 2927, 2928, 2929, 2930   \ \n\
2931, 2932, 2933, 2934, 2935, 2936, 2937, 2938, 2939, 2940   \ \n\
2941, 2942, 2943, 2944, 2945, 2946, 2947, 2948, 2949, 2950   \ \n\
2951, 2952, 2953, 2954, 2955, 2956, 2957, 2958, 2959, 2960   \ \n\
2961, 2962, 2963, 2964, 2965, 2966, 2967, 2968, 2969, 2970   \ \n\
2971, 2972, 2973, 2974, 2975, 2976, 2977, 2978, 2979, 2980   \ \n\
2981, 2982, 2983, 2984, 2985, 2986, 2987, 2988, 2989, 2990   \ \n\
2991, 2992\n\n'

    if 'dmono' in bindmode:
        occ='\
Occupation\n\
864\n\
1,2-864\n\n'
        abspot='\
Absorbing\n\
432 0.100\n\
161, 162, 163, 164, 165, 166, 167, 168, 169, 170   \ \n\
171, 172, 173, 174, 175, 176, 177, 178, 179, 180   \ \n\
181, 182, 183, 184, 185, 186, 187, 643, 644, 645   \ \n\
646, 647, 648, 649, 650, 651, 652, 653, 654, 655   \ \n\
656, 657, 658, 659, 660, 661, 662, 663, 664, 665   \ \n\
666, 667, 668, 669, 670, 671, 672, 673, 674, 675   \ \n\
676, 677, 678, 679, 680, 681, 682, 683, 684, 685   \ \n\
686, 687, 688, 689, 690, 691, 692, 693, 694, 695   \ \n\
696, 1575, 1576, 1577, 1578, 1579, 1580, 1581, 1582, 1583   \  \n\
1584, 1585, 1586, 1587, 1588, 1589, 1590, 1591, 1592, 1593   \ \n\
1594, 1595, 1596, 1597, 1598, 1599, 1600, 1601, 1602, 1603   \ \n\
1604, 1605, 1606, 1607, 1608, 1609, 1610, 1791, 1792, 1793   \ \n\
1794, 1795, 1796, 1797, 1798, 1799, 1800, 1801, 1802, 1803   \ \n\
1804, 1805, 1806, 1807, 1808, 1809, 1810, 1811, 1812, 1813   \ \n\
1814, 1815, 1816, 1817, 1818, 1819, 1820, 1821, 1822, 1823   \ \n\
1824, 1825, 1826, 1827, 1828, 1829, 1830, 1831, 1832, 1833   \ \n\
1834, 1835, 1836, 1837, 1838, 1839, 1840, 1841, 1842, 1843   \ \n\
1844, 1845, 1846, 1847, 1848, 1849, 1850, 1851, 1852, 1853   \ \n\
1854, 1855, 1856, 1857, 1858, 1859, 1860, 1861, 1862, 1863   \ \n\
1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 3493, 3494   \ \n\
3495, 3496, 3497, 3498, 3499, 3500, 3501, 3502, 3503, 3504   \ \n\
3505, 3506, 3507, 3508, 3509, 3510, 3511, 3512, 3513, 3514   \ \n\
3515, 3516, 3517, 3518, 3519, 3520, 3521, 3522, 3523, 3524   \ \n\
3525, 3526, 3527, 3528, 3529, 3530, 3531, 3532, 3533, 3534   \ \n\
3535, 3536, 3537, 3538, 3539, 3540, 3541, 3542, 3543, 3544   \ \n\
3545, 3546, 3547, 3548, 3549, 3550, 3551, 3552, 3553, 3554   \ \n\
3555, 3556, 3557, 3558, 3559, 3560, 3561, 3562, 3563, 3564   \ \n\
3925, 3926, 3927, 3928, 3929, 3930, 3931, 3932, 3933, 3934   \ \n\
3935, 3936, 3937, 3938, 3939, 3940, 3941, 3942, 3943, 3944   \ \n\
3945, 3946, 3947, 3948, 3949, 3950, 3951, 3952, 3953, 3954   \ \n\
3955, 3956, 3957, 3958, 3959, 3960, 3961, 3962, 3963, 3964   \ \n\
3965, 3966, 3967, 3968, 3969, 3970, 3971, 3972, 3973, 3974   \ \n\
3975, 3976, 3977, 3978, 3979, 3980, 3981, 3982, 3983, 3984   \ \n\
3985, 3986, 3987, 3988, 3989, 3990, 3991, 3992, 3993, 3994   \ \n\
3995, 3996, 3997, 3998, 3999, 4000, 4001, 4002, 4003, 4004   \ \n\
4005, 4006, 4007, 4008, 4009, 4010, 4011, 4012, 4013, 4014   \ \n\
4015, 4016, 4017, 4018, 4019, 4020, 4021, 4022, 4023, 4024   \ \n\
4025, 4026, 4027, 4028, 4029, 4030, 4031, 4032, 4033, 4034   \ \n\
4035, 4036, 4037, 4038, 4039, 4040, 4041, 4042, 4043, 4044   \ \n\
4045, 4046, 4047, 4048, 4049, 4050, 4051, 4052, 4053, 4054   \ \n\
4055, 4056, 4057, 4058, 4059, 4060, 4061, 4062, 4063, 4064   \ \n\
4065, 4066, 4067, 4068, 4069, 4070, 4071, 4072, 4073, 4074   \ \n\
4075, 4076, 4077, 4078, 4079, 4080, 4081, 4082, 4083, 4084   \ \n\
4085, 4086\n\n'

    return cubedyn,dynamics,occ,abspot


# get conformation numbers
def get_confnum(bindmode):
    # files in current directory
    allfiles=os.listdir(os.getcwd())
    # conformation numbers
    confnum=[] 
    # rename dat files
    for file in allfiles:
        if bindmode in file and '.dat' in file:
            newfile=file.replace('tarj_','').replace('_excitations','')
            conf=newfile.replace(bindmode,'').replace('.dat','')
            confnum.append(conf)
            subprocess.call(["mv",file,newfile])
    return confnum


# get particle states
def get_excit(confnum):
    # files in current directory
    allfiles=os.listdir(os.getcwd())
    # conformations and states
    confstates=[[0 for j in range(2)] for i in range(len(confnum))]
    k=0
    for conf in confnum:
        for file in allfiles:
            if str(conf) in file and '.dat' in file:
                states=[]
                # read analyzed excitations
                with open(file) as fo:
                    buff=fo.read().split('\n\n')
                    del buff[-1]
                for i in range(0,len(buff)):
                    buff[i]=str(buff[i]).split('\n')
                    # get particle states
                    for j in range(0,len(buff[i])):
                        if '->' in buff[i][j]: 
                            buff[i][j]=buff[i][j].split()
                            states.append(buff[i][j][2])
                # remove duplicate states
                states=list(set(states))
                confstates[k][0]=int(conf) 
                confstates[k][1]=states
                k+=1
    return confstates


# create bind files for each conformation and particle state 
# organize in subdirectories as: masterpath/conformation/state 
def magic_maker(bindmode,confstates,bottomBind,cluster,queue):
    # master directory
    masterpath=os.getcwd()
    for i in range(0,len(confstates)):
        # create bind file
        subprocess.call(["python","com_to_crystbind.py",bindmode+str(confstates[i][0])+'.com'])
        # create directory for each conformation and move related files
        confdir=bindmode+str(confstates[i][0])
        os.mkdir(confdir)
        sh.move(bindmode+str(confstates[i][0])+'.com',confdir)
        sh.move(bindmode+str(confstates[i][0])+'.dat',confdir)
        sh.move(bindmode+str(confstates[i][0])+'.bind',confdir)
        # access conformation directory
        os.chdir(masterpath+'/'+confdir)
        # create directories and bind files for each state
        states=confstates[i][1]
        for j in range(0,len(states)):
            statedir=states[j]
            os.mkdir(statedir)
            sh.copy(bindmode+str(confstates[i][0])+'.bind',statedir)
            # access state directory
            os.chdir(masterpath+'/'+confdir+'/'+statedir)
            # edit bind file
            with open(bindmode+str(confstates[i][0])+'.bind','a') as fo:
                # bottomBind = 0-cubedyn,1-dynamics,2-occ,3-abspot
                fo.write(bottomBind[0])
                fo.write(bottomBind[1])
                # adsorbate section
                if 'biCA' in bindmode:
                    adsorb='\
Adsorbate\n\
34 '+statedir+' 1.0\n\
866,867-899\n\n'
                if 'mono' in bindmode:
                    adsorb='\
Adsorbate\n\
35 '+statedir+' 1.0\n\
865,866-899\n\n'
                if 'dmono' in bindmode:
                    adsorb='\
Adsorbate\n\
33 '+statedir+' 1.0\n\
865,866-897\n\n'
                fo.write(adsorb)
                fo.write(bottomBind[2])
                fo.write(bottomBind[3])
            # generate submission script
            gen_subscript(cluster,queue,confdir,statedir)
            # go back to conformation directory
            os.chdir(masterpath+'/'+confdir)
        # go back to master directory
        os.chdir(masterpath)
    
         

# RUN PROGRAM
magic_maker(complex,get_excit(get_confnum(complex)),make_bottomBind(complex,steps,cube),cluster,queue)

