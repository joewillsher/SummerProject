from Lifetime import *

# newfig()
# t = np.linspace(0., 3., 1000)
# print(convoluted_exponential(t, .4, .1, 0))
# pl.semilogy(t, convoluted_exponential(t, 6.05448532,  0.48522807,  0.19727462, -0.10720751), '-r')
# savefig('convoluted')
# pl.close()

#get data
data = readFile('np.txt' if '--full-set' in sys.argv else 'np-short.txt')
d = data[0]
print(d)
mass, time = d.reconstructedD0Mass, d.decayTime
print('mass', mass, mass*1e-6*c**2 / e, time, time*1e15)

filtered = data
# cut on mass diff
width = 3.
filtered, rejected, po, bin_width = cutEventSet_massDiff(filtered, width)

bg_integral, bg_fraction = estimate_background(po, filtered, width)

if not '--no-plot' in sys.argv:
	print('plot')

	massDiff_plot(filtered, 'KK', methodName='massDiff_d0dstar_kk')
	massDiff_plot(filtered, 'PP', methodName='massDiff_d0dstar_pp')

	newfig()
	pl.plot([f.massDiff_d0dstar for f in filtered], [f.pD0_t for f in filtered], ',g')
	pl.plot([f.massDiff_d0dstar for f in rejected], [f.pD0_t for f in rejected], ',r')
	savefig('dm-pD0_t-correlation')
	pl.close()

	newfig()
	pl.plot([f.massDiff_d0dstar for f in filtered], [f.pPslow for f in filtered], ',g')
	pl.plot([f.massDiff_d0dstar for f in rejected], [f.pPslow for f in rejected], ',r')
	savefig('dm-pPslow-correlation')
	pl.close()

	newfig()
	pl.plot([f.massDiff_d0dstar for f in filtered], [f.pPslow_t for f in filtered], ',g')
	pl.plot([f.massDiff_d0dstar for f in rejected], [f.pPslow_t for f in rejected], ',r')
	savefig('dm-pPslow_t-correlation')
	pl.close()

	fig, ax = newfig()
	pl.semilogy([f.massDiff_d0dstar for f in filtered if f.decayTime < 20e-12], [f.decayTime*1e12 for f in filtered if f.decayTime < 20e-12], ',g')
	pl.semilogy([f.massDiff_d0dstar for f in rejected if f.decayTime < 20e-12], [f.decayTime*1e12 for f in rejected if f.decayTime < 20e-12], ',r')
	ax.set_ylim(ymin=0.1, ymax=20)
	savefig('dm-decayTime-correlation')
	pl.close()

	newfig()
	pl.plot([f.massDiff_d0dstar for f in filtered], [f.d0IP_log for f in filtered], ',g')
	pl.plot([f.massDiff_d0dstar for f in rejected], [f.d0IP_log for f in rejected], ',r')
	savefig('dm-d0IP_log-correlation')
	pl.close()


	plot_compare(filtered, rejected, 'decayTime', 'decayTime', range=(0, 10e-12), \
		label=r'Decay time $t$ [ps]')
	plot_compare(filtered, rejected, 'pD0_t', 'pd0-t', \
		label=r'$D^0$ Transverse momentum $p_T$ [GeV / c]')
	plot_compare(filtered, rejected, 'pPslow', 'pslow', \
		label=r'Slow $\pi$ momentum p [GeVp_T / c]')
	plot_compare(filtered, rejected, 'pPslow_t', 'pslow-t', \
		label=r'Slow $\pi$ transverse momentum $p_T$ [GeV / c]')
	plot_compare(filtered, rejected, 'pDstar_t', 'dstar-t', \
		label=r'$D^{*+}$ transverse momentum $p_T$ [GeV / c]')
	plot_compare(filtered, rejected, 'pk_t', 'pk-t', \
		label=r'Daughter $k$ transverse momentum $p_T$ [GeV / c]')
	plot_compare(filtered, rejected, 'pp_t', 'pp-t', \
		label=r'Daughter $\pi$ transverse momentum $p_T$ [GeV / c]')

	plot_compare(filtered, rejected, 'd0IP_log', 'd0-impact-parameter', \
		label=r'$\log{\left(IP_{D^0} / \mathrm{mm}\right)}$')
	plot_compare(filtered, rejected, 'kIP_log', 'k-impact-parameter', \
		label=r'$\log{\left(IP_{k} / \mathrm{mm}\right)}$')
	plot_compare(filtered, rejected, 'pIP_log', 'p-impact-parameter', \
		label=r'$\log{\left(IP_{\pi} / \mathrm{mm}\right)}$')
	plot_compare(filtered, rejected, 'psIP_log', 'ps-impact-parameter', \
		label=r'$\log{\left(IP_{\pi_s} / \mathrm{mm}\right)}$')
	
	plot_compare(filtered, rejected, 's_z', 's_z', range=(-200, 200), \
		label=r'$s_z$ [mm]')
	plot_compare(filtered, rejected, 'costheta', 'costheta', range=(.999,1), \
		label=r'$\cos{\theta}$')


print('cut')
filtered, rejected = cut(filtered, rejected, lambda d: 4500 <= d.pD0_t)
filtered, rejected = cut(filtered, rejected, lambda d: 2500 <= d.pDstar_t < 20000)
filtered, rejected = cut(filtered, rejected, lambda d: 200 <= d.pPslow_t < 2500)
filtered, rejected = cut(filtered, rejected, lambda d: 1000 <= d.pk_t)
filtered, rejected = cut(filtered, rejected, lambda d: 1000 <= d.pp_t)

filtered, rejected = cut(filtered, rejected, lambda d: -5 <= d.d0IP_log <= -2.5)
# filtered, rejected = cut(filtered, rejected, lambda d: -4 <= d.kIP_log <= -0.1)
# filtered, rejected = cut(filtered, rejected, lambda d: -4 <= d.pIP_log <= -0.1)
# filtered, rejected = cut(filtered, rejected, lambda d: -4 <= d.psIP_log <= -1.1)

filtered, rejected = cut(filtered, rejected, lambda d:  10 <= d.s_z <= 120)
# filtered, rejected = cut(filtered, rejected, lambda d:  .9995 <= d.costheta)

print('cut-done')

massDiff_plot(filtered, 'after')
estimate_background(po, filtered, width)


# remove width
d0_c, dstar_c = 1865., 2010.
width = 20.
filtered = [event for event in filtered if (d0_c-width) <= mass_toMeV(event.reconstructedD0Mass) <= (d0_c+width) and (dstar_c-width) <= mass_toMeV(event.reconstructedDstarMass) <= (dstar_c+width)]



# filtered = [d for d in filtered if d.pPslow >= 1.3e3]

# massDiff_plot(filtered, 'AFTER', 0)
plotData(filtered)

# mass dist
newfig()
offs = [d.pPslow for d in filtered]
pl.hist(offs, bins=100, histtype='step', fill=False)
savefig('offsets')
pl.close()
