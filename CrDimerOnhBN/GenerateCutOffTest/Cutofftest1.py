import numpy as np
cutwfc = np.array([30, 40, 50, 70, 80, 90])
cutrho = cutwfc * 13
i = 0
atoms = 3
config = 1
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
    N        0.733273197   0.066460353   0.482663681
    B        0.265481231   0.533253363   0.508485902
    B        0.066600264   0.533321411   0.486562044
    B        0.466646722   0.533184231   0.555065988
    N        0.333118233   0.666722116   0.502866624
    N        0.933243958   0.666524641   0.485779703
    N        0.535100227   0.670104001   0.528064987
    N        0.133370935   0.666523337   0.485830190
    N        0.733699057   0.666725815   0.502788845
    B        0.466586591   0.734357796   0.508485970
    B        0.866617759   0.733183460   0.490601917
    B        0.066647616   0.733207140   0.483788805
    B        0.667866617   0.734357264   0.508455864
    B        0.266659963   0.733179824   0.490660436
    N        0.933244716   0.866469520   0.485798651
    N        0.533325102   0.866706149   0.493187169
    N        0.333316368   0.866469058   0.485832578
    N        0.133308143   0.866528851   0.482656732
    N        0.733472545   0.866710074   0.493178367
    B        0.666741013   0.933400352   0.489588402
    B        0.466519003   0.933239920   0.486567582
    B        0.866816864   0.933241220   0.486550231
    B        0.667857665   0.533259823   0.508394002
    B        0.866812668   0.533325636   0.486509373
    N        0.329731433   0.464731552   0.528047275
    N        0.933325772   0.466561782   0.482863938
    N        0.533276934   0.066514237   0.482881212
    N        0.333312501   0.066594286   0.485779800
    N        0.933321582   0.066514770   0.482873226
    N        0.133366473   0.066592506   0.485767795
    B        0.666581318   0.133164749   0.482407658
    B        0.866670282   0.133169323   0.482410120
    B        0.266652491   0.133220514   0.490576286
    B        0.466512236   0.133026400   0.486522331
    B        0.066595532   0.133021120   0.486518968
    N        0.133127488   0.266366017   0.493130746
    B        0.266630064   0.933190368   0.483789768
    N        0.733272348   0.266566371   0.482630842
    N        0.533318243   0.266370356   0.493107574
    N        0.333111229   0.266140008   0.502754059
    B        0.666737134   0.333099221   0.489517866
    B        0.265478320   0.331970511   0.508414549
    B        0.866674473   0.333257018   0.482396931
    B        0.066438732   0.333098672   0.489566890
    B        0.466576160   0.331980201   0.508388842
    N        0.733467307   0.466519037   0.493094882
    N        0.535095283   0.464742520   0.527983472
    N        0.133133069   0.466514705   0.493186230
    N        0.933379008   0.266566050   0.482650749
    B        0.066646862   0.933189315   0.483771399
    Ti1      0.531979205   0.663812062   0.714621215
    Ti2      0.335992003   0.467768997   0.714606043
    Ti3      0.532034428   0.467823580   0.714544396
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
