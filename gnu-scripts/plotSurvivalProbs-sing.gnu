# wavepacket survival probabilities

set term postscript enhanced color solid font "Helvetica,20"
set output "survProb_3mlct.eps"

set tmargin 0
set bmargin 2  
set lmargin 6  
set rmargin 16

set xrange [0:4000]
set yrange [0:1]
set xlabel "Time [fs]"
set ylabel "P(t)"

set border lw 2
set key outside
set key font ",14"
set key spacing 1.5

set ytics nomirror out                                   
set xtics nomirror out                                   
set xtics 0,1000,4000

set style line 1  lt -1 lw 2 linecolor rgb 'red'
set style line 2  lt -1 lw 2 linecolor rgb 'light-pink'
set style line 3  lt -1 lw 2 linecolor rgb 'blue'
set style line 4  lt -1 lw 2 linecolor rgb 'web-blue'
set style line 5  lt -1 lw 2 linecolor rgb 'web-green'
set style line 6  lt -1 lw 2 linecolor rgb 'orange'
set style line 7  lt -1 lw 2 linecolor rgb 'black'
set style line 8  lt -1 lw 2 linecolor rgb 'gray40' 
set style line 9  lt -1 lw 2 linecolor rgb 'gray70' 
set style line 10 lt -1 lw 2 linecolor rgb 'dark-pink' 

plot  'febpycn4t_par_cn_a_aligned_53.bind.edyn' u 1:2 w l ls 7  t '1-CN^{-},bpy-perp',\
      'febpycn4t_par_cn_b_aligned_53.bind.edyn' u 1:2 w l ls 8  t '1-CN^{-},bpy-par',\
      'febpycn4t_cn_a_aligned_69.bind.edyn'     u 1:2 w l ls 3  t '2-CN^{-},bpy-perp',\
      'febpycn4t_cn_b_aligned_69.bind.edyn'     u 1:2 w l ls 4  t '2-CN^{-},bpy-par',\
      'febpycn4t_monoCA_aligned_69.bind.edyn'   u 1:2 w l ls 1  t '2-mono',\
      'febpycn4t_dmonoCA_aligned_69.bind.edyn'  u 1:2 w l ls 2  t '2-bis-mono',\
      'febpycn4t_biCA_aligned_69.bind.edyn'     u 1:2 w l ls 10 t '2-bi'

