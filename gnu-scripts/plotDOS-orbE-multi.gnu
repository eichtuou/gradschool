# This script creates 28 indiviual plots of the same type.

# DOS with orbital energies
set term postscript enhanced color solid font "Helvetica,20"
set output "febpycn4s_biCA_dos_1.eps"

set ylabel "Energy [eV]"
set xlabel "Density of States [arb]"

set yzeroaxis lt 0
set yrange [-18:-6]
set xrange [-120:1000]

set ytics nomirror out
unset xtics

set border linewidth 1.5
set key spacing 1.2


plot 'febpycn4s_biCA_huckel_orbE.dat'     u ($2*60):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'febpycn4s_biCA_aligned.bind.DOS'    u 1:3 t '' w l lt 2 lw 3.5 lc rgb "#00008B",\
     'febpycn4s_biCA_aligned.bind.DOS'    u 2:3 t '' w l lt -1 lw 3  lc rgb "#000000"
reset

# DOS with orbital energies
set term postscript enhanced color solid font "Helvetica,20"
set output "febpycn4s_biCA_dos_2.eps"

set ylabel "Energy [eV]"
set xlabel "Density of States [arb]"

set yzeroaxis lt 0
set yrange [-11:-6]
set xrange [-120:1000]

set ytics nomirror out
unset xtics

set border linewidth 1.5
set key spacing 1.2


plot 'febpycn4s_biCA_huckel_orbE.dat'     u ($2*60):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'febpycn4s_biCA_aligned.bind.DOS'    u 1:3 t '' w l lt 2 lw 3.5 lc rgb "#00008B",\
     'febpycn4s_biCA_aligned.bind.DOS'    u 2:3 t '' w l lt -1 lw 3  lc rgb "#000000"
reset

# DOS with orbital energies
set term postscript enhanced color solid font "Helvetica,20"
set output "febpycn4t_biCA_dos_1.eps"

set ylabel "Energy [eV]"
set xlabel "Density of States [arb]"

set yzeroaxis lt 0
set yrange [-18:-6]
set xrange [-120:1000]

set ytics nomirror out
unset xtics

set border linewidth 1.5
set key spacing 1.2


plot 'febpycn4t_biCA_huckel_orbE.dat'     u ($2*60):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'febpycn4t_biCA_aligned.bind.DOS'    u 1:3 t '' w l lt 2 lw 3.5 lc rgb "#00008B",\
     'febpycn4t_biCA_aligned.bind.DOS'    u 2:3 t '' w l lt -1 lw 3  lc rgb "#000000"
reset

# DOS with orbital energies
set term postscript enhanced color solid font "Helvetica,20"
set output "febpycn4t_biCA_dos_2.eps"

set ylabel "Energy [eV]"
set xlabel "Density of States [arb]"

set yzeroaxis lt 0
set yrange [-11:-6]
set xrange [-120:1000]

set ytics nomirror out
unset xtics

set border linewidth 1.5
set key spacing 1.2


plot 'febpycn4t_biCA_huckel_orbE.dat'     u ($2*60):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'febpycn4t_biCA_aligned.bind.DOS'    u 1:3 t '' w l lt 2 lw 3.5 lc rgb "#00008B",\
     'febpycn4t_biCA_aligned.bind.DOS'    u 2:3 t '' w l lt -1 lw 3  lc rgb "#000000"
reset

# DOS with orbital energies
set term postscript enhanced color solid font "Helvetica,20"
set output "febpycn4s_monoCA_dos_1.eps"

set ylabel "Energy [eV]"
set xlabel "Density of States [arb]"

set yzeroaxis lt 0
set yrange [-18:-6]
set xrange [-120:1000]

set ytics nomirror out
unset xtics

set border linewidth 1.5
set key spacing 1.2


plot 'febpycn4s_monoCA_huckel_orbE.dat'     u ($2*60):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'febpycn4s_monoCA_aligned.bind.DOS'    u 1:3 t '' w l lt 2 lw 3.5 lc rgb "#00008B",\
     'febpycn4s_monoCA_aligned.bind.DOS'    u 2:3 t '' w l lt -1 lw 3  lc rgb "#000000"
reset

# DOS with orbital energies
set term postscript enhanced color solid font "Helvetica,20"
set output "febpycn4s_monoCA_dos_2.eps"

set ylabel "Energy [eV]"
set xlabel "Density of States [arb]"

set yzeroaxis lt 0
set yrange [-11:-6]
set xrange [-120:1000]

set ytics nomirror out
unset xtics

set border linewidth 1.5
set key spacing 1.2


plot 'febpycn4s_monoCA_huckel_orbE.dat'     u ($2*60):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'febpycn4s_monoCA_aligned.bind.DOS'    u 1:3 t '' w l lt 2 lw 3.5 lc rgb "#00008B",\
     'febpycn4s_monoCA_aligned.bind.DOS'    u 2:3 t '' w l lt -1 lw 3  lc rgb "#000000"
reset

# DOS with orbital energies
set term postscript enhanced color solid font "Helvetica,20"
set output "febpycn4t_monoCA_dos_1.eps"

set ylabel "Energy [eV]"
set xlabel "Density of States [arb]"

set yzeroaxis lt 0
set yrange [-18:-6]
set xrange [-120:1000]

set ytics nomirror out
unset xtics

set border linewidth 1.5
set key spacing 1.2


plot 'febpycn4t_monoCA_huckel_orbE.dat'     u ($2*60):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'febpycn4t_monoCA_aligned.bind.DOS'    u 1:3 t '' w l lt 2 lw 3.5 lc rgb "#00008B",\
     'febpycn4t_monoCA_aligned.bind.DOS'    u 2:3 t '' w l lt -1 lw 3  lc rgb "#000000"
reset

# DOS with orbital energies
set term postscript enhanced color solid font "Helvetica,20"
set output "febpycn4t_monoCA_dos_2.eps"

set ylabel "Energy [eV]"
set xlabel "Density of States [arb]"

set yzeroaxis lt 0
set yrange [-11:-6]
set xrange [-120:1000]

set ytics nomirror out
unset xtics

set border linewidth 1.5
set key spacing 1.2


plot 'febpycn4t_monoCA_huckel_orbE.dat'     u ($2*60):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'febpycn4t_monoCA_aligned.bind.DOS'    u 1:3 t '' w l lt 2 lw 3.5 lc rgb "#00008B",\
     'febpycn4t_monoCA_aligned.bind.DOS'    u 2:3 t '' w l lt -1 lw 3  lc rgb "#000000"
reset

# DOS with orbital energies
set term postscript enhanced color solid font "Helvetica,20"
set output "febpycn4s_dmonoCA_dos_1.eps"

set ylabel "Energy [eV]"
set xlabel "Density of States [arb]"

set yzeroaxis lt 0
set yrange [-18:-6]
set xrange [-120:1000]

set ytics nomirror out
unset xtics

set border linewidth 1.5
set key spacing 1.2


plot 'febpycn4s_dmonoCA_huckel_orbE.dat'     u ($2*60):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'febpycn4s_dmonoCA_aligned.bind.DOS'    u 1:3 t '' w l lt 2 lw 3.5 lc rgb "#00008B",\
     'febpycn4s_dmonoCA_aligned.bind.DOS'    u 2:3 t '' w l lt -1 lw 3  lc rgb "#000000"
reset

# DOS with orbital energies
set term postscript enhanced color solid font "Helvetica,20"
set output "febpycn4s_dmonoCA_dos_2.eps"

set ylabel "Energy [eV]"
set xlabel "Density of States [arb]"

set yzeroaxis lt 0
set yrange [-11:-6]
set xrange [-120:1000]

set ytics nomirror out
unset xtics

set border linewidth 1.5
set key spacing 1.2


plot 'febpycn4s_dmonoCA_huckel_orbE.dat'     u ($2*60):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'febpycn4s_dmonoCA_aligned.bind.DOS'    u 1:3 t '' w l lt 2 lw 3.5 lc rgb "#00008B",\
     'febpycn4s_dmonoCA_aligned.bind.DOS'    u 2:3 t '' w l lt -1 lw 3  lc rgb "#000000"
reset

# DOS with orbital energies
set term postscript enhanced color solid font "Helvetica,20"
set output "febpycn4t_dmonoCA_dos_1.eps"

set ylabel "Energy [eV]"
set xlabel "Density of States [arb]"

set yzeroaxis lt 0
set yrange [-18:-6]
set xrange [-120:1000]

set ytics nomirror out
unset xtics

set border linewidth 1.5
set key spacing 1.2


plot 'febpycn4t_dmonoCA_huckel_orbE.dat'     u ($2*60):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'febpycn4t_dmonoCA_aligned.bind.DOS'    u 1:3 t '' w l lt 2 lw 3.5 lc rgb "#00008B",\
     'febpycn4t_dmonoCA_aligned.bind.DOS'    u 2:3 t '' w l lt -1 lw 3  lc rgb "#000000"
reset

# DOS with orbital energies
set term postscript enhanced color solid font "Helvetica,20"
set output "febpycn4t_dmonoCA_dos_2.eps"

set ylabel "Energy [eV]"
set xlabel "Density of States [arb]"

set yzeroaxis lt 0
set yrange [-11:-6]
set xrange [-120:1000]

set ytics nomirror out
unset xtics

set border linewidth 1.5
set key spacing 1.2


plot 'febpycn4t_dmonoCA_huckel_orbE.dat'     u ($2*60):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'febpycn4t_dmonoCA_aligned.bind.DOS'    u 1:3 t '' w l lt 2 lw 3.5 lc rgb "#00008B",\
     'febpycn4t_dmonoCA_aligned.bind.DOS'    u 2:3 t '' w l lt -1 lw 3  lc rgb "#000000"
reset

# DOS with orbital energies
set term postscript enhanced color solid font "Helvetica,20"
set output "febpycn4s_cn_a_dos_1.eps"

set ylabel "Energy [eV]"
set xlabel "Density of States [arb]"

set yzeroaxis lt 0
set yrange [-18:-6]
set xrange [-120:1000]

set ytics nomirror out
unset xtics

set border linewidth 1.5
set key spacing 1.2


plot 'febpycn4s_cn_a_huckel_orbE.dat'     u ($2*60):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'febpycn4s_cn_a_aligned.bind.DOS'    u 1:3 t '' w l lt 2 lw 3.5 lc rgb "#00008B",\
     'febpycn4s_cn_a_aligned.bind.DOS'    u 2:3 t '' w l lt -1 lw 3  lc rgb "#000000"
reset

# DOS with orbital energies
set term postscript enhanced color solid font "Helvetica,20"
set output "febpycn4s_cn_a_dos_2.eps"

set ylabel "Energy [eV]"
set xlabel "Density of States [arb]"

set yzeroaxis lt 0
set yrange [-11:-6]
set xrange [-120:1000]

set ytics nomirror out
unset xtics

set border linewidth 1.5
set key spacing 1.2


plot 'febpycn4s_cn_a_huckel_orbE.dat'     u ($2*60):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'febpycn4s_cn_a_aligned.bind.DOS'    u 1:3 t '' w l lt 2 lw 3.5 lc rgb "#00008B",\
     'febpycn4s_cn_a_aligned.bind.DOS'    u 2:3 t '' w l lt -1 lw 3  lc rgb "#000000"
reset

# DOS with orbital energies
set term postscript enhanced color solid font "Helvetica,20"
set output "febpycn4t_cn_a_dos_1.eps"

set ylabel "Energy [eV]"
set xlabel "Density of States [arb]"

set yzeroaxis lt 0
set yrange [-18:-6]
set xrange [-120:1000]

set ytics nomirror out
unset xtics

set border linewidth 1.5
set key spacing 1.2


plot 'febpycn4t_cn_a_huckel_orbE.dat'     u ($2*60):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'febpycn4t_cn_a_aligned.bind.DOS'    u 1:3 t '' w l lt 2 lw 3.5 lc rgb "#00008B",\
     'febpycn4t_cn_a_aligned.bind.DOS'    u 2:3 t '' w l lt -1 lw 3  lc rgb "#000000"
reset

# DOS with orbital energies
set term postscript enhanced color solid font "Helvetica,20"
set output "febpycn4t_cn_a_dos_2.eps"

set ylabel "Energy [eV]"
set xlabel "Density of States [arb]"

set yzeroaxis lt 0
set yrange [-11:-6]
set xrange [-120:1000]

set ytics nomirror out
unset xtics

set border linewidth 1.5
set key spacing 1.2


plot 'febpycn4t_cn_a_huckel_orbE.dat'     u ($2*60):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'febpycn4t_cn_a_aligned.bind.DOS'    u 1:3 t '' w l lt 2 lw 3.5 lc rgb "#00008B",\
     'febpycn4t_cn_a_aligned.bind.DOS'    u 2:3 t '' w l lt -1 lw 3  lc rgb "#000000"
reset

# DOS with orbital energies
set term postscript enhanced color solid font "Helvetica,20"
set output "febpycn4s_cn_b_dos_1.eps"

set ylabel "Energy [eV]"
set xlabel "Density of States [arb]"

set yzeroaxis lt 0
set yrange [-18:-6]
set xrange [-120:1000]

set ytics nomirror out
unset xtics

set border linewidth 1.5
set key spacing 1.2


plot 'febpycn4s_cn_b_huckel_orbE.dat'     u ($2*60):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'febpycn4s_cn_b_aligned.bind.DOS'    u 1:3 t '' w l lt 2 lw 3.5 lc rgb "#00008B",\
     'febpycn4s_cn_b_aligned.bind.DOS'    u 2:3 t '' w l lt -1 lw 3  lc rgb "#000000"
reset

# DOS with orbital energies
set term postscript enhanced color solid font "Helvetica,20"
set output "febpycn4s_cn_b_dos_2.eps"

set ylabel "Energy [eV]"
set xlabel "Density of States [arb]"

set yzeroaxis lt 0
set yrange [-11:-6]
set xrange [-120:1000]

set ytics nomirror out
unset xtics

set border linewidth 1.5
set key spacing 1.2


plot 'febpycn4s_cn_b_huckel_orbE.dat'     u ($2*60):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'febpycn4s_cn_b_aligned.bind.DOS'    u 1:3 t '' w l lt 2 lw 3.5 lc rgb "#00008B",\
     'febpycn4s_cn_b_aligned.bind.DOS'    u 2:3 t '' w l lt -1 lw 3  lc rgb "#000000"
reset

# DOS with orbital energies
set term postscript enhanced color solid font "Helvetica,20"
set output "febpycn4t_cn_b_dos_1.eps"

set ylabel "Energy [eV]"
set xlabel "Density of States [arb]"

set yzeroaxis lt 0
set yrange [-18:-6]
set xrange [-120:1000]

set ytics nomirror out
unset xtics

set border linewidth 1.5
set key spacing 1.2


plot 'febpycn4t_cn_b_huckel_orbE.dat'     u ($2*60):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'febpycn4t_cn_b_aligned.bind.DOS'    u 1:3 t '' w l lt 2 lw 3.5 lc rgb "#00008B",\
     'febpycn4t_cn_b_aligned.bind.DOS'    u 2:3 t '' w l lt -1 lw 3  lc rgb "#000000"
reset

# DOS with orbital energies
set term postscript enhanced color solid font "Helvetica,20"
set output "febpycn4t_cn_b_dos_2.eps"

set ylabel "Energy [eV]"
set xlabel "Density of States [arb]"

set yzeroaxis lt 0
set yrange [-11:-6]
set xrange [-120:1000]

set ytics nomirror out
unset xtics

set border linewidth 1.5
set key spacing 1.2


plot 'febpycn4t_cn_b_huckel_orbE.dat'     u ($2*60):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'febpycn4t_cn_b_aligned.bind.DOS'    u 1:3 t '' w l lt 2 lw 3.5 lc rgb "#00008B",\
     'febpycn4t_cn_b_aligned.bind.DOS'    u 2:3 t '' w l lt -1 lw 3  lc rgb "#000000"
reset

# DOS with orbital energies
set term postscript enhanced color solid font "Helvetica,20"
set output "febpycn4s_par_cn_a_dos_1.eps"

set ylabel "Energy [eV]"
set xlabel "Density of States [arb]"

set yzeroaxis lt 0
set yrange [-18:-6]
set xrange [-120:1000]

set ytics nomirror out
unset xtics

set border linewidth 1.5
set key spacing 1.2


plot 'febpycn4s_par_cn_a_huckel_orbE.dat'     u ($2*60):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'febpycn4s_par_cn_a_aligned.bind.DOS'    u 1:3 t '' w l lt 2 lw 3.5 lc rgb "#00008B",\
     'febpycn4s_par_cn_a_aligned.bind.DOS'    u 2:3 t '' w l lt -1 lw 3  lc rgb "#000000"
reset

# DOS with orbital energies
set term postscript enhanced color solid font "Helvetica,20"
set output "febpycn4s_par_cn_a_dos_2.eps"

set ylabel "Energy [eV]"
set xlabel "Density of States [arb]"

set yzeroaxis lt 0
set yrange [-11:-6]
set xrange [-120:1000]

set ytics nomirror out
unset xtics

set border linewidth 1.5
set key spacing 1.2


plot 'febpycn4s_par_cn_a_huckel_orbE.dat'     u ($2*60):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'febpycn4s_par_cn_a_aligned.bind.DOS'    u 1:3 t '' w l lt 2 lw 3.5 lc rgb "#00008B",\
     'febpycn4s_par_cn_a_aligned.bind.DOS'    u 2:3 t '' w l lt -1 lw 3  lc rgb "#000000"
reset

# DOS with orbital energies
set term postscript enhanced color solid font "Helvetica,20"
set output "febpycn4t_par_cn_a_dos_1.eps"

set ylabel "Energy [eV]"
set xlabel "Density of States [arb]"

set yzeroaxis lt 0
set yrange [-18:-6]
set xrange [-120:1000]

set ytics nomirror out
unset xtics

set border linewidth 1.5
set key spacing 1.2


plot 'febpycn4t_par_cn_a_huckel_orbE.dat'     u ($2*60):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'febpycn4t_par_cn_a_aligned.bind.DOS'    u 1:3 t '' w l lt 2 lw 3.5 lc rgb "#00008B",\
     'febpycn4t_par_cn_a_aligned.bind.DOS'    u 2:3 t '' w l lt -1 lw 3  lc rgb "#000000"
reset

# DOS with orbital energies
set term postscript enhanced color solid font "Helvetica,20"
set output "febpycn4t_par_cn_a_dos_2.eps"

set ylabel "Energy [eV]"
set xlabel "Density of States [arb]"

set yzeroaxis lt 0
set yrange [-11:-6]
set xrange [-120:1000]

set ytics nomirror out
unset xtics

set border linewidth 1.5
set key spacing 1.2


plot 'febpycn4t_par_cn_a_huckel_orbE.dat'     u ($2*60):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'febpycn4t_par_cn_a_aligned.bind.DOS'    u 1:3 t '' w l lt 2 lw 3.5 lc rgb "#00008B",\
     'febpycn4t_par_cn_a_aligned.bind.DOS'    u 2:3 t '' w l lt -1 lw 3  lc rgb "#000000"
reset

# DOS with orbital energies
set term postscript enhanced color solid font "Helvetica,20"
set output "febpycn4s_par_cn_b_dos_1.eps"

set ylabel "Energy [eV]"
set xlabel "Density of States [arb]"

set yzeroaxis lt 0
set yrange [-18:-6]
set xrange [-120:1000]

set ytics nomirror out
unset xtics

set border linewidth 1.5
set key spacing 1.2


plot 'febpycn4s_par_cn_b_huckel_orbE.dat'     u ($2*60):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'febpycn4s_par_cn_b_aligned.bind.DOS'    u 1:3 t '' w l lt 2 lw 3.5 lc rgb "#00008B",\
     'febpycn4s_par_cn_b_aligned.bind.DOS'    u 2:3 t '' w l lt -1 lw 3  lc rgb "#000000"
reset

# DOS with orbital energies
set term postscript enhanced color solid font "Helvetica,20"
set output "febpycn4s_par_cn_b_dos_2.eps"

set ylabel "Energy [eV]"
set xlabel "Density of States [arb]"

set yzeroaxis lt 0
set yrange [-11:-6]
set xrange [-120:1000]

set ytics nomirror out
unset xtics

set border linewidth 1.5
set key spacing 1.2


plot 'febpycn4s_par_cn_b_huckel_orbE.dat'     u ($2*60):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'febpycn4s_par_cn_b_aligned.bind.DOS'    u 1:3 t '' w l lt 2 lw 3.5 lc rgb "#00008B",\
     'febpycn4s_par_cn_b_aligned.bind.DOS'    u 2:3 t '' w l lt -1 lw 3  lc rgb "#000000"
reset

# DOS with orbital energies
set term postscript enhanced color solid font "Helvetica,20"
set output "febpycn4t_par_cn_b_dos_1.eps"

set ylabel "Energy [eV]"
set xlabel "Density of States [arb]"

set yzeroaxis lt 0
set yrange [-18:-6]
set xrange [-120:1000]

set ytics nomirror out
unset xtics

set border linewidth 1.5
set key spacing 1.2


plot 'febpycn4t_par_cn_b_huckel_orbE.dat'     u ($2*60):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'febpycn4t_par_cn_b_aligned.bind.DOS'    u 1:3 t '' w l lt 2 lw 3.5 lc rgb "#00008B",\
     'febpycn4t_par_cn_b_aligned.bind.DOS'    u 2:3 t '' w l lt -1 lw 3  lc rgb "#000000"
reset

# DOS with orbital energies
set term postscript enhanced color solid font "Helvetica,20"
set output "febpycn4t_par_cn_b_dos_2.eps"

set ylabel "Energy [eV]"
set xlabel "Density of States [arb]"

set yzeroaxis lt 0
set yrange [-11:-6]
set xrange [-120:1000]

set ytics nomirror out
unset xtics

set border linewidth 1.5
set key spacing 1.2


plot 'febpycn4t_par_cn_b_huckel_orbE.dat'     u ($2*60):($1*27.21):(40):(0) t '' w boxxyerrorbars lt -1 lw 1 lc rgb "#000000",\
     'febpycn4t_par_cn_b_aligned.bind.DOS'    u 1:3 t '' w l lt 2 lw 3.5 lc rgb "#00008B",\
     'febpycn4t_par_cn_b_aligned.bind.DOS'    u 2:3 t '' w l lt -1 lw 3  lc rgb "#000000"
reset
