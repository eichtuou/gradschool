# wavepacket survival probabilities

set output 'febpycn4CA_survProbs.eps'
set terminal postscript color enhanced font "Helvetica,16" 

set multiplot layout 2,3 columnsfirst 

set xrange [0:2000]
set yrange [0:1]

# column 1
set ylabel 'P(t)' offset 1,-0.5
set ytics nomirror out
set xtics nomirror out
set xtics textcolor "#FFFFFF"
set tmargin 0
set bmargin 0
set lmargin 2
set rmargin 0 

plot 'febpycn4s_monoCA_aligned_69.bind.edyn.dat' using ($1):($2) title 'LUMO' w l lt 1 lw 3 lc rgb "#000000",\
     'febpycn4s_monoCA_aligned_70.bind.edyn.dat' using ($1):($2) title 'LUMO+1' w l lt 1 lw 3 lc rgb "#FF0000",\
     'febpycn4t_monoCA_aligned_69.bind.edyn.dat' using ($1):($2) title '^{3}MLCT' w l lt 1 lw 3 lc rgb "#0000FF"

set xlabel 'Time [fs]'
set xtics textcolor "#000000"
set xtics 0,500,1500

plot 'febpycn4s_dmonoCA_aligned_69.bind.edyn.dat' using ($1):($2) title '' w l lt 1 lw 3 lc rgb "#000000",\
     'febpycn4s_dmonoCA_aligned_70.bind.edyn.dat' using ($1):($2) title '' w l lt 1 lw 3 lc rgb "#FF0000",\
     'febpycn4t_dmonoCA_aligned_69.bind.edyn.dat' using ($1):($2) title '' w l lt 1 lw 3 lc rgb "#0000FF"

# column 2
set lmargin 0
unset ylabel
set ytics textcolor "#FFFFFF"
unset xlabel
set xtics textcolor "#FFFFFF"

plot 'febpycn4s_cn_a_aligned_69.bind.edyn.dat' using ($1):($2) title '' w l lt 1 lw 3 lc rgb "#000000",\
     'febpycn4s_cn_a_aligned_70.bind.edyn.dat' using ($1):($2) title '' w l lt 1 lw 3 lc rgb "#FF0000",\
     'febpycn4t_cn_a_aligned_69.bind.edyn.dat' using ($1):($2) title '' w l lt 1 lw 3 lc rgb "#0000FF"

set xlabel 'Time [fs]'
set xtics textcolor "gray"
set xtics 0,500

plot 'febpycn4s_cn_b_aligned_69.bind.edyn.dat' using ($1):($2) title '' w l lt 1 lw 3 lc rgb "#000000",\
     'febpycn4s_cn_b_aligned_70.bind.edyn.dat' using ($1):($2) title '' w l lt 1 lw 3 lc rgb "#FF0000",\
     'febpycn4t_cn_b_aligned_69.bind.edyn.dat' using ($1):($2) title '' w l lt 1 lw 3 lc rgb "#0000FF"

# column 3
set rmargin 2
set xtics textcolor "#000000"
set xtics 0,500

plot 'febpycn4s_biCA_aligned_69.bind.edyn.dat' using ($1):($2) title '' w l lt 1 lw 3 lc rgb "#000000",\
     'febpycn4s_biCA_aligned_70.bind.edyn.dat' using ($1):($2) title '' w l lt 1 lw 3 lc rgb "#FF0000",\
     'febpycn4t_biCA_aligned_69.bind.edyn.dat' using ($1):($2) title '' w l lt 1 lw 3 lc rgb "#0000FF"

unset multiplot
