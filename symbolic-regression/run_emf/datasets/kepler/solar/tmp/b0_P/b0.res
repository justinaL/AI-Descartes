===========================================================================
 BARON version 26.5.28. Built: OSX-64 2026-05-28 22:29:23           
 Running on machine s-MacBook.local

 BARON is a product of The Optimization Firm. For more information and 
 related optimization and data analytics products visit https://minlp.com.


 If you publish work using this software, please cite publications from
 https://minlp.com/baron-publications, such as: 

 Zhang, Y. and N. V. Sahinidis, Solving continuous and discrete
 nonlinear programs with BARON, Comput Optim Appl, 92, 1123-1161, 2025. 
 https://doi.org/10.1007/s10589-024-00633-0
===========================================================================
 This BARON run may utilize the following subsolver(s)
 For LP/MIP/QP: CLP/CBC                                         
 For NLP: IPOPT, FILTERSQP
===========================================================================
    The options used in solving the problem are as follows:
       maxtime        =  0.6000E+02
       maxiter        =      -1
       numsol         =       1
       firstfeas      =       0
       firstloc       =       0
       cutoff         =  0.1000E+52
       target         = -0.1000E+52
       epsa           =  0.1000E-03
       epsr           =  0.1000E-02
       relgaptype     =       4
       deltaterm      =       0
       deltaa         =  0.1000E+52
       deltar         =  0.1000E+01
       deltat         = -0.1000E+03
       boxtol         =  0.1000E-07
       isoltol        =  0.1000E-03
       absconfeastol  =  0.1000E-05
       relconfeastol  =  0.0000E+00
       absintfeastol  =  0.1000E-04
       relintfeastol  =  0.0000E+00
       primalcstol    =  0.1000E-04
       dualcstol      =  0.1000E-04
       dualfeastol    =  0.1000E-04
       ectol          =  0.1000E-04
       results        =       1
       summary        =       1
       times          =       1
       wantdual       =       1
       prtimefreq     =  0.1000E+01
       prfreq         = 1000000
       prlevel        =       1
       lpsol          =       8
       nlpsol         =      -1
       allowminos     =       0
       allowsnopt     =       0
       allowexternal  =       0
       allowipopt     =       1
       allowfiltersd  =       0
       allowfiltersqp =       1
       allowcplex     =       0
       allowxpress    =       0
       allowcbc       =       1
       allowhsl       =       1
       allowhighs     =       0
       dolocal        =       1
       numloc         =      20
       locres         =       0
       nouter1        =       4
       noutpervar     =       4
       noutiter       =       4
       outgrid        =      20
       tdo            =       1
       mdo            =       1
       obttdo         =       1
       lbttdo         =       1
       pdo            =      -2
       brvarstra      =       0
       brptstra       =       0
       nodesel        =       0
       compiis        =       0
       iisint         =       1
       iisorder       =      -1
       images         =      -1
       threads        =       1
       userrel        =       0
       usergencuts    =       0
       usersearch     =       0
       usertighten    =       0
       problemisconvex=       0
===========================================================================
 >>> Preprocessing found feasible solution
 >>> Objective value is:           4646.6460651299994424335     
 >>> Corresponding solution vector is:
 >>> Variable no.              Value
 >>>       1             0.0000000000000000000000     
 >>>       2             0.0000000000000000000000     
 >>>       3             0.0000000000000000000000     
 >>>       4             0.0000000000000000000000     
 >>>       5             0.0000000000000000000000     

 >>> No dual information is available
 >>> Variable no.              Marginal
 >>>       1             0.0000000000000000000000     
 >>>       2             0.0000000000000000000000     
 >>>       3             0.0000000000000000000000     
 >>>       4             0.0000000000000000000000     
 >>>       5             0.0000000000000000000000     
 >>> Constraint no.            Price
 >>>       1             0.0000000000000000000000     
 >>>       2             0.0000000000000000000000     
 >>>       3             0.0000000000000000000000     
 >>>       4             0.0000000000000000000000     
 >>>       5             0.0000000000000000000000     

 Doing local search
 >>> Preprocessing found feasible solution
 >>> Objective value is:           4646.6380425435181678040     
 >>> Corresponding solution vector is:
 >>> Variable no.              Value
 >>>       1             3.0000000000000000000000     
 >>>       2            -3.0000000000000000000000     
 >>>       3             3.0000000000000000000000     
 >>>       4            -3.0000000000000000000000     
 >>>       5            0.87793907715108820383985E-006

 >>> No dual information is available
 >>> Variable no.              Marginal
 >>>       1             0.0000000000000000000000     
 >>>       2             0.0000000000000000000000     
 >>>       3             0.0000000000000000000000     
 >>>       4             0.0000000000000000000000     
 >>>       5             0.0000000000000000000000     
 >>> Constraint no.            Price
 >>>       1             0.0000000000000000000000     
 >>>       2             0.0000000000000000000000     
 >>>       3             0.0000000000000000000000     
 >>>       4             0.0000000000000000000000     
 >>>       5             0.0000000000000000000000     

 Solving bounding LP
 Starting multi-start local search
 Done with local search
===========================================================================

 >>> Better Solution Found at Iteration           1
 >>> Objective value is:           291.48044333457812626875     
 >>> Corresponding solution vector is:
 >>> Variable no.              Value
 >>>       1             1.0000000000000000000000     
 >>>       2             1.0000000000000000000000     
 >>>       3             3.0000000000000000000000     
 >>>       4             3.0000000000000000000000     
 >>>       5            0.13582496696341289752104E-003

 >>> No dual information is available
 >>> Variable no.              Marginal
 >>>       1             0.0000000000000000000000     
 >>>       2             0.0000000000000000000000     
 >>>       3             0.0000000000000000000000     
 >>>       4             0.0000000000000000000000     
 >>>       5             0.0000000000000000000000     
 >>> Constraint no.            Price
 >>>       1             0.0000000000000000000000     
 >>>       2             0.0000000000000000000000     
 >>>       3             0.0000000000000000000000     
 >>>       4             0.0000000000000000000000     
 >>>       5             0.0000000000000000000000     


 >>> Better Solution Found at Iteration           6
 >>> Objective value is:           262.43518212399015965275     
 >>> Corresponding solution vector is:
 >>> Variable no.              Value
 >>>       1             1.0000000000000000000000     
 >>>       2            -1.0000000000000000000000     
 >>>       3             3.0000000000000000000000     
 >>>       4             3.0000000000000000000000     
 >>>       5            0.40058788498484827755863E-001

 >>> No dual information is available
 >>> Variable no.              Marginal
 >>>       1             0.0000000000000000000000     
 >>>       2             0.0000000000000000000000     
 >>>       3             0.0000000000000000000000     
 >>>       4             0.0000000000000000000000     
 >>>       5             0.0000000000000000000000     
 >>> Constraint no.            Price
 >>>       1             0.0000000000000000000000     
 >>>       2             0.0000000000000000000000     
 >>>       3             0.0000000000000000000000     
 >>>       4             0.0000000000000000000000     
 >>>       5             0.0000000000000000000000     


 >>> Better Solution Found at Iteration           8
 >>> Objective value is:           123.88811314273162622612     
 >>> Corresponding solution vector is:
 >>> Variable no.              Value
 >>>       1             0.0000000000000000000000     
 >>>       2             0.0000000000000000000000     
 >>>       3             1.0000000000000000000000     
 >>>       4             1.0000000000000000000000     
 >>>       5             1.8009521025479475753173     

 >>> No dual information is available
 >>> Variable no.              Marginal
 >>>       1             0.0000000000000000000000     
 >>>       2             0.0000000000000000000000     
 >>>       3             0.0000000000000000000000     
 >>>       4             0.0000000000000000000000     
 >>>       5             0.0000000000000000000000     
 >>> Constraint no.            Price
 >>>       1             0.0000000000000000000000     
 >>>       2             0.0000000000000000000000     
 >>>       3             0.0000000000000000000000     
 >>>       4             0.0000000000000000000000     
 >>>       5             0.0000000000000000000000     


 >>> Better Solution Found at Iteration           9
 >>> Objective value is:           58.668527129031545541693     
 >>> Corresponding solution vector is:
 >>> Variable no.              Value
 >>>       1             0.0000000000000000000000     
 >>>       2             0.0000000000000000000000     
 >>>       3             2.0000000000000000000000     
 >>>       4             2.0000000000000000000000     
 >>>       5            0.69122612822081305750110E-001

 >>> No dual information is available
 >>> Variable no.              Marginal
 >>>       1             0.0000000000000000000000     
 >>>       2             0.0000000000000000000000     
 >>>       3             0.0000000000000000000000     
 >>>       4             0.0000000000000000000000     
 >>>       5             0.0000000000000000000000     
 >>> Constraint no.            Price
 >>>       1             0.0000000000000000000000     
 >>>       2             0.0000000000000000000000     
 >>>       3             0.0000000000000000000000     
 >>>       4             0.0000000000000000000000     
 >>>       5             0.0000000000000000000000     



                         *** Normal completion ***            


 >>> Objective value is:           58.668527129031545541693     
 >>> Corresponding solution vector is:
 >>> Variable no.              Value
 >>>       1             0.0000000000000000000000     
 >>>       2             0.0000000000000000000000     
 >>>       3             2.0000000000000000000000     
 >>>       4             2.0000000000000000000000     
 >>>       5            0.69122612822081305750110E-001

 >>> Corresponding dual solution vector is:
 >>> Variable no.              Marginal
 >>>       1             0.0000000000000000000000     
 >>>       2            -78.612520600851468088877     
 >>>       3             0.0000000000000000000000     
 >>>       4             197.18314145449150487366     
 >>>       5            -.50098571124923552133623E-011
 >>> Constraint no.            Price
 >>>       1             0.0000000000000000000000     
 >>>       2             0.0000000000000000000000     
 >>>       3             0.0000000000000000000000     
 >>>       4             0.0000000000000000000000     
 >>>       5             0.0000000000000000000000     


The best solution found is:

  variable		xlo			 xbest				xup
  exp0m_abs			0			 0.00000000000000000000000e+00	3
  exp0m			-3			 0.00000000000000000000000e+00	3
  exp0d_abs			0			 2.00000000000000000000000e+00	3
  exp0d			-3			 2.00000000000000000000000e+00	3
  C0			-100			 6.91226128220813057501104e-02	100

The above solution has an objective value of:  58.668527129031545541693     
