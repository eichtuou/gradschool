# IET vs E density plot

set terminal postscript color enhanced font 'Helvetica,14' 
set output 'edensityIET_k.eps'

set border lw 2 
set key outside

set ylabel 'k_{IET} (fs^{-1})'
set xlabel 'Electron density on linker (%)' font 'Helvetica,14'

set xrange [0:20]
set yrange [0:0.05]

set xtics nomirror
set ytics nomirror

plot 'edensity.dat' i 0 u ($2):(1/$1) t 'CA-mono' w p pt 7 ps 2 lc rgb 'red',\
'' i 0 u ($4):(1/$3) t ''         w p pt 7 ps 2 lc rgb 'red',\
'' i 0 u ($6):(1/$5) t 'CA-bi'    w p pt 7 ps 2 lc rgb '#FF69B4',\
'' i 0 u ($8):(1/$7) t ''         w p pt 7 ps 2 lc rgb '#FF69B4',\
'' i 1 u ($2):(1/$1) t 'PA-mono'  w p pt 7 ps 2 lc rgb 'blue',\
'' i 1 u ($4):(1/$3) t ''         w p pt 7 ps 2 lc rgb 'blue',\
'' i 1 u ($6):(1/$5) t 'PA-bi'    w p pt 7 ps 2 lc rgb '#48D1CC',\
'' i 1 u ($8):(1/$7) t ''         w p pt 7 ps 2 lc rgb '#48D1CC',\
'' i 2 u ($2):(1/$1) t 'HA-bich'  w p pt 7 ps 2 lc rgb '#008000',\
'' i 2 u ($4):(1/$3) t ''         w p pt 7 ps 2 lc rgb '#008000',\
'' i 4 u ($2):(1/$1) t 'CAT-bibr' w p pt 7 ps 2 lc rgb 'purple',\
'' i 3 u ($2):(1/$1) t 'AC-bibr'  w p pt 7 ps 2 lc rgb 'orange',\
'' i 3 u ($4):(1/$3) t ''         w p pt 7 ps 2 lc rgb 'orange',\
'' i 3 u ($6):(1/$5) t 'AC-bich'  w p pt 7 ps 2 lc rgb 'yellow',\
'' i 3 u ($8):(1/$7) t ''         w p pt 7 ps 2 lc rgb 'yellow',\
'' i 3 u ($10):(1/$9) t 'AC-mono' w p pt 7 ps 2 lc rgb 'black',\
'' i 3 u ($12):(1/$11) t ''       w p pt 7 ps 2 lc rgb 'black'

