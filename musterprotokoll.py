import numpy as np
import matplotlib.pyplot as plt
import PhyPraKit as ppk
import kafe



#Bestimmung m_e ___________________________________________________________________________
M= 0.14174 #Angaben in kg
M_F= 0.0154
o_me=0.1*10**-3 #Fehler von der Wage

me,o_me=(M+1./3.*M_F),o_me+1/3*o_me


#Bestimmung von T ___________________________________________________________________________
hlines,data=ppk.readCSV('HandyPendel.csv')
t=data[0]
a=data[2]

#Glätten der Funktion
a_smooth=ppk.meanFilter(a,7)

# calculate autocorrelation function
ac_a = ppk.autocorrelate(a_smooth)
ac_t = t  

# find maxima and minima using convolution peak finder
width= 3
pidxac =  ppk.convolutionPeakfinder(ac_a, width, th=0.66)
didxac =  ppk.convolutionPeakfinder(-ac_a, width, th=0.66)
if len(pidxac) > 1:
    print(" --> %i auto-correlation peaks found"%(len(pidxac)))
    pidxac[0]=0 # first peak is at 0 by construction
    ac_tp, ac_ap= np.array(ac_t[pidxac]), np.array(ac_a[pidxac])
    ac_td, ac_ad= np.array(ac_t[didxac]), np.array(ac_a[didxac])
else:
    print("*!!* not enough correlation peaks found")

#Plot erstellen
fig=plt.figure(1, figsize=(7.5,10))
fig.subplots_adjust(left=0.14, bottom=0.1, right=0.97, top=0.93,
                    wspace=None, hspace=.25)#
#1.rohdaten mir glätten
ax1=fig.add_subplot(3, 1, 1)
ax1.plot(t, a)
ax1.set_xlabel('Zeit  (ms)', size='large')
ax1.set_ylabel('Amplitude (mV)', size='large')
ax1.grid()
'''
ax2=fig.add_subplot(3, 1, 1)
ax2.plot(t, a_smooth)
ax2.set_xlabel('Zeit (ms)', size='large')
ax2.set_ylabel(u'geglättete Amplitude (mV)', size='large')
ax2.grid()
'''
#2.autocorrelate
ax2=fig.add_subplot(3, 1, 2)
ax2.plot(ac_tp, ac_ap, 'bx', alpha=0.9, label='peaks')
ax2.plot(ac_td, ac_ad, 'gx', alpha=0.9, label='dips')
ax2.plot(ac_t, ac_a, 'k-')
ax2.set_xlabel('$time \, displacement$ (ms) ', size='large')
ax2.set_ylabel('$autocorrelation$', size='large')
ax2.legend(loc='best', numpoints=1, prop={'size':10})
ax2.grid()

#3. analysis of auto-correlation function
ax3 = fig.add_subplot(3, 1, 3)
ac_dtp = ac_tp[1:] - ac_tp[:-1] 
ac_dtd = ac_td[1:] - ac_td[:-1] 
bins=np.linspace(min(min(ac_dtp),min(ac_dtd)), max(max(ac_dtp), max(ac_dtd)), 100)
bc, be, _ = ax3.hist([ac_dtp, ac_dtd], bins, stacked = True, 
                         color=['b','g'], label=['peaks','dips'], alpha=0.5)
ax3.set_xlabel(r'$time \, difference \, of \, maxima/minima$ (ms)', size='large')
ax3.set_ylabel(r'$frequency$', size='large')
ax3.legend(loc='best', numpoints=1, prop={'size':10})
ax3.grid()

#analysis of histogram
m_dtp, s_dtp, sm_dtp = ppk.histstat(bc[0], be, pr=False)
m_dtd, s_dtd, sm_dtd = ppk.histstat(bc[1], be, pr=False)

#T entspricht dem durchnitt con dtp und dtd
T,o_T=(m_dtp+m_dtd)/2.,(sm_dtp+sm_dtd)/2.


#berechnung von D_______________________________________________________________
D=me*(2*np.pi*1/T)**2
o_D=np.sqrt(16*np.pi**4*1/(T**2)*o_me**2+36*np.pi**4*1/(T**6)*o_T**2)


#Ausgeben der Ergebisse_________________________________________________________
print('T =',T,'+/-',o_T)
print('m_eff =',me,'+/-',o_me)
print('D =',D,'+/-',o_D)

#abspeichern und anzeigen der Plots_____________________________________________
plt.savefig('Blatt6_a_auto.pdf')
plt.show()

