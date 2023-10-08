import numpy as np
import matplotlib.pyplot as plt
from colecole import * 

n = 4
eps_0 = 8.8541878128e-12


def test1():
    f = np.linspace(1, 100, 300)
    
    # blood from ITIS Database-V4.1: Thermal_dielectric_acoustic_MR properties_database_V4.1(Excel).xls
    ef = 4
    sig = 0.7
    deltas = [56, 5200, 0, 0]
    taus = [8.377e-12, 132.629e-9, 159.155e-6, 15.915e-3]
    alphas = [0.1, 0.1, 0.2, 0]
    er_blood = colecole(n, ef, deltas, taus, alphas, sig)
    plot_colecole_cond(er_blood, f)

    # blood from ITIS Database-V4.1: Thermal_dielectric_acoustic_MR properties_database V4.1(h5-Sim4Life_v2.0).db
    plot_colecole_cond(colecole_from_ITISdb('Blood'), f)
    plt.show()

def test2():
    f = np.linspace(1, 100, 300)
    colecole = colecole_from_ITISdb('Blood')
    plot_colecole_cond(colecole, f)
    plot_e_rel_cond(colecole, f)
    plt.show()
    
def test3():
    f = np.linspace(1, 100, 300)
    colecole = colecole_from_ITISdb('Blood')
    plot_colecole_realimag(colecole, f)
    plot_e_realimag(colecole, f)
    plt.show()

def tissues():
    colecoles = {
        'Skin' : colecole_from_ITISdb('Skin'),
        'Muscle' : colecole_from_ITISdb('Muscle'),
        'Heart Muscle' : colecole_from_ITISdb('Heart Muscle'),
        'Heart Lumen' : colecole_from_ITISdb('Heart Lumen'),
        'Lung' : colecole_from_ITISdb('Lung'),
        'Lung (Deflated)' : colecole_from_ITISdb('Lung (Deflated)'),
        'Lung (Inflated)' : colecole_from_ITISdb('Lung (Inflated)'),
        'Fat' : colecole_from_ITISdb('Fat'),
        'Bone (Cancellous)' : colecole_from_ITISdb('Bone (Cancellous)'),
        'Bone (Cortical)' : colecole_from_ITISdb('Bone (Cortical)'),
        'Air' : colecole_from_ITISdb('Air'),
        'Kidney' : colecole_from_ITISdb('Kidney'),
        'Liver' : colecole_from_ITISdb('Liver'),
        'Urine' : colecole_from_ITISdb('Urine'),
        'Blood' : colecole_from_ITISdb('Blood'),
        'Water' : colecole_from_ITISdb('Water'),
    }
    f = np.logspace(0, 6, 500)
    # plot_e_rel_cond(colecoles['Water'], f, 'Water', log=True)
    for x in colecoles:
        plot_e_rel_cond(colecoles[x], f, str(x), log=True)
    plt.show()


def main():
    # test1()
    # test2()
    # test3()
    tissues()


if __name__ == '__main__':
    main()
