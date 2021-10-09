# DOS with orbital energies

set term postscript enhanced color solid font "Helvetica,20"
set output "DOSorbE.eps"

set ylabel "Energy (eV)"

set yzeroaxis lt 0
set yrange [-17:-6]
set xrange [-520:600]

set ytics nomirror
unset xtics

set border linewidth 1.5
set key spacing 1.2


plot 'CAmonoS_a_huckel.dat'       u (($2*60)-400):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'PAmonoS_a_huckel.dat'       u (($2*60)-300):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'HAs_a_huckel.dat'           u (($2*60)-200):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'CATs_a_huckel.dat'          u (($2*60)-100):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'ACmonoS_a_huckel.dat'       u (($2*60)):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'CAmonoS_a_aligned.bind.DOS' u 1:3 t '' w l lt 2 lw 3.5 lc rgb "#00008B",\
     'CAmonoS_a_aligned.bind.DOS' u 2:3 t '' w l lt -1 lw 3 lc rgb "#000000"

