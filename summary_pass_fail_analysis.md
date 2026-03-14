# OpenFOAM10 Pass/Fail Error Analysis (Cases 1/2/3)

Reference: Basic/<case>/1/GT_files (comments ignored).
Exclusions: damBreakWithObstacle and Allrun.

## benchmark
- FAIL_OR_POOR: **30**

### Good / potentially pass examples

### Fail / error-analysis examples
- BernardCells/1 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - error file: log.blockMesh | snippet: l&, Foam::label&, Foam::cellList&)     in file meshes/polyMesh/polyMeshFromShapeMesh.C at line 324.  FOAM aborting  #0  Foam::error::printStack(Foam::Ostream&) at ??:? #1  Foam::er
- BernardCells/2 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - error file: log.buoyantFoam | snippet: l properties  Selecting thermodynamics package pureMixture<const<perfectGas<specie>>,sensibleInternalEnergy>   --> FOAM FATAL ERROR:  Unknown fluidThermo type pureMixture<const<per
- BernardCells/3 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - error file: log.blockMesh | snippet: l&, Foam::label&, Foam::cellList&)     in file meshes/polyMesh/polyMeshFromShapeMesh.C at line 324.  FOAM aborting  #0  Foam::error::printStack(Foam::Ostream&) at ??:? #1  Foam::er
- Cavity/1 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - error file: log.blockMesh | snippet: * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * // Create time  Reading "blockMeshDict"    --> FOAM FATAL ERROR:  Cannot find file "system/blockMeshDict"       
- Cavity/2 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - error file: log.pisoFoam | snippet:  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * // Create time  Create mesh for time = 0    --> FOAM FATAL IO ERROR:  keyword PISO is undefined in dictionary "/m
- Cavity/3 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - error file: log.pisoFoam | snippet: dlLibraryTable/dlLibraryTable.C at line 106     could not load "libfvMeshTools.so" Create mesh for time = 0    --> FOAM FATAL IO ERROR:  keyword PISO is undefined in dictionary "/m
- Cylinder/1 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - error file: log.blockMesh | snippet: m     "system/blockMeshDict" Creating block edges No non-planar block faces defined Creating topology blocks   --> FOAM FATAL IO ERROR:  Block hex (0 1 2 3 4 5 6 7) (20 20 1) simpl
- Cylinder/2 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - error file: log.blockMesh | snippet: eate time  Reading "blockMeshDict"  Creating block mesh from     "system/blockMeshDict" Creating block edges   --> FOAM FATAL IO ERROR:  wrong token type - expected int32_t, found 
- Cylinder/3 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - worst file mismatch: system/blockMeshDict (sim=0.201)
- counterFlowFlame2D/1 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - error file: log.blockMesh | snippet: m     "system/blockMeshDict" Creating block edges No non-planar block faces defined Creating topology blocks   --> FOAM FATAL IO ERROR:  Block hex (0 1 2 3 4 5 6 7) (50 50 1) simpl
- counterFlowFlame2D/2 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - error file: log.blockMesh | snippet: * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * // Create time  Reading "blockMeshDict"    --> FOAM FATAL ERROR:  Cannot find file "system/blockMeshDict"       
- counterFlowFlame2D/3 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - error file: log.reactingFoam | snippet: sient mode with 1 outer corrector PIMPLE: Operating solver in PISO mode   Reading thermophysical properties    --> FOAM FATAL IO ERROR:  keyword thermoType is undefined in dictiona
- forwardStep/1 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - error file: log.blockMesh | snippet: :faceListList&, Foam::label) const     in file meshes/polyMesh/polyMeshFromShapeMesh.C at line 118.  FOAM aborting  #0  Foam::error::printStack(Foam::Ostream&) at ??:? #1  Foam::er
- forwardStep/2 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - error file: log.rhoCentralFoam | snippet: ionaryEntry::stream() const     in file db/dictionary/dictionaryEntry/dictionaryEntry.C at line 83.  FOAM aborting  #0  Foam::error::printStack(Foam::Ostream&) at ??:? #1  Foam::IO
- forwardStep/3 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - error file: log.blockMesh | snippet: :faceListList&, Foam::label) const     in file meshes/polyMesh/polyMeshFromShapeMesh.C at line 118.  FOAM aborting  #0  Foam::error::printStack(Foam::Ostream&) at ??:? #1  Foam::er
- obliqueShock/1 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - error file: log.blockMesh | snippet: * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * // Create time  Reading "blockMeshDict"    --> FOAM FATAL ERROR:  Cannot find file "system/blockMeshDict"       
- obliqueShock/2 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - error file: log.rhoCentralFoam | snippet: me  Create mesh for time = 0  Reading thermophysical properties  Selecting thermodynamics package perfectGas   --> FOAM FATAL ERROR:  Unknown psiThermo type perfectGas  Valid psiTh
- obliqueShock/3 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - error file: log.blockMesh | snippet: l&, Foam::label&, Foam::cellList&)     in file meshes/polyMesh/polyMeshFromShapeMesh.C at line 324.  FOAM aborting  #0  Foam::error::printStack(Foam::Ostream&) at ??:? #1  Foam::er
- pitzDaily/1 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - error file: log.blockMesh | snippet: m     "system/blockMeshDict" Creating block edges No non-planar block faces defined Creating topology blocks   --> FOAM FATAL IO ERROR:  Expected a ')' while reading VectorSpace<Fo
- pitzDaily/2 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - error file: log.pimpleFoam | snippet: :min(const dimensionSet&, const dimensionSet&)     in file dimensionSet/dimensionSet.C at line 245.  FOAM aborting  #0  Foam::error::printStack(Foam::Ostream&) at ??:? #1  Foam::er
- pitzDaily/3 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - error file: log.blockMesh | snippet:  No non-planar block faces defined Creating topology blocks Creating topology patches  Creating block mesh topology #0  Foam::error::printStack(Foam::Ostream&) at ??:? #1  Foam::si
- shallowWaterWithSquareBump/1 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - error file: log.setFields | snippet: ator()(Foam::Istream&) const     in file setFields.C at line 179     field type 0.01 not currently supported   --> FOAM FATAL IO ERROR:  wrong token type - expected word, found on 
- shallowWaterWithSquareBump/2 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - error file: log.setFields | snippet: * * * * * * * // Create time  Create mesh for time = 0  Reading "setFieldsDict"  Setting field region values   --> FOAM FATAL IO ERROR:  keyword regions is undefined in dictionary 
- shallowWaterWithSquareBump/3 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - error file: Allrun.err | snippet: ryIO.C at line 129     Reading system/controlDict     found on line 49 an error     expected either } or EOF   --> FOAM FATAL IO ERROR:   Essential value for keyword 'points' not s
- squareBend/1 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - error file: log.blockMesh | snippet: m     "system/blockMeshDict" Creating block edges No non-planar block faces defined Creating topology blocks   --> FOAM FATAL IO ERROR:  Block hex (0 1 3 2 4 5 7 6) (20 20 20) simp

## standard
- FAIL_OR_POOR: **30**

### Good / potentially pass examples

### Fail / error-analysis examples
- BernardCells/1 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - worst file mismatch: system/controlDict (sim=0.240)
- BernardCells/2 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - worst file mismatch: system/controlDict (sim=0.240)
- BernardCells/3 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - worst file mismatch: system/controlDict (sim=0.240)
- Cavity/1 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - worst file mismatch: system/fvSchemes (sim=0.328)
- Cavity/2 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - worst file mismatch: system/fvSchemes (sim=0.326)
- Cavity/3 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - worst file mismatch: constant/momentumTransport (sim=0.421)
- Cylinder/1 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - worst file mismatch: system/blockMeshDict (sim=0.057)
- Cylinder/2 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - worst file mismatch: system/blockMeshDict (sim=0.075)
- Cylinder/3 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - worst file mismatch: system/blockMeshDict (sim=0.056)
- counterFlowFlame2D/1 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - worst file mismatch: constant/thermo.compressibleGas (sim=0.015)
- counterFlowFlame2D/2 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - worst file mismatch: constant/thermo.compressibleGas (sim=0.015)
- counterFlowFlame2D/3 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - worst file mismatch: constant/thermo.compressibleGas (sim=0.005)
- forwardStep/1 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - worst file mismatch: system/fvSolution (sim=0.255)
- forwardStep/2 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - worst file mismatch: system/fvSolution (sim=0.267)
- forwardStep/3 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - worst file mismatch: system/fvSolution (sim=0.215)
- obliqueShock/1 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - worst file mismatch: system/controlDict (sim=0.085)
- obliqueShock/2 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - worst file mismatch: system/controlDict (sim=0.104)
- obliqueShock/3 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - worst file mismatch: system/controlDict (sim=0.085)
- pitzDaily/1 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - worst file mismatch: system/blockMeshDict (sim=0.307)
- pitzDaily/2 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - worst file mismatch: system/blockMeshDict (sim=0.307)
- pitzDaily/3 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - worst file mismatch: system/blockMeshDict (sim=0.307)
- shallowWaterWithSquareBump/1 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - worst file mismatch: system/setFieldsDict (sim=0.305)
- shallowWaterWithSquareBump/2 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - worst file mismatch: system/setFieldsDict (sim=0.305)
- shallowWaterWithSquareBump/3 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - worst file mismatch: constant/gravitationalProperties (sim=0.000)
- squareBend/1 | FAIL_OR_POOR | Insufficient GT alignment and/or explicit errors and/or no execution artifact.
  - worst file mismatch: constant/polyMesh/faces (sim=0.000)

## Overall alignment winner
- benchmark: mean avg_similarity=0.4061
- standard: mean avg_similarity=0.5192
- Winner: **standard**