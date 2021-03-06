import numpy as np
x = np.array([0.01, 0.02, 0.03, 0.04, 0.05, 0.06])
y = np.array([0.01, 0.02, 0.03, 0.04, 0.05, 0.06])
i = 0
j = 0
task = "scf"
while i <= len(x)-1:
    name = "Crdimer-{x}-{y}".format(x=x[i], y=y[i])
    # print(name)
    txt = """
    &CONTROL
    calculation   = "{task}"
    restart_mode  = "from_scratch"
    prefix        = '{name}'
    pseudo_dir    = "/home/yueyi/q-e-gpu-qe-gpu-6.7/pseudo"
    outdir        = './mytmp'
    !forc_conv_thr =  1.d-5
    !nstep=100
/

&SYSTEM
    ibrav = 4, A = 10.0160, C = 18.0000, nat = 34, ntyp = 4,
    ecutrho                   = 457
    ecutwfc                   = 48
    occupations="smearing", smearing="gaussian", degauss=1.d-8,
    nspin                     = 2
    starting_magnetization(3) = 1
    starting_magnetization(4) = 1
    vdw_corr = 'Grimme-D3'
/

&ELECTRONS
    electron_maxstep = 500
    mixing_beta      = 0.5
    conv_thr         = 1.d-7
/



K_POINTS {{automatic}}
    3 3 1  1 1 0

ATOMIC_SPECIES
B      10.81100     B.pbe-n-kjpaw_psl.1.0.0.UPF
N      14.00674     N.pbe-n-kjpaw_psl.1.0.0.UPF
Cr1    51.99610  Cr.pbe-spn-kjpaw_psl.1.0.0.UPF
Cr2    51.99610  Cr.pbe-spn-kjpaw_psl.1.0.0.UPF

ATOMIC_POSITIONS {{crystal}}
B        0.000000000   0.250000000   0.500    0   0   1
B        0.750000000   0.750000000   0.500    0   0   1
B        0.250000000   0.000000000   0.500    0   0   1
B        0.750000000   0.000000000   0.500    0   0   1
B        0.250000000   0.250000000   0.500    0   0   1
B        0.000000000   0.750000000   0.500    0   0   1
N        0.916667000   0.333333000   0.500    0   0   1
N        0.666667000   0.583333000   0.500    0   0   1
N        0.416667000   0.083333000   0.500    0   0   1
N        0.666667000   0.083333000   0.500    0   0   1
N        0.416667000   0.333333000   0.500    0   0   1
N        0.916667000   0.583333000   0.500    0   0   1
N        0.166667000   0.333333000   0.500    0   0   1
N        0.666667000   0.833333000   0.500    0   0   1
N        0.166667000   0.833333000   0.500    0   0   1
B        0.250000000   0.500000000   0.500    0   0   1
B        0.500000000   0.750000000   0.500    0   0   1
B        0.250000000   0.750000000   0.500    0   0   1
B        0.500000000   0.250000000   0.500    0   0   1
B        0.750000000   0.250000000   0.500    0   0   1
B        0.750000000   0.500000000   0.500    0   0   1
N        0.666667000   0.333333000   0.500    0   0   1
B        0.000000000   0.500000000   0.500    0   0   1
B        0.500000000   0.500000000   0.500    0   0   1
B        0.500000000   0.000000000   0.500    0   0   1
N        0.166667000   0.583333000   0.500    0   0   1
N        0.416667000   0.583333000   0.500    0   0   1
N        0.416667000   0.833333000   0.500    0   0   1
N        0.916667000   0.833333000   0.500    0   0   1
N        0.166667000   0.083333000   0.500    0   0   1
N        0.916667000   0.083333000   0.500    0   0   1
B        0.000000000   0.000000000   0.500    0   0   1
Cr1      0.577468588   0.426794586   0.67166666666666666666666666666667
Cr2      0.340036646   0.4053333000   0.67166666666666666666666666666667
    """.format(x=x[i], y=y[i], name=name, task=task)

    slurm = """#!/bin/bash
#SBATCH -J {name}
#SBATCH -p regular
#SBATCH -N 1
#SBATCH --ntasks-per-node=16
#SBATCH -o {name}.out

mpirun -np 16 pw.x -inp {name}.{task}.in > {name}.{task}.out
""".format(name=name, task=task)

    with open("{name}.scf.in".format(name=name), "w") as f:
        f.write(txt)
    with open("{name}.scf.slurm".format(name=name), "w") as f:
        f.write(slurm)
    print("sbatch {name}.scf.slurm".format(name=name))
    i += 1
