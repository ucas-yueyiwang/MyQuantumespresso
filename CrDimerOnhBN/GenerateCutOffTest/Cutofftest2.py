import numpy as np
cutwfc = np.array([30, 40, 50, 70, 80, 90])
cutrho = cutwfc * 13
i = 0
atoms = 3
config = 2
task = "scf"
while i <= len(cutwfc)-1:
    name = "{atoms}-{config}-{wfc}-{rho}".format(atoms=atoms, config=config, wfc=cutwfc[i], rho=cutrho[i])
    #print(name)
    txt = """
    &CONTROL
        calculation   = "scf"
        restart_mode  = "from_scratch"
        prefix        = '{name}'
        pseudo_dir    = "../../pseudo/"
        outdir        = '../../mytmp/'
        !forc_conv_thr =  3.d-4
        !nstep=150
    /

    &SYSTEM
        ibrav = 4, A = 12.52, C = 12.0000, nat = 53, ntyp = 5,
        ecutrho                   = {rho}
        ecutwfc                   = {wfc}
        occupations="smearing", smearing="gaussian", degauss=0.025,
      ! lspinorb=true,
        noncolin=true,
        angle1(3)=0
        angle2(3)=0
        angle1(4)=0
        angle2(4)=0
        angle1(5)=0
        angle2(5)=0
        starting_magnetization(3) = 1
        starting_magnetization(4) = 1
        starting_magnetization(5) = 1
        !vdw_corr = 'Grimme-D3'
    /

    &ELECTRONS
        electron_maxstep = 100
        mixing_beta      = 0.3
    mixing_mode='local-TF'
        conv_thr         = 1.d-5
    /


    K_POINTS {{automatic}}
        3 3 1  1 1 0

    ATOMIC_SPECIES
    B      10.81100     B.pbe-n-rrkjus_psl.0.1.UPF
    N      14.00674     N.pbe-n-rrkjus_psl.1.0.0.UPF
    Ti1    47.86700  Ti.pbe-spn-rrkjus_psl.1.0.0.UPF
    Ti2    47.86700  Ti.pbe-spn-rrkjus_psl.1.0.0.UPF
    Ti3    47.86700  Ti.pbe-spn-rrkjus_psl.1.0.0.UPF

    ATOMIC_POSITIONS {{crystal}}
    N        0.740497541   0.069880890   0.483255098
    B        0.275463685   0.539508954   0.539131558
    B        0.073344849   0.537243810   0.501841604
    B        0.475300824   0.537239098   0.501828275
    N        0.342095031   0.672772690   0.510513328
    N        0.940692766   0.669893284   0.484347544
    N        0.541085505   0.670492202   0.495658467
    N        0.140819908   0.670496924   0.495684693
    N        0.740612372   0.669894258   0.484338810
    B        0.473551799   0.737350190   0.496200021
    B        0.874001327   0.736587772   0.482952084
    B        0.074133409   0.736771402   0.487000883
    B        0.674045966   0.736772013   0.486982542
    B        0.275215782   0.737351755   0.496212559
    N        0.940692365   0.869974491   0.484347016
    N        0.540709156   0.870094674   0.483245879
    N        0.340797345   0.870093942   0.483252381
    N        0.140697133   0.869935451   0.484185897
    N        0.740652518   0.869936321   0.484173347
    B        0.673895596   0.936693668   0.482490850
    B        0.474064564   0.936720646   0.480973848
    B        0.873816883   0.936541078   0.486994813
    B        0.674047822   0.536450259   0.486988226
    B        0.873817536   0.536452356   0.486993823
    N        0.343853424   0.471512933   0.521991625
    N        0.940094375   0.469770454   0.495676605
    N        0.540666449   0.069921309   0.477732395
    N        0.340798919   0.069877599   0.483253150
    N        0.940095211   0.069499390   0.495682429
    N        0.140820960   0.069499306   0.495686597
    B        0.673867750   0.136522549   0.480977905
    B        0.873244748   0.137040852   0.496214003
    B        0.275218113   0.137037413   0.496219280
    B        0.474066138   0.136520950   0.480976379
    B        0.073346342   0.135279765   0.501849166
    N        0.139078146   0.266731734   0.522007369
    B        0.274213409   0.936693599   0.482497754
    N        0.740498650   0.269792262   0.483251970
    N        0.540711590   0.269789617   0.483253239
    N        0.342098463   0.268494568   0.510529805
    B        0.673896368   0.336375548   0.482492890
    B        0.275467815   0.335127558   0.539144394
    B        0.873244953   0.335377670   0.496210302
    B        0.071090171   0.335131952   0.539139445
    B        0.473554996   0.335374837   0.496214290
    N        0.740653038   0.469890642   0.484176452
    N        0.541086327   0.469768631   0.495670349
    N        0.139074854   0.471519142   0.521994129
    N        0.937824542   0.268499187   0.510518812
    B        0.074134308   0.936536906   0.487000707
    Ti1      0.336390860   0.467797305   0.701067608
    Ti2      0.142808165   0.467793378   0.701066612
    Ti3      0.142813605   0.274216420   0.701079904
    """.format(rho=cutrho[i], wfc=cutwfc[i], name=name)

    slurm = """#!/bin/bash
#SBATCH -J {name}
#SBATCH -p regular
#SBATCH -N 1
#SBATCH --ntasks-per-node=36
#SBATCH -o {name}.out

module load mpi/intelmpi/2017.4.239
srun --mpi=pmi2 /public/software/apps/qe/6.4.1/intelmpi/bin/pw.x < {name}.{task}.in > {name}.{task}.out
""".format(name=name, task=task)

    with open("{name}.scf.in".format(name=name), "w") as f:
        f.write(txt)
    with open("{name}.scf.slurm".format(name=name), "w") as f:
        f.write(slurm)
    print("sbatch {name}.scf.slurm".format(name=name))
    i += 1
