C author: X. W. Zhou, xzhou@sandia.gov
C updates by: Lucas Hale lucas.hale@nist.gov
C show difference of F boundary value by By Student
c      open(unit=5,file='a.i')
      call inter
c      close(5)
      call writeset
      stop
      end
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c main subroutine.                                                c
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
      subroutine inter
      implicit real*8 (a-h,o-z)
      implicit integer*8 (i-m)
      character*80 atomtype,atommatch,outfile,outelem
      namelist /funccard/ atomtype
      common /pass1/ re(16),fe(16),rhoe(16),alpha(16),
     *   beta(16),beta1(16),A(16),B(16),cai(16),ramda(16),
     *   ramda1(16),
     *   Fi0(16),Fi1(16),Fi2(16),Fi3(16),Fi4(16),Fi5(16),Fi6(16),
     *   Fm2(16),Fm3(16),Fm4(16),Fm5(16),Fm6(16),
     *   Fn0(16),Fn1(16),Fn2(16),Fn3(16),
     *   rhoin(16),rhoout(16),rhol(16),
     *   rhoh(16),rhos(16)
      common /pass2/ amass(16),Fr(5000,16),rhor(5000,16),
     *   z2r(5000,16,16),blat(16),drho,dr,rc,outfile,outelem
      common /pass3/ ielement(16),ntypes,nrho,nr
      ntypes=0
10    continue
      atomtype='none'
      read(5,funccard)
      if (atomtype .eq. 'none') goto 1200
      open(unit=10,file='EAM_code_v11',form='FORMATTED',status='OLD')
11    read(10,9501,end=1210)atommatch
9501  format(a80)
      if (atomtype .eq. atommatch) then
         ntypes=ntypes+1
         length=len_trim(outfile)
         if (length .eq. len(outfile)) then
            outfile = atomtype
         else
            outfile = outfile(1:length)//atomtype
         endif
         length=len_trim(outelem)
         if (length .eq. len(outelem)) then
            outelem = atomtype
         else
            outelem = outelem(1:length)//' '//atomtype
         endif
         read(10,*) re(ntypes)
         read(10,*) fe(ntypes)
         read(10,*) rhoe(ntypes)
         read(10,*) rhos(ntypes)
         read(10,*) alpha(ntypes)
         read(10,*) beta(ntypes)
         read(10,*) A(ntypes)
         read(10,*) B(ntypes)
         read(10,*) cai(ntypes)
         read(10,*) ramda(ntypes)
         read(10,*) Fi0(ntypes)
         read(10,*) Fi1(ntypes)
         read(10,*) Fi2(ntypes)
         read(10,*) Fi3(ntypes)
         read(10,*) Fi4(ntypes)
         read(10,*) Fi5(ntypes)
         read(10,*) Fi6(ntypes)
         read(10,*) Fm2(ntypes)
         read(10,*) Fm3(ntypes)
         read(10,*) Fm4(ntypes)
         read(10,*) Fm5(ntypes)
         read(10,*) Fm6(ntypes)
         read(10,*) Fn0(ntypes)
         read(10,*) Fn1(ntypes)
         read(10,*) Fn2(ntypes)
         read(10,*) Fn3(ntypes)
         read(10,*) ielement(ntypes)
         read(10,*) amass(ntypes)
         read(10,*) Fm4(ntypes)
         read(10,*) beta1(ntypes)
         read(10,*) ramda1(ntypes)
         read(10,*) rhol(ntypes)
         read(10,*) rhoh(ntypes)
         blat(ntypes)=sqrt(2.0d0)*re(ntypes)
         rhoin(ntypes)=rhol(ntypes)*rhoe(ntypes)
         rhoout(ntypes)=rhoh(ntypes)*rhoe(ntypes)
      else
         do 1 i=1,27
1        read(10,*)vtmp
         goto 11
      endif
      close(10)
      goto 10
1210  write(6,*)'error: atom type ',atomtype,' not found'
      stop
1200  continue
      nr=2000
      nrho=2000
      alatmax=blat(1)
      rhoemax=rhoe(1)
      do 2 i=2,ntypes
         if (alatmax .lt. blat(i)) alatmax=blat(i)
         if (rhoemax .lt. rhoe(i)) rhoemax=rhoe(i)
2     continue
      rc=sqrt(10.0d0)/2.0d0*alatmax
      rst=0.5d0
      dr=rc/(nr-1.0d0)
      fmax=-1.0d0
      do 3 i1=1,ntypes
      do 3 i2=1,i1
      if ( i1 .eq. i2) then
         do 4 i=1,nr
            r=(i-1)*dr
            if (r .lt. rst) r=rst
            call prof(i1,r,fvalue)
            if (fmax .lt. fvalue) fmax=fvalue
            rhor(i,i1)=fvalue
            call pair(i1,i2,r,psi)
            z2r(i,i1,i2)=r*psi
4        continue
      else
         do 5 i=1,nr
            r=(i-1)*dr
            if (r .lt. rst) r=rst
            call pair(i1,i2,r,psi)
            z2r(i,i1,i2)=r*psi
            z2r(i,i2,i1)=z2r(i,i1,i2)
5        continue
      endif
3     continue
      rhom=fmax
      if (rhom .lt. 2.0d0*rhoemax) rhom=2.0d0*rhoemax
      if (rhom .lt. 100.0d0) rhom=100.0d0
      drho=rhom/(nrho-1.0d0)
      do 6 it=1,ntypes
      do 7 i=1,nrho
         rhoF=(i-1)*drho
         if (i .eq. 1) rhoF=0.0d0
         call embed(it,rhoF,emb)
         Fr(i,it)=emb
7     continue
      do 20 i=1,nrho
         rhoF=(i-1)*drho
         if ( (rhoF .ge. rhoin(it)) .and.
     *        (rhoF .lt. rhoin(it)+drho) ) then
           call embed0(it,rhoF,emb)
           embb11 = emb
           embb12 = Fr(i,it)
         endif
         if ( (rhoF .ge. rhoout(it)) .and. 
     *        (rhoF .lt. rhoout(it)+drho) ) then
           call embed0(it,rhoF,emb)
           embb21 = emb
           embb22 = Fr(i,it)
         endif
20    continue
      diff = abs(embb11 - embb12) + abs(embb21 - embb22)
6     continue
      open(unit=50,file='diff.dat',form='FORMATTED',status='OLD')
      write(50,*) diff
      close(50)
      return
      end
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c This subroutine calculates the electron density.                c
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
      subroutine prof(it,r,f)
      implicit real*8 (a-h,o-z)
      implicit integer*8 (i-m)
      common /pass1/ re(16),fe(16),rhoe(16),alpha(16),
     *   beta(16),beta1(16),A(16),B(16),cai(16),ramda(16),
     *   ramda1(16),
     *   Fi0(16),Fi1(16),Fi2(16),Fi3(16),Fi4(16),Fi5(16),Fi6(16),
     *   Fm2(16),Fm3(16),Fm4(16),Fm5(16),Fm6(16),
     *   Fn0(16),Fn1(16),Fn2(16),Fn3(16),
     *   rhoin(16),rhoout(16),rhol(16),
     *   rhoh(16),rhos(16)
      f=fe(it)*exp(-beta1(it)*(r/re(it)-1.0d0))
      f=f/(1.0d0+(r/re(it)-ramda1(it))**20)
      return
      end
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c This subroutine calculates the pair potential.                  c
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
      subroutine pair(it1,it2,r,psi)
      implicit real*8 (a-h,o-z)
      implicit integer*8 (i-m)
      common /pass1/ re(16),fe(16),rhoe(16),alpha(16),
     *   beta(16),beta1(16),A(16),B(16),cai(16),ramda(16),
     *   ramda1(16),
     *   Fi0(16),Fi1(16),Fi2(16),Fi3(16),Fi4(16),Fi5(16),Fi6(16),
     *   Fm2(16),Fm3(16),Fm4(16),Fm5(16),Fm6(16),
     *   Fn0(16),Fn1(16),Fn2(16),Fn3(16),
     *   rhoin(16),rhoout(16),rhol(16),
     *   rhoh(16),rhos(16)
      if (it1 .eq. it2) then
         psi1=A(it1)*exp(-alpha(it1)*(r/re(it1)-1.0d0))
         psi1=psi1/(1.0d0+(r/re(it1)-cai(it1))**20)
         psi2=B(it1)*exp(-beta(it1)*(r/re(it1)-1.0d0))
         psi2=psi2/(1.0d0+(r/re(it1)-ramda(it1))**20)
         psi=psi1-psi2
      else
         psi1=A(it1)*exp(-alpha(it1)*(r/re(it1)-1.0d0))
         psi1=psi1/(1.0d0+(r/re(it1)-cai(it1))**20)
         psi2=B(it1)*exp(-beta(it1)*(r/re(it1)-1.0d0))
         psi2=psi2/(1.0d0+(r/re(it1)-ramda(it1))**20)
         psia=psi1-psi2
         psi1=A(it2)*exp(-alpha(it2)*(r/re(it2)-1.0d0))
         psi1=psi1/(1.0d0+(r/re(it2)-cai(it2))**20)
         psi2=B(it2)*exp(-beta(it2)*(r/re(it2)-1.0d0))
         psi2=psi2/(1.0d0+(r/re(it2)-ramda(it2))**20)
         psib=psi1-psi2
         call prof(it1,r,f1)
         call prof(it2,r,f2)
         psi=0.5d0*(f2/f1*psia+f1/f2*psib)
      endif
      return
      end
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c This subroutine calculates the embedding energy.                c
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
      subroutine embed(it,rho,emb)
      implicit real*8 (a-h,o-z)
      implicit integer*8 (i-m)
      common /pass1/ re(16),fe(16),rhoe(16),alpha(16),
     *   beta(16),beta1(16),A(16),B(16),cai(16),ramda(16),
     *   ramda1(16),
     *   Fi0(16),Fi1(16),Fi2(16),Fi3(16),Fi4(16),Fi5(16),Fi6(16),
     *   Fm2(16),Fm3(16),Fm4(16),Fm5(16),Fm6(16),
     *   Fn0(16),Fn1(16),Fn2(16),Fn3(16),
     *   rhoin(16),rhoout(16),rhol(16),
     *   rhoh(16),rhos(16)
c      if (rho .lt. rhoe(it)) then
c         Fm33=Fm3(it)
c      else 
c         Fm33=Fm4(it)
c      endif
      if (rho .eq. 0.0d0) then
        emb = 0.0d0
      else if (rho .lt. rhoin(it)) then
         emb=Fi0(it)+
     *       Fi1(it)*(rho/rhoin(it)-1.0d0)+
     *       Fi2(it)*(rho/rhoin(it)-1.0d0)**2+
     *       Fi3(it)*(rho/rhoin(it)-1.0d0)**3+
     *       Fi4(it)*(rho/rhoin(it)-1.0d0)**4+
     *       Fi5(it)*(rho/rhoin(it)-1.0d0)**5+
     *       Fi6(it)*(rho/rhoin(it)-1.0d0)**6
      else if (rho .lt. rhoout(it)) then
         emb=Fi0(it)+
     *       Fi1(it)*(rho/rhoin(it)-1.0d0)+
     *       Fm2(it)*(rho/rhoin(it)-1.0d0)**2+
     *       Fm3(it)*(rho/rhoin(it)-1.0d0)**3+
     *       Fm4(it)*(rho/rhoin(it)-1.0d0)**4+
     *       Fm5(it)*(rho/rhoin(it)-1.0d0)**5+
     *       Fm6(it)*(rho/rhoin(it)-1.0d0)**6
      else
         emb=Fn0(it)+
     *       Fn1(it)*(rho/rhoout(it)-1.0d0)+
     *       Fn2(it)*(rho/rhoout(it)-1.0d0)**2+
     *       Fn3(it)*(rho/rhoout(it)-1.0d0)**3
c         emb=Fn(it)*(1.0d0-fnn(it)*log(rho/rhos(it)))*
c     *       (rho/rhos(it))**fnn(it)
      endif
      return
      end
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c This subroutine calculates the embedding energy for boundary.   c
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
      subroutine embed0(it,rho,emb)
      implicit real*8 (a-h,o-z)
      implicit integer*8 (i-m)
      common /pass1/ re(16),fe(16),rhoe(16),alpha(16),
     *   beta(16),beta1(16),A(16),B(16),cai(16),ramda(16),
     *   ramda1(16),
     *   Fi0(16),Fi1(16),Fi2(16),Fi3(16),Fi4(16),Fi5(16),Fi6(16),
     *   Fm2(16),Fm3(16),Fm4(16),Fm5(16),Fm6(16),
     *   Fn0(16),Fn1(16),Fn2(16),Fn3(16),
     *   rhoin(16),rhoout(16),rhol(16),
     *   rhoh(16),rhos(16)
c      if (rho .lt. rhoe(it)) then
c         Fm33=Fm3(it)
c      else 
c         Fm33=Fm4(it)
c      endif
      if (rho .eq. 0.0d0) then
        emb = 0.0d0
      else if (rho .lt. rhoin(it)) then
         emb=Fi0(it)+
     *       Fi1(it)*(rho/rhoin(it)-1.0d0)+
     *       Fm2(it)*(rho/rhoin(it)-1.0d0)**2+
     *       Fm3(it)*(rho/rhoin(it)-1.0d0)**3+
     *       Fm4(it)*(rho/rhoin(it)-1.0d0)**4+
     *       Fm5(it)*(rho/rhoin(it)-1.0d0)**5+
     *       Fm6(it)*(rho/rhoin(it)-1.0d0)**6
      else if (rho .lt. rhoout(it)) then
         emb=Fn0(it)+
     *       Fn1(it)*(rho/rhoout(it)-1.0d0)+
     *       Fn2(it)*(rho/rhoout(it)-1.0d0)**2+
     *       Fn3(it)*(rho/rhoout(it)-1.0d0)**3
      else
         emb=Fi0(it)+
     *       Fi1(it)*(rho/rhoin(it)-1.0d0)+
     *       Fm2(it)*(rho/rhoin(it)-1.0d0)**2+
     *       Fm3(it)*(rho/rhoin(it)-1.0d0)**3+
     *       Fm4(it)*(rho/rhoin(it)-1.0d0)**4+
     *       Fm5(it)*(rho/rhoin(it)-1.0d0)**5+
     *       Fm6(it)*(rho/rhoin(it)-1.0d0)**6
      endif
      return
      end
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c write out set file.                                             c
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
      subroutine writeset
      implicit real*8 (a-h,o-z)
      implicit integer*8 (i-m)
      character*80 outfile,outelem
      common /pass1/ re(16),fe(16),rhoe(16),alpha(16),
     *   beta(16),beta1(16),A(16),B(16),cai(16),ramda(16),
     *   ramda1(16),
     *   Fi0(16),Fi1(16),Fi2(16),Fi3(16),Fi4(16),Fi5(16),Fi6(16),
     *   Fm2(16),Fm3(16),Fm4(16),Fm5(16),Fm6(16),
     *   Fn0(16),Fn1(16),Fn2(16),Fn3(16),
     *   rhoin(16),rhoout(16),rhol(16),
     *   rhoh(16),rhos(16)
      common /pass2/ amass(16),Fr(5000,16),rhor(5000,16),
     *   z2r(5000,16,16),blat(16),drho,dr,rc,outfile,outelem
      common /pass3/ ielement(16),ntypes,nrho,nr
      character*80 struc
      struc='ZZZ'
      outfile = outfile(1:index(outfile,' ')-1)//'_Zhou04.eam.alloy'
      open(unit=1,file=outfile)
      write(1,*) ' DATE: 2018-03-30 ',
     *   'CONTRIBUTOR: Xiaowang Zhou xzhou@sandia.gov and ',
     *   'Lucas Hale lucas.hale@nist.gov ',
     *   'CITATION: X. W. Zhou, R. A. Johnson, ',
     *   'H. N. G. Wadley, Phys. Rev. B, 69, 144113(2004)'
      write(1,*) ' Generated from Zhou04_create_v2.f'
      write(1,*) ' Fixes precision issues with older version'
      write(1,8)ntypes,outelem
8     format(i5,' ',a24)
      write(1,9)nrho,drho,nr,dr,rc
9     format(i5,e24.16,i5,2e24.16)
      do 10 i=1,ntypes
      write(1,11)ielement(i),amass(i),blat(i),struc
      write(1,12)(Fr(j,i),j=1,nrho)
      write(1,12)(rhor(j,i),j=1,nr)
10    continue
11    format(i5,2g15.5,a8)
12    format(5e24.16)
      do 13 i1=1,ntypes
      do 13 i2=1,i1
      write(1,12)(z2r(i,i1,i2),i=1,nr)
13    continue
      close(1)
      return
      end
