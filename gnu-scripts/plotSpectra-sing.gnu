# UV-Vis spectra

set term postscript enhanced color solid font "Helvetica,20"
set output "febpycn4.eps"

set xlabel "Wavelength [nm]"
set ylabel "{/Symbol e} [M^{-1}cm^{-1}]" offset 1,-0.5
set y2label "Oscillator Strength" font "Helvetica,18" offset -1,0

set border lw 2
set key spacing 1.5 font "Helvetica,18"

set tmargin 0
set bmargin 2
set lmargin 6
set rmargin 6

set xrange [350:800]
set yrange [0:9000]
set y2range [0:0.2]

set xtics nomirror out
set xtics 400, 100, 800
set ytics nomirror out
set y2tics nomirror out
set y2tics 0, 0.1, 0.2

plot 'spec_par.dat'   u (1239.84/$1):($2) t '[Fe(bpy)(CN)_{4}]^{2-}' w l lt 1 lw 10 lc rgb "#004080",\
     'spec_CA.dat'    u (1239.84/$1):($2) t '[Fe(bpy-dca)(CN)_{4}]^{2-}' w l lt 1 lw 10 lc rgb "#8B0000"
#    'sticks_par.dat' u 1:2 axes x1y2     t '' w i lt 1 lw 5 lc rgb "#004080",\
#    'sticks_CA.dat'  u 1:2 axes x1y2     t '' w i lt 1 lw 5 lc rgb "#8B0000"

