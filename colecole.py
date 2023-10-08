import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import sqlite3
eps_0 = 8.8541878128e-12

def format_yaxis(ax):
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2E'))





def plot_colecole_cond(colecole, freqs):
    w = 2*np.pi*freqs
    er = colecole(w)
    cond = -1*w*eps_0*np.imag(er)
    er_real = np.real(er)
    fig, ax = plt.subplots(2, sharex=True)
    ax[0].plot(freqs, er_real)
    ax[0].set_ylabel('Relative Permittivity')
    ax[1].set_ylabel('Conductivity (S/m)')
    ax[1].set_xlabel('Frequency (Hz)')
    ax[1].plot(freqs, cond)
    format_yaxis(ax[0])
    format_yaxis(ax[1])   

def plot_colecole_realimag(colecole, freqs):
    w = 2*np.pi*freqs
    er = colecole(w)
    er_imag = -1*np.imag(er)
    er_real = np.real(er)
    fig, ax = plt.subplots(2, sharex=True)
    ax[0].plot(freqs, er_real)
    ax[0].set_ylabel(r"$ \epsilon ' $")
    ax[1].set_ylabel(r"$ \epsilon '' $")
    ax[1].set_xlabel('Frequency (Hz)')
    ax[1].plot(freqs, er_imag)
    format_yaxis(ax[0])
    format_yaxis(ax[1])

def e_rel_cond(colecole):
    def e_rel(omega):
        return np.real(colecole(omega))
    def cond(omega):
        return -1*omega*eps_0*np.imag(colecole(omega))
    return [e_rel, cond]

def e_real_imag(colecole):
    def e_p(omega):
        return np.real(colecole(omega))
    def e_pp(omega):
        return -1*np.imag(colecole(omega))
    return [e_p, e_pp]

def plot_e_rel_cond(colecole, freqs, name='', log=False):
    w = 2*np.pi*freqs
    e_rel, cond = e_rel_cond(colecole)
    fig, ax = plt.subplots(2, sharex=True)
    ax[0].plot(freqs, e_rel(w))
    ax[0].set_title(name)
    ax[0].set_ylabel('Relative Permittivity')
    ax[1].set_ylabel('Conductivity (S/m)')
    ax[1].set_xlabel('Frequency (Hz)')
    ax[1].plot(freqs, cond(w))
    if log:
        ax[0].set_xscale('log', base=10)
        ax[1].set_xscale('log', base=10)
    format_yaxis(ax[0])
    format_yaxis(ax[1])

def plot_e_realimag(colecole, freqs):
    w = 2*np.pi*freqs
    e_real, e_imag = e_real_imag(colecole)
    fig, ax = plt.subplots(2, sharex=True)
    ax[0].plot(freqs, e_real(w))
    ax[0].set_ylabel(r"$ \epsilon ' $")
    ax[1].set_ylabel(r"$ \epsilon '' $")
    ax[1].set_xlabel('Frequency (Hz)')
    ax[1].plot(freqs, e_imag(w))
    format_yaxis(ax[0])
    format_yaxis(ax[1])  

# Calculation taken from the following paper (although many other resources available):
# DOI: 10.1088/0031-9155/57/8/2169
def colecole(n, ef, deltas, taus, alphas, sigma):
    def eps_r(omega):
        er_sum = ef + sigma/(1j*omega*eps_0)
        for i in range(n):
            er_sum = er_sum + deltas[i]/(1+np.float_power(1j*omega*taus[i], 1-alphas[i]))
        return er_sum
    return eps_r

# from ITIS Database-V4.1: 'Thermal_dielectric_acoustic_MR properties_database V4.1(h5-Sim4Life_v2.0).db'
# renamed to 'properties.db'
def colecole_from_ITISdb(tissue):
    # open db
    conn = sqlite3.connect('properties.db')
    c = conn.cursor()
    # get property id
    res = c.execute("SELECT prop_id, name FROM properties WHERE name='Gabriel Parameters'")
    prop_id, _ = res.fetchone()
    res.fetchall()
    # get material id
    res = c.execute("SELECT mat_id, name FROM materials WHERE name=?", [tissue])
    mat_id, _ = res.fetchone()
    res.fetchall()
    # get the data
    res = c.execute("SELECT mat_id, prop_id, vals FROM vectors WHERE mat_id=? AND prop_id=?", [mat_id, prop_id])
    vals = res.fetchone()
    res.fetchall()
    # decode data
    params = np.frombuffer(vals[2])
    deltas = [params[1], params[4], params[7], params[10]]
    taus = [1e-12*params[2], 1e-9*params[5], 1e-6*params[8], 1e-3*params[11]]
    alphas = [params[3], params[6], params[9], params[12]]
    return colecole(4, params[0], deltas, taus, alphas, params[13])

def main():
    pass

if __name__ == '__main__':
    main()


