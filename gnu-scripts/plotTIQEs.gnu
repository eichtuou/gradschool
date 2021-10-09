# UV-Vis with TIQEs 

set term postscript enhanced color solid font "Helvetica,18"
set output "TIQEs_all.eps"

set multiplot layout 5,1

set border
set key

set tmargin 0
set bmargin 0
set lmargin 4 
set rmargin 6

set ylabel "TIQE [%]" offset 0,-11.5
set y2label "{/Symbol e} [M^{-1}cm^{-1} x 10^{2}]" offset -0.25,-11.25

set xrange [350:800]
set yrange [0:75]
set y2range [0:120]

unset xtics
set ytics 0, 25, 75
set y2tics 0, 40, 120
set ytics nomirror out
set y2tics nomirror out

set boxwidth 3.00
set style fill solid 1.00 noborder


# PARENT - PERP+PAR
set ytics textcolor rgb "black"
set y2tics textcolor rgb "black"

plot 'spec_par.dat'           u (1239.84/$1):($2/100) axes x1y2 t 'parent' w l lt 1 lw 5 lc rgb "#004080",\
     'TIQEs_singlets.dat' i 0 u ($2):((($3+$4)/2)*100) axes x1y1 t '' w boxes lc rgb "#004080" 


# CN - PERP+PAR
unset ylabel
unset y2label
set ytics 0, 25, 50
set y2tics 0, 40, 80

set ytics textcolor rgb "gray"
set y2tics textcolor rgb "gray"

plot 'spec_CA.dat'            u (1239.84/$1):($2/100) axes x1y2 t 'Cyanide' w l lt 1 lw 5 lc rgb "#8B0000",\
     'TIQEs_singlets.dat' i 4 u ($2):((($3+$4)/2)*100) axes x1y1 t '' w boxes lc rgb "#8B0000" 


# CA - MONODENTATE
set ytics textcolor rgb "black"
set y2tics textcolor rgb "black"

plot 'spec_CA.dat'            u (1239.84/$1):($2/100) axes x1y2 t 'CA-monodentate' w l lt 1 lw 5 lc rgb "#8B0000",\
     'TIQEs_singlets.dat' i 1 u ($2):($3*100) axes x1y1 t '' w boxes lc rgb "#8B0000" 


# CA - BIS-MONODENTATE
set ytics textcolor rgb "gray"
set y2tics textcolor rgb "gray"

plot 'spec_CA.dat'            u (1239.84/$1):($2/100) axes x1y2 t 'CA-bismonodentate' w l lt 1 lw 5 lc rgb "#8B0000",\
     'TIQEs_singlets.dat' i 2 u ($2):($3*100) axes x1y1 t '' w boxes lc rgb "#8B0000" 


# CA - BIDENTATE
set xlabel "Wavelength [nm]"
set xtics nomirror out
set xtics 400, 100, 800
set ytics textcolor rgb "black"
set y2tics textcolor rgb "black"

plot 'spec_CA.dat'            u (1239.84/$1):($2/100) axes x1y2 t 'CA-bidentate' w l lt 1 lw 5 lc rgb "#8B0000",\
     'TIQEs_singlets.dat' i 3 u ($2):($3*100) axes x1y1 t '' w boxes lc rgb "#8B0000" 


unset multiplot

