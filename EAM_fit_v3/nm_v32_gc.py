from scipy import optimize
import numpy
import numpy as np
import commands
import sys
#----------------------------------------------------------------------
file_tmp = 'EAM_code_v32.tmp'
file_inp = 'EAM_code_v32'

cif2cell_adress = "cif2cell"

commands.getoutput("setenv OMP_NUM_THREADS 1")
num_core = commands.getoutput("grep 'core id' /proc/cpuinfo | sort -u | wc -l")
lammps_adress = "mpirun -np "+str(num_core)+" --allow-run-as-root lmp"
pwscf_adress = "mpirun -np "+str(num_core)+" --allow-run-as-root pw.x"
#lammps_adress = "mpirun -np "+str(num_core)+" lmp"
#pwscf_adress = "mpirun -np "+str(num_core)+" pw.x"
#lammps_adress = "mpirun -np 2 lmp"
#pwscf_adress = "mpirun -np 2 pw.x"

satom = commands.getoutput("grep \"atomtype\" EAM.input | sed -e \"s/.*=//\" -e \"s/'//g\"")

commands.getoutput("chmod +x ./cfg2vasp/cfg2vasp")
commands.getoutput("chmod +x pwscf2force")
commands.getoutput("cp in.lmp_temp_v2 in.lmp_temp")
commands.getoutput("chmod +x setinp")
commands.getoutput("./setinp")
commands.getoutput("mkdir cfg")
commands.getoutput("mkdir work")
commands.getoutput("echo -n > energy.dat")

natom = 5000
fxl = numpy.ones(int(natom)+1)
fyl = numpy.ones(int(natom)+1)
fzl = numpy.ones(int(natom)+1)
fxp = numpy.ones(int(natom)+1)
fyp = numpy.ones(int(natom)+1)
fzp = numpy.ones(int(natom)+1)

print "use struct.dat"
struct = commands.getoutput("awk '{if($1==\""+str(satom)+"\"){print $0}}' struct.dat")
struct_list = struct.split()
ntemp = int((len(struct_list)-1)/3 - 1)
temp = []
stru = []
weig = []
#if float(struct_list[3*ntemp+1]) <= 1073.0 :
#  ntemp = ntemp + 1
#  struct_list.append(1273.0)
#  struct_list.append("L")
#  struct_list.append(1.0)
for i in range(ntemp+1):
  temp.append(float(struct_list[3*i+1]))
  stru.append(struct_list[3*i+2])
  weig.append(float(struct_list[3*i+3]))
  t = temp[i]
  s = stru[i]
  commands.getoutput("cp in.lmp in.lmp_"+str(t)+"K")
  commands.getoutput("sed -i 's/YYYY/"+str(t)+"/' in.lmp_"+str(t)+"K")
  commands.getoutput("cp ./data/data.in."+str(s)+" data.in_"+str(t)+"K")
print "temperature: ",temp
print "structure  : ",stru
print "weight     : ",weig
#----------------------------------------------------------------------
print "read parameters from EAM_code_v32.init"
nline = commands.getoutput("grep -n "+str(satom)+" EAM_code_v32.init | head -1 | sed -e \"s/:.*//g\"")
print "read line: "+nline
check_satom = commands.getoutput("awk '{if(NR=="+str(nline)+"+0){print $1}}' EAM_code_v32.init | head -1")
print "fit element: "+check_satom
# fitting parameters
x0  = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+1){print $1}}' EAM_code_v32.init | head -1"))
x1  = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+2){print $1}}' EAM_code_v32.init | head -1"))
x2  = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+3){print $1}}' EAM_code_v32.init | head -1"))
x3  = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+4){print $1}}' EAM_code_v32.init | head -1"))
x4  = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+5){print $1}}' EAM_code_v32.init | head -1"))
x5  = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+6){print $1}}' EAM_code_v32.init | head -1"))
x6  = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+7){print $1}}' EAM_code_v32.init | head -1"))
x7  = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+8){print $1}}' EAM_code_v32.init | head -1"))
x8  = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+9){print $1}}' EAM_code_v32.init | head -1"))
x9  = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+10){print $1}}' EAM_code_v32.init | head -1"))
x10 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+11){print $1}}' EAM_code_v32.init | head -1"))
x11 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+12){print $1}}' EAM_code_v32.init | head -1"))
x12 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+13){print $1}}' EAM_code_v32.init | head -1"))
x13 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+14){print $1}}' EAM_code_v32.init | head -1"))
x14 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+15){print $1}}' EAM_code_v32.init | head -1"))
x15 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+16){print $1}}' EAM_code_v32.init | head -1"))
x16 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+17){print $1}}' EAM_code_v32.init | head -1"))
x17 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+18){print $1}}' EAM_code_v32.init | head -1"))
x18 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+19){print $1}}' EAM_code_v32.init | head -1"))
x19 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+20){print $1}}' EAM_code_v32.init | head -1"))
x20 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+21){print $1}}' EAM_code_v32.init | head -1"))
x21 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+22){print $1}}' EAM_code_v32.init | head -1"))
x22 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+23){print $1}}' EAM_code_v32.init | head -1"))
x23 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+24){print $1}}' EAM_code_v32.init | head -1"))
x24 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+25){print $1}}' EAM_code_v32.init | head -1"))
x25 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+26){print $1}}' EAM_code_v32.init | head -1"))
x26 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+27){print $1}}' EAM_code_v32.init | head -1"))
x27 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+28){print $1}}' EAM_code_v32.init | head -1"))
x28 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+29){print $1}}' EAM_code_v32.init | head -1"))
x29 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+30){print $1}}' EAM_code_v32.init | head -1"))
x30 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+31){print $1}}' EAM_code_v32.init | head -1"))
x31 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+32){print $1}}' EAM_code_v32.init | head -1"))
x32 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+33){print $1}}' EAM_code_v32.init | head -1"))
x33 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+34){print $1}}' EAM_code_v32.init | head -1"))
x34 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+35){print $1}}' EAM_code_v32.init | head -1"))
x35 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+36){print $1}}' EAM_code_v32.init | head -1"))
x36 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+37){print $1}}' EAM_code_v32.init | head -1"))
x37 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+38){print $1}}' EAM_code_v32.init | head -1"))
x38 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+39){print $1}}' EAM_code_v32.init | head -1"))
x39 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+42){print $1}}' EAM_code_v32.init | head -1"))
x40 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+43){print $1}}' EAM_code_v32.init | head -1"))
x41 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+44){print $1}}' EAM_code_v32.init | head -1"))
print "initial parameters: ",x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15,x16,x17,x18,x19,x20,x21,x22,x23,x24,x25,x26,x27,x28,x29,x30,x31,x32,x33,x34,x35,x36,x37,x38,x39,x40,x41
x0 = [x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15,x16,x17,x18,x19,x20,x21,x22,x23,x24,x25,x26,x27,x28,x29,x30,x31,x32,x33,x34,x35,x36,x37,x38,x39,x40,x41]

count = 0
#----------------------------------------------------------------------
def f(x):
  
  print "------------------------"
  global count
  count += 1
  print count

  fi = open(file_tmp,'r')
  text = fi.read().replace('re',str(x[0]).replace("[","").replace("]",""))
  text = text.replace('p0',str(x[1]).replace("[","").replace("]",""))
  text = text.replace('rhoe',str(x[2]).replace("[","").replace("]",""))
  text = text.replace('pk1',str(x[3]).replace("[","").replace("]",""))
  text = text.replace('pk2',str(x[4]).replace("[","").replace("]",""))
  text = text.replace('pk3',str(x[5]).replace("[","").replace("]",""))
  text = text.replace('pk4',str(x[6]).replace("[","").replace("]",""))
  text = text.replace('pk5',str(x[7]).replace("[","").replace("]",""))
  text = text.replace('pk6',str(x[8]).replace("[","").replace("]",""))
  text = text.replace('pk7',str(x[9]).replace("[","").replace("]",""))
  text = text.replace('pk8',str(x[10]).replace("[","").replace("]",""))
  text = text.replace('Fi0',str(x[11]).replace("[","").replace("]",""))
  text = text.replace('Fi1',str(x[12]).replace("[","").replace("]",""))
  text = text.replace('Fi2',str(x[13]).replace("[","").replace("]",""))
  text = text.replace('Fi3',str(x[14]).replace("[","").replace("]",""))
  text = text.replace('Fi4',str(x[15]).replace("[","").replace("]",""))
  text = text.replace('Fi5',str(x[16]).replace("[","").replace("]",""))
  text = text.replace('Fi6',str(x[17]).replace("[","").replace("]",""))
  text = text.replace('Fi7',str(x[18]).replace("[","").replace("]",""))
  text = text.replace('Fi8',str(x[19]).replace("[","").replace("]",""))
  text = text.replace('Fi9',str(x[20]).replace("[","").replace("]",""))
  text = text.replace('Fm2',str(x[21]).replace("[","").replace("]",""))
  text = text.replace('Fm3',str(x[22]).replace("[","").replace("]",""))
  text = text.replace('Fm4',str(x[23]).replace("[","").replace("]",""))
  text = text.replace('Fm5',str(x[24]).replace("[","").replace("]",""))
  text = text.replace('Fm6',str(x[25]).replace("[","").replace("]",""))
  text = text.replace('Fm7',str(x[26]).replace("[","").replace("]",""))
  text = text.replace('Fm8',str(x[27]).replace("[","").replace("]",""))
  text = text.replace('Fm9',str(x[28]).replace("[","").replace("]",""))
  text = text.replace('Fn0',str(x[29]).replace("[","").replace("]",""))
  text = text.replace('Fn1',str(x[30]).replace("[","").replace("]",""))
  text = text.replace('Fn2',str(x[31]).replace("[","").replace("]",""))
  text = text.replace('Fn3',str(x[32]).replace("[","").replace("]",""))
  text = text.replace('Fn4',str(x[33]).replace("[","").replace("]",""))
  text = text.replace('Fn5',str(x[34]).replace("[","").replace("]",""))
  text = text.replace('Fn6',str(x[35]).replace("[","").replace("]",""))
  text = text.replace('Fn7',str(x[36]).replace("[","").replace("]",""))
  text = text.replace('Fn8',str(x[37]).replace("[","").replace("]",""))
  text = text.replace('Fn9',str(x[38]).replace("[","").replace("]",""))
  text = text.replace('p1',str(x[39]).replace("[","").replace("]",""))
  text = text.replace('hc',str(x[40]).replace("[","").replace("]",""))
  text = text.replace('rhol',str(x[41]).replace("[","").replace("]",""))
  fi.close

  with open(file_inp,'w') as f:
    print >> f, text

  commands.getoutput("./Zhou04_EAM_v32 < EAM.input")

  tdiffea = 0.0
  tdiffp  = 0.0
  tdifff  = 0.0
  for t in temp:
    print "---------------"
    print "Temperature: "+str(t)+" [K]"
    if count > 20000 or count % int(10000*2.718**(-count/10000)+1) == 1: 
      commands.getoutput("mv data.in_"+str(t)+"K data.in")
      natom = commands.getoutput("awk '{if($2==\"atoms\"){print $1}}' data.in")
      commands.getoutput(lammps_adress+" < in.lmp_"+str(t)+"K")
      commands.getoutput("cp ./cfg/run.0.cfg run.50.cfg")
      commands.getoutput("./cfg2vasp/cfg2vasp run.50.cfg")
      commands.getoutput("python ./vasp2cif/vasp2cif.py run.50.vasp")
      commands.getoutput(cif2cell_adress+" run.50.vasp.cif --no-reduce -p pwscf --pwscf-pseudo-PSLibrary-libdr=\"./potentials\" --setup-all --k-resolution=0.48 --pwscf-force=yes --pwscf-stress=yes --pwscf-run-type=scf --pwscf-k-point-even=no  -o pw.in") 
      commands.getoutput("sed -i 's/\'pw\'/\'pw_"+str(t)+"K\'/g' pw.scf.in")
      commands.getoutput(pwscf_adress+" < pw.scf.in > pw.out")
      commands.getoutput(cif2cell_adress+" run.50.vasp.cif --no-reduce -p pwscf --pwscf-pseudo-PSLibrary-libdr=\"./potentials\" --setup-all --k-resolution=0.20 --pwscf-force=yes --pwscf-stress=yes --pwscf-run-type=scf -o pw.in") 
      commands.getoutput("sed -i 's/\'pw\'/\'pw_"+str(t)+"K\'/g' pw.scf.in")
      commands.getoutput(pwscf_adress+" < pw.scf.in > pw.out")
      commands.getoutput("./pwscf2force >> config_potfit_"+str(satom))
      commands.getoutput(cif2cell_adress+" run.50.vasp.cif --no-reduce -p lammps -o data_fix.in_"+str(t)+"K")
      commands.getoutput("cp data_fix.in_"+str(t)+"K data_fix.in")
      commands.getoutput(lammps_adress+" < in.lmp_fix")
      commands.getoutput("mv data.in.restart data.in_"+str(t)+"K")
      #
      commands.getoutput("./pwscf2force > config_"+str(t)+"K")
    else:
      commands.getoutput("cp data_fix.in_"+str(t)+"K data_fix.in")
      natom = commands.getoutput("awk '{if($2==\"atoms\"){print $1}}' data_fix.in")
      commands.getoutput(lammps_adress+" < in.lmp_fix")
    print "number of atoms: "+str(natom)

    # 1 bar = 0.0001 GPa
    # stress = -pressure
    #pxxl = commands.getoutput("awk '{if($1==\"pxxl\"){printf \"%10.8f\",$3*7.4028083e-11}}' log.lammps")
    #pyyl = commands.getoutput("awk '{if($1==\"pyyl\"){printf \"%10.8f\",$3*7.4028083e-11}}' log.lammps")
    #pzzl = commands.getoutput("awk '{if($1==\"pzzl\"){printf \"%10.8f\",$3*7.4028083e-11}}' log.lammps")
    #pxyl = commands.getoutput("awk '{if($1==\"pxyl\"){printf \"%10.8f\",$3*7.4028083e-11}}' log.lammps")
    #pxzl = commands.getoutput("awk '{if($1==\"pxzl\"){printf \"%10.8f\",$3*7.4028083e-11}}' log.lammps")
    #pyzl = commands.getoutput("awk '{if($1==\"pyzl\"){printf \"%10.8f\",$3*7.4028083e-11}}' log.lammps")
    #pxxp = commands.getoutput("awk '{if($1==\"#S\"){print -$2}}' config")
    #pyyp = commands.getoutput("awk '{if($1==\"#S\"){print -$3}}' config")
    #pzzp = commands.getoutput("awk '{if($1==\"#S\"){print -$4}}' config")
    #pxyp = commands.getoutput("awk '{if($1==\"#S\"){print -$5}}' config")
    #pxzp = commands.getoutput("awk '{if($1==\"#S\"){print -$6}}' config")
    #pyzp = commands.getoutput("awk '{if($1==\"#S\"){print -$7}}' config")
    #diffpxx = (float(pxxl) - float(pxxp))/(float(pxxp)+0.000000101)*100.0/6.0
    #diffpyy = (float(pyyl) - float(pyyp))/(float(pyyp)+0.000000101)*100.0/6.0
    #diffpzz = (float(pzzl) - float(pzzp))/(float(pzzp)+0.000000101)*100.0/6.0
    #diffpxy = (float(pxyl) - float(pxyp))/(float(pxyp)+0.000000101)*100.0/6.0
    #diffpxz = (float(pxzl) - float(pxzp))/(float(pxzp)+0.000000101)*100.0/6.0
    #diffpyz = (float(pyzl) - float(pyzp))/(float(pyzp)+0.000000101)*100.0/6.0
    #diffp = abs(diffpxx) + abs(diffpyy) + abs(diffpzz) + abs(diffpxy) + abs(diffpxz) + abs(diffpyz)
    #print "lammps: "+str(pxxl)+", "+str(pyyl)+", "+str(pzzl)+", "+str(pxyl)+", "+str(pxzl)+", "+str(pyzl)+" [eV/A^3]"
    #print "pwscf:  "+str(pxxp)+", "+str(pyyp)+", "+str(pzzp)+", "+str(pxyp)+", "+str(pxzp)+", "+str(pyzp)+" [eV/A^3]"
    #print "P diff (%): "+str(diffp)
    #print "---------------"
    diffp = 0.0

    # force
    difffx = 0.0
    difffy = 0.0
    difffz = 0.0
    difff  = 0.0
    for i in range(int(natom)):
      fxl[i] = commands.getoutput("awk '{if(NR==10+"+str(i)+"){printf \"%10.8f\",$7}}' trajectory.lammpstrj")
      fyl[i] = commands.getoutput("awk '{if(NR==10+"+str(i)+"){printf \"%10.8f\",$8}}' trajectory.lammpstrj")
      fzl[i] = commands.getoutput("awk '{if(NR==10+"+str(i)+"){printf \"%10.8f\",$9}}' trajectory.lammpstrj")
      fxp[i] = commands.getoutput("awk '{if(NR==11+"+str(i)+"){print $5}}' config_"+str(t)+"K")
      fyp[i] = commands.getoutput("awk '{if(NR==11+"+str(i)+"){print $6}}' config_"+str(t)+"K")
      fzp[i] = commands.getoutput("awk '{if(NR==11+"+str(i)+"){print $7}}' config_"+str(t)+"K")
      difffx = (float(fxl[i]) - float(fxp[i]))/(float(fxp[i])+0.000000101)*100.0/3.0/float(natom)
      difffy = (float(fyl[i]) - float(fyp[i]))/(float(fyp[i])+0.000000101)*100.0/3.0/float(natom)
      difffz = (float(fzl[i]) - float(fzp[i]))/(float(fzp[i])+0.000000101)*100.0/3.0/float(natom)
      difff  = difff + abs(difffx) + abs(difffy) + abs(difffz)
    print "lammps: "+str(fxl[0])+" : "+str(fyl[0])+" : "+str(fzl[0])+" [eV/A]"
    print "PWscf: "+str(fxp[0])+" : "+str(fyp[0])+" : "+str(fzp[0])+" [eV/A]"
    print "force diff (%): "+str(difff)
    print "---------------"

    lammps_get_data = "grep \"Total Energy\" log.lammps | tail -1 | awk '{printf \"%-20.10f\",$4}'"
    lmpe = commands.getoutput(lammps_get_data)

    pwe = commands.getoutput("awk '{if($1==\"#E\"){print $2}}' config_"+str(t)+"K")
    pwe = float(pwe) * float(natom)

    print "lammps: "+str(lmpe)+" [eV]"

    print "PWscf:  "+str(pwe)+" [eV]"

    diffe = float(pwe) - float(lmpe)
    print "diff: "+str(diffe)+" [eV]"
    diffea = float(diffe)/float(natom)
    print "diff/atom: "+str(diffea)+" [eV/atom]"
    commands.getoutput("echo "+str(count)+" "+str(diffe)+" >> energy.dat")

    for itw in range(ntemp+1):
      if t == temp[itw]:
        wt = weig[itw]

    tdiffea = tdiffea + float(diffea)*float(wt)
    tdiffp  = tdiffp  + float(diffp)*float(wt)
    tdifff  = tdifff  + float(difff)*float(wt)

  diffb  = commands.getoutput("cat diff.dat")
  print "F boundary, diff: "+str(diffb)
  print "---------------"

  y = float(tdiffea)**2 + 1000*float(diffb)**2 + 0.0000002*abs(tdiffp)**2 + 0.0000010*abs(tdifff)**2

  print "Evaluate: ", y
  #print "Parameters: ", x
  print "Parameters: x0 = "+"[ "+str(x[0])+","+str(x[1])+","+str(x[2])+","+str(x[3])+","+str(x[4])+","+str(x[5])+","+str(x[6])+","+str(x[7])+","+str(x[8])+","+str(x[9])+","+str(x[10])+","+str(x[11])+","+str(x[12])+","+str(x[13])+","+str(x[14])+","+str(x[15])+","+str(x[16])+","+str(x[17])+","+str(x[18])+","+str(x[19])+","+str(x[20])+","+str(x[21])+","+str(x[22])+","+str(x[23])+","+str(x[24])+","+str(x[25])+","+str(x[26])+","+str(x[27])+","+str(x[28])+","+str(x[29])+","+str(x[30])+","+str(x[31])+","+str(x[32])+","+str(x[33])+","+str(x[34])+","+str(x[35])+","+str(x[36])+","+str(x[37])+","+str(x[38])+","+str(x[39])+","+str(x[40])+","+str(x[41])+" ]"
  print "------------------------"

  return y
#----------------------------------------------------------------------
res = optimize.minimize(f,x0,method='Nelder-Mead',options={'adaptive':True})
#res = optimize.minimize(f,x0,method='Nelder-Mead')
#res = optimize.minimize(f,x0,method='TNC')
#res = optimize.minimize(f,x0,method='Powell')
#res = optimize.minimize(f,x0,method='BFGS')
