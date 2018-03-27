# Gnuplot script file for plotting data in DOS 
set terminal aqua size 700,700 font "Helvetica,14" enhanced dashed 
#set terminal wxt size 700,700 font "Helvetica,14"

set ytics mirror
set y2tics
set xrange[-1:1]
set yrange [0:]
set key font "Helvetica,11" 

set multiplot layout 2,1 columnsfirst margin 0.1, 0.9, 0.1, 0.9 spacing screen 0.1, screen 0.05

# For atom 1 
unset xlabel
set xtics format ""
set arrow from 0,graph 0 to 0,graph 1 nohead lc 7 dt 2 
set label "Atom 1" at graph 0.1,0.1 front 
plot "pdos_dft.dat" u ($1*27.2):6 w l ls 8, \
     "pdos_afm.dat" u ($1*27.2):6 w l ls 8

# For atom 2
set xlabel "Energy (eV)"
set xtics format "% h"
unset label
set label "Atom 2" at graph 0.1,0.1 front 
plot "pdos_dft.dat" u ($1*27.2):6 w l ls 8, \
     "pdos_afm.dat" u ($1*27.2):6 w l ls 8

unset multiplot

