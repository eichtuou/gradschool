# IET bars

set terminal postscript color enhanced font "Helvetica,18" 
set output 'IETrates_bars_avg.eps'

set border lw 2.5
unset key
unset colorbox

set boxwidth 1.00 relative 
set style fill solid 1.00 noborder

unset xtics
set ytics nomirror
set logscale y 10
set format y "10^{%L}"
set ylabel "{/Symbol t}_{IET} [fs], log scale " offset -1,-0.5

set xrange [-3:31]
set yrange [1:100000]

set palette model RGB defined (0 'red', 1 'blue', 2 'green', 3 'purple', 4 'orange', 5 'yellow', 6 'brown')
mol=5
gap=3

set tmargin 0
set bmargin 0
set lmargin 4
set rmargin 0


plot 'rates_singTrip_avg.dat' i 0 u ($0):($2):($0) t '' w boxes palette,\
     ''                       i 0 u ($0+1*(mol+gap)):($4):($0) t '' w boxes palette,\
     ''                       i 0 u ($0+2*(mol+gap)):($6):($0) t '' w boxes palette,\
     ''                       i 0 u ($0+3*(mol+gap)):($8):($0) t '' w boxes palette,\
     20000                    t '' w l lt 0 lw 10 lc rgb 'black',\
     30                       t '' w l lt 0 lw 10 lc rgb 'black'

