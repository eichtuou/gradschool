'''
This script generates input files utilized for a set of DFT functional benchmarking calculations.
'''
# complex name
cname='fetpy2q_par'

# functinals list
flist=['b3lyp','b3lyp+d2','b3lyp+d3','apf','apfd','m06','m06l','m052x','wb97xd','b97d','b97d3']

# fragment of route section
route2='\
    pseudo=cards\n\
    integral=ultrafine\n\
    opt(tight)\n\
    scf(maxconventionalcycles=100,vtl,xqc)\n\
    scrf(pcm,solvent=water,read)\n\
    freq\n\
    nosymm\n\
\n'

# charge, multiplicity, coordinates, basis set 
coords='\
2 5\n\
 Fe        8.368753       11.323506        6.229264\n\
 N         9.907834       11.534924        7.340529\n\
 C         9.923216       12.528955        8.246494\n\
 C        11.029720       12.706256        9.074615\n\
 C        12.108407       11.833178        8.936824\n\
 C        12.073303       10.809522        7.990513\n\
 C        10.938324       10.683333        7.192097\n\
 H        12.907725       10.129338        7.881289\n\
 H        12.979730       11.950445        9.569614\n\
 H        11.052522       13.500994        9.808342\n\
 H         8.605167        9.923982        8.977060\n\
 H         8.177184        9.083627        4.109516\n\
 H        10.749830       13.110986        5.403454\n\
 H         5.924910       13.199286        6.444315\n\
 N         9.478487        9.804780        5.530754\n\
 C         8.686544       13.329231        8.220709\n\
 N         7.302115       10.082766        7.391747\n\
 N         6.832667       11.107502        5.114591\n\
 C         9.150400        8.943147        4.562141\n\
 C         6.102993        9.721844        6.856187\n\
 N         8.917266       12.497601        4.697223\n\
 C        10.001234        7.921794        4.151141\n\
 H         9.690370        7.248448        3.362389\n\
 C        10.689730        9.681382        6.141137\n\
 N         7.774327       12.912528        7.299230\n\
 C         5.833888       10.309723        5.532647\n\
 C         7.643491        9.607200        8.594091\n\
 C         7.997626       12.560843        3.694640\n\
 C        11.240623        7.791890        4.770599\n\
 H        11.927459        7.007972        4.474506\n\
 C         6.791833       11.748928        3.933045\n\
 C         5.229097        8.874544        7.528638\n\
 H         4.280624        8.605443        7.081964\n\
 C         4.646533       10.774089        3.505545\n\
 H         3.781394       10.641172        2.867352\n\
 C         7.231805       15.099747        8.928776\n\
 H         7.021413       15.952298        9.563479\n\
 C         8.441082       14.420076        9.047647\n\
 H         9.183407       14.732975        9.770641\n\
 C         8.209364       13.334435        2.558659\n\
 H         7.461646       13.369740        1.776963\n\
 C        10.051548       13.196162        4.580740\n\
 C         5.691760       11.599032        3.091095\n\
 H         5.648598       12.107759        2.137110\n\
 C         4.707419       10.118928        4.735083\n\
 H         3.899152        9.477122        5.059820\n\
 C         6.615073       13.570240        7.191421\n\
 C        10.329680       13.989589        3.472105\n\
 H        11.262492       14.536990        3.424013\n\
 C        11.589813        8.684732        5.780091\n\
 H        12.546823        8.608609        6.279764\n\
 C         9.392481       14.059546        2.445723\n\
 H         9.577027       14.668861        1.569000\n\
 C         6.302899       14.668812        7.986248\n\
 H         5.350677       15.168633        7.860997\n\
 C         6.818959        8.755096        9.322144\n\
 H         7.140149        8.396943       10.292061\n\
 C         5.592288        8.383761        8.779847\n\
 H         4.925550        7.722794        9.320741\n\
\n\
C H N 0\n\
6-311g*\n\
****\n\
Fe 0\n\
SDD\n\
****\n\
\n\
FE 0\n\
SDD\n\
\n\
\n'


# generate input files
for i in flist:
    #title section
    title=cname+'_'+i+'\n\n'        

    # add empirical dispersion
    if i == 'b3lyp+d2' or i == 'b3lyp+d3':
        disp='\
    empiricaldispersion=g'+i[-2:]+'\n'

    # fragment of route section
        route1='\
%chk='+cname+'.chk\n\
%mem=16GB\n\
%nproc=8\n\
#p  '+i[:5]+'/gen\n'

        # write input files
        filename=cname+'_'+i+'.com'
        fo=open(filename, 'w')
        buff=route1+disp+route2+title+coords
        fo.write(buff)
        fo.close()

    else:
        route1='\
%chk='+cname+'.chk\n\
%mem=16GB\n\
%nproc=8\n\
#p  '+i+'/gen\n'
        filename=cname+'_'+i+'.com'
        fo=open(filename, 'w')
        buff=route1+route2+title+coords
        fo.write(buff)
        fo.close()

