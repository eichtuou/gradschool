# UV-Vis spectra

set term postscript enhanced color solid font "Helvetica,20"
set output "febpycn4-par.eps"

set xlabel "Wavelength [nm]" font ",24"
set ylabel "{/Symbol e} [M^{-1}cm^{-1} x 10^{2}]" font ",24" offset -1.5,-0.5
set y2label "Oscillator Strength" font ",24" offset -1,0

set border lw 2

set tmargin 0
set bmargin 2
set lmargin 6
set rmargin 6

set xrange [350:800]
set yrange [0:75]
set y2range [0:0.2]

set xtics nomirror out
set xtics 400, 100, 800
set ytics nomirror out
set ytics 0, 25, 75
set y2tics nomirror out
set y2tics 0, 0.1, 0.2

plot 'spec_par.dat'   u (1239.84/$1):($2/100) t '' w l lt 1 lw 5 lc rgb "#004080",\
     'sticks_par.dat' u 1:2 axes x1y2     t '' w i lt 1 lw 3 lc rgb "#000000"

reset

set term postscript enhanced color solid font "Helvetica,20"
set output "febpycn4-CA.eps"

set xlabel "Wavelength [nm]" font ",24"
set ylabel "{/Symbol e} [M^{-1}cm^{-1} x 10^{2}]" font ",24" offset -1.5,-0.5
set y2label "Oscillator Strength" font ",24" offset -1,0

set border lw 2

set tmargin 0
set bmargin 2
set lmargin 6
set rmargin 6

set xrange [350:800]
set yrange [0:125]
set y2range [0:0.2]

set xtics nomirror out
set xtics 400, 100, 800
set ytics nomirror out
set ytics 0, 25, 125
set y2tics nomirror out
set y2tics 0, 0.1, 0.2

plot 'spec_CA.dat'    u (1239.84/$1):($2/100) t '' w l lt 1 lw 5 lc rgb "#004080",\
     'sticks_CA.dat'  u 1:2 axes x1y2     t '' w i lt 1 lw 3 lc rgb "#000000"

