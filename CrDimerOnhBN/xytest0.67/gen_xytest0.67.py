import numpy as np

x = 0.5 * np.array([0.2, 0.22, 0.24, 0.26, 0.28, 0.3])
y = np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.5])
i = 0
j = 0
task = "scf"
# x means half of distance between 2 atoms, in crystal-conventional coordinate.
# y means the coordinate of centre of dimer. Y(centre) = y, X(centre) = (Y(centre)+0.5)/2.
# X1=y+x Y1=Y X2=y-x Y2=Y
while i <= len(x)-1:
    j = 0
    while j <= len(y)-1:
        x1 = (y[j] + 0.5) / 2 + x[i]
        x2 = (y[j] + 0.5) / 2 - x[i]
        name = "Crdimer{x}-{y}".format(x=x[i], y=y[j])
        # print(name)
        txt = """&CONTROL
     calculation   = "{task}"
     restart_mode  = "from_scratch"
     prefix        = '{name}'
     pseudo_dir    = "/home/sf05/q-e-qe-6.7MaX-Release/pseudo"
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
Cr1      {x1}   {y}   0.67
Cr2      {x2}   {y}   0.67
            """.format(name=name, task=task, x1=x1, y=y[j], x2=x2)

        slurm = """#!/bin/bash
#
#SBATCH --job-name={name}
#SBATCH --output={name}.out
#SBATCH -N 1
#SBATCH --ntasks-per-node=48
#SBATCH --time=10:00:00
#SBATCH -p debug

EXEC=/home/sf05/q-e-qe-6.7MaX-Release/bin/pw.x

mpirun -np 48 $EXEC -inp {name}.{task}.in > {name}.{task}.out
        """.format(name=name, task=task)

        with open("{name}.scf.in".format(name=name), "w") as f:
            f.write(txt)
        with open("{name}.scf.slurm".format(name=name), "w") as f:
            f.write(slurm)
        print("sbatch {name}.scf.slurm".format(name=name))
        j += 1
    i += 1
