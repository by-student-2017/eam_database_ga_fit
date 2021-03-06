from scipy import optimize
import numpy as np
import commands
import sys
#----------------------------------------------------------------------
limit = 0.001*0.001
#limit = 0.035*0.035

file_tmp = 'EAM_code.tmp'
file_inp = 'EAM_code'

lammps_adress = "lmp"
cif2cell_adress = "cif2cell"

commands.getoutput("setenv OMP_NUM_THREADS 1")
num_core = commands.getoutput("grep 'core id' /proc/cpuinfo | sort -u | wc -l")
#pwscf_adress = "mpirun -np "+str(num_core)+" --allow-run-as-root pw.x"
#pwscf_adress = "mpirun -np "+str(num_core)+" pw.x"
pwscf_adress = "mpirun -np 2 pw.x"

satom = commands.getoutput("grep \"atomtype\" EAM.input | sed -e \"s/.*=//\" -e \"s/'//g\"")

commands.getoutput("chmod +x ./cfg2vasp/cfg2vasp")
#commands.getoutput("chmod +x pwscf2force")
commands.getoutput("chmod +x setinp")
commands.getoutput("./setinp")
commands.getoutput("mkdir cfg")
#commands.getoutput("mkdir work")
commands.getoutput("echo -n > energy.dat")

natom = commands.getoutput("cat data.in | awk '{if($2==\"atoms\"){print $1}}'")

temp_K = commands.getoutput("awk '{if($2==\"temp\"){print $4}}' in.lmp")
print "Lammps MD: "+temp_K+" K"

target = [0,0,0] # dummy data
y_str = [0] # dummy data


# fitting parameter
x0 = [ 3.729214887845323,2.3290014992384136,32.24270804951544,32.007667433005935,9.158612020064028,4.8629042541053105,0.4733176276699437,0.5651215999606349,0.5270630662058398,0.9590121891962463,-4.188430459388984,-0.3015466639985088,0.9916549582477155,-3.2170821313602405,-4.209653687521967,0.9203815966822847,-0.9868108353544846,0.6389713216163743,-4.213556880020658 ] # initial data

count = 0
#----------------------------------------------------------------------
def f(x):
  
  print "------------------------"
  global count
  count += 1
  print count

  fi = open(file_tmp,'r')
  text = fi.read().replace('re',str(x[0]).replace("[","").replace("]",""))
  text = text.replace('fe',str(x[1]).replace("[","").replace("]",""))
  text = text.replace('rhoe1',str(x[2]).replace("[","").replace("]",""))
  text = text.replace('rhoe2',str(x[3]).replace("[","").replace("]",""))
  text = text.replace('alpha',str(x[4]).replace("[","").replace("]",""))
  text = text.replace('beta',str(x[5]).replace("[","").replace("]",""))
  text = text.replace('Ap',str(x[6]).replace("[","").replace("]",""))
  text = text.replace('Bp',str(x[7]).replace("[","").replace("]",""))
  text = text.replace('kappa',str(x[8]).replace("[","").replace("]",""))
  text = text.replace('lambda',str(x[9]).replace("[","").replace("]",""))
  text = text.replace('Fn0',str(x[10]).replace("[","").replace("]",""))
  text = text.replace('Fn1',str(x[11]).replace("[","").replace("]",""))
  text = text.replace('Fn2',str(x[12]).replace("[","").replace("]",""))
  text = text.replace('Fn3',str(x[13]).replace("[","").replace("]",""))
  text = text.replace('F0',str(x[14]).replace("[","").replace("]",""))
  text = text.replace('F2',str(x[15]).replace("[","").replace("]",""))
  text = text.replace('F3',str(x[16]).replace("[","").replace("]",""))
  text = text.replace('eta',str(x[17]).replace("[","").replace("]",""))
  text = text.replace('Fep',str(x[18]).replace("[","").replace("]",""))
  fi.close

  with open(file_inp,'w') as f:
    print >> f, text

  commands.getoutput("./Zhou04_EAM_2 < EAM.input")
  commands.getoutput(lammps_adress+" < in.lmp")
  commands.getoutput("cp ./cfg/run.50.cfg run.50.cfg")
  commands.getoutput("./cfg2vasp/cfg2vasp run.50.cfg")
  commands.getoutput("python ./vasp2cif/vasp2cif.py run.50.vasp")
  #commands.getoutput(cif2cell_adress+" run.50.vasp.cif --no-reduce -p pwscf --pwscf-pseudo-PSLibrary-libdr=\"./potentials\" --setup-all --k-resolution=0.48 --pwscf-force=yes --pwscf-stress=yes --pwscf-run-type=scf -o pw.in") 
  #commands.getoutput(pwscf_adress+" < pw.scf.in > pw.out")
  #commands.getoutput("./pwscf2force >> config_potfit")
  commands.getoutput(cif2cell_adress+" run.50.vasp.cif --no-reduce -p lammps  -o data_fix.in")
  commands.getoutput(lammps_adress+" < in.lmp_ref_fix")

  lammps_get_data = "grep \"Total Energy\" log.lammps | tail -1 | awk '{printf \"%20.10f\",$4}'"
  target[0] = commands.getoutput(lammps_get_data)

  commands.getoutput(lammps_adress+" < in.lmp_fix")
  commands.getoutput("mv data.in.restart data.in")

  lammps_get_data = "grep \"Total Energy\" log.lammps | tail -1 | awk '{printf \"%20.10f\",$4}'"
  y_str[0] = commands.getoutput(lammps_get_data)

  print "lammps: ", float(y_str[0])

  print "lammps ref.:  ", float(target[0])

  diffe = float(target[0]) - float(y_str[0])
  print "diff: ", diffe, "[eV]"
  diffea = diffe/float(natom)
  print "diff/atom: ", diffea, "[eV/atom]"

  commands.getoutput("echo "+str(count)+" "+str(diffe)+" >> energy.dat")
 
  rhoin  = float(x[2])*0.85
  rhoout = float(x[2])*1.15
  print "---------------"
  print "F boundary 1, rho: "+str(rhoin)
  print "F boundary 2, rho: "+str(rhoout)
  commands.getoutput("cp "+satom+"_Zhou04.eam.alloy"+" Xx_Zhou04.eam.alloy")
  commands.getoutput("./plot")
  rhoin1  = commands.getoutput("cat F.plt | awk '{if($1<"+str(rhoin)+"){print $2}}' | tail -2 | head -1")
  rhoin2  = commands.getoutput("cat F.plt | awk '{if($1>"+str(rhoin)+"){print $2}}' | head -2 | tail -1")
  rhoout1 = commands.getoutput("cat F.plt | awk '{if($1<"+str(rhoout)+"){print $2}}' | tail -2 | head -1")
  rhoout2 = commands.getoutput("cat F.plt | awk '{if($1>"+str(rhoout)+"){print $2}}' | head -2 | tail -1")
  print "F near boundary, F: "+str(rhoin1)+" | "+str(rhoin2)+" | diff "+str(float(rhoin1) - float(rhoin2))
  print "F near boundary, F: "+str(rhoout1)+" | "+str(rhoout2)+" | diff "+str(float(rhoout1) - float(rhoout2))
  print "---------------"

  y = abs(diffea)**2 + 1000*abs(float(rhoin1) - float(rhoin2))**2 + 1000*abs(float(rhoout1) - float(rhoout2))**2

  print "Evaluate: ", y
  #print "Parameters:", x
  print "Parameters: x0 = "+"[ "+str(x[0])+","+str(x[1])+","+str(x[2])+","+str(x[3])+","+str(x[4])+","+str(x[5])+","+str(x[6])+","+str(x[7])+","+str(x[8])+","+str(x[9])+","+str(x[10])+","+str(x[11])+","+str(x[12])+","+str(x[13])+","+str(x[14])+","+str(x[15])+","+str(x[16])+","+str(x[17])+","+str(x[18])+" ]"
  print "------------------------"

  return y
#----------------------------------------------------------------------
res = optimize.minimize(f,x0,method='Nelder-Mead',tol=limit,options={'adaptive':True})
#res = optimize.minimize(f,x0,method='Nelder-Mead')
#res = optimize.minimize(f,x0,method='TNC')
#res = optimize.minimize(f,x0,method='Powell')
#res = optimize.minimize(f,x0,method='BFGS')
