# UV-VIS spectra - stacked

set term postscript enhanced color solid "Helvetica,20"

set output "febpycn4_stackedSpectra.eps"
set tmargin 0
set bmargin 0
set lmargin 6
set rmargin 10

set multiplot layout 2,1 

set xrange [350:700]
set yrange [0:75]
set y2range [0:0.2]

set ytics 0,25, 75
set y2tics 0, 0.1, 0.2
set ytics nomirror out
set y2tics nomirror out 
unset xtics

set ytics textcolor rgb "black"
set y2tics textcolor rgb "black"

plot 'spec_par.dat' u (1239.84/$1):($2/100) t 'Parent' w l lw 5 lc rgb "#000000",\
'sticks_par.dat' u 1:2 axes x1y2 title '' w i lt 1 lw 3 lc rgb "#000000"

set yrange [0:125]
set ytics 0, 25, 100
set y2tics 0, 0.1, 0.1
set ytics textcolor rgb "gray"
set y2tics textcolor rgb "gray"

set ylabel "{/Symbol e} [M^{-1}cm^{-1}, 10^{2}]" offset -1,6
set y2label "Oscillator Strength" offset 1,6
set xlabel "Wavelength [nm]"

set xtics textcolor rgbcolor "black"
set xtics nomirror out 

set ytics textcolor rgb "gray"
set y2tics textcolor rgb "gray"

plot 'spec_CA.dat' u (1239.84/$1):($2/100) t 'Carboxylic Acid' w l lw 5 lc rgb "#000000",\
'sticks_CA.dat' u 1:2 axes x1y2 t '' w i lt 1 lw 3 lc rgb "#000000"

unset multiplot

