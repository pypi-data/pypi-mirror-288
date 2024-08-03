# This file is part of the mlhpbf project. License: See LICENSE
import os, sys

try:
    # mlhp.py script folder
    path = os.path.abspath( os.path.dirname(sys.argv[0]) );
    
    # Try to open path/mlhpPythonPath containing the python module path. This
    # file is written as post build command after compiling pymlhpcore.
    with open( os.path.join( path, 'mlhpPythonPath' ), 'r') as f:
        sys.path.append( os.path.normpath( f.read( ).splitlines( )[0] ) )
        
except IOError: 
    pass
        
from pymlhpbf import *

import mlhp
import math
from dataclasses import dataclass

vtudefault="RawBinary"

class units:
    m = 1000.0
    cm = 1e-2 * m
    mm = 1e-3 * m
    um = 1e-6 * m
    s = 1.0
    ms = 1e-3 * s
    kg = 1000.0
    g = 1e-3 * kg
    N = 1.0
    J = N * m
    kJ = 1e3 * J
    W = J / s
    kW = 1e3 * W
    C = 1.0
    Pa = N / ( m * m )
    MPa = 1e6 * Pa
    GPa = 1e9 * Pa

# Pass single value or interpolate using two lists of temperatures and values.
# extrapolate can be "constant", "linear", or "polynomial".
def temperatureFunction(temperatures=None, values=None, degree=1, extrapolate="constant"):
    if values is None:
        if not isinstance(temperatures, float): raise ValueError("Single value must be of type float.")
        return mlhp.constantInterpolation([0.0], [temperatures])
        
    extrapolateStr = "default" if extrapolate.lower( ) == "polynomial" else extrapolate
    if degree == 1:
        return mlhp.linearInterpolation(temperatures, values, extrapolateStr)
    else:
        return mlhp.splineInterpolation(temperatures, values, degree, extrapolateStr)

def makePowder(material, densityScaling=0.5, conductivityScaling=0.08, youngsModulusScaling=1e-4):
    if not isinstance(material, Material): 
        raise ValueError(f"Invalid data type for material ({type(material)}).")
        
    scale = lambda f, factor : temperatureFunction(factor * f(20.0)[0])
    powder = Material()
    powder.initialized          = material.initialized
    powder.name                 = material.name + "Powder"
    powder.density              = scale(material.density, densityScaling)
    powder.specificHeatCapacity = scale(material.specificHeatCapacity, 1.0)
    powder.heatConductivity     = scale(material.heatConductivity, conductivityScaling)
    powder.plasticModelSelector = 0.0
    powder.solidTemperature     = material.solidTemperature    
    powder.liquidTemperature    = material.liquidTemperature   
    powder.latentHeatOfFusion   = material.latentHeatOfFusion  
    powder.regularization       = material.regularization      
    powder.thermalExpansionCoefficient = temperatureFunction(0.0)
    powder.youngsModulus        = temperatureFunction(youngsModulusScaling)    
    powder.poissonRatio         = temperatureFunction(0.0)
    powder.yieldStress          = temperatureFunction(1e50)        
    powder.hardening            = temperatureFunction(0.0)
    powder.plasticModelSelector = 0.0
    
    return powder
    
def makeAir(epsilon=1e-5, material=makeMaterial("IN625")):
    if not isinstance(epsilon, (int, float, bool)): 
        raise ValueError("Invalid data type for epsilon")
    return makePowder(material, epsilon, epsilon, epsilon)
    
def temperatureBC(faceIndex, temperature):
    def process(thermalProblem, tstate):
        sliced = mlhp.sliceLast(process.function, tstate.time)
        return mlhp.integrateDirichletDofs(sliced, tstate.basis, [process.iface])
    
    process.function=mlhp.scalarField(4, temperature) if isinstance(temperature, float) else temperature
    process.iface=faceIndex
    
    return process

def thermalVtuOutput(filebase, interval=1, writemode=vtudefault, functions=[]):
    def process(thermalProblem, tstate):
        if tstate.index % process.interval == 0:
            processors = [mlhp.functionProcessor(mlhp.sliceLast(f, tstate.time), 
                "VolumeSource" + str(i)) for i, f in enumerate(thermalProblem.volumeSources)]
            processors += [mlhp.solutionProcessor(3, tstate.dofs, "Temperature")]
            sliceF = lambda f : mlhp.sliceLast(f, tstate.time) if isinstance(f, mlhp.ScalarFunction4D) else f
            processors += [mlhp.functionProcessor(sliceF(f), name) for f, name in functions]
            postmesh = mlhp.gridOnCells(mlhp.degreeOffsetResolution(tstate.basis, 2))
            writer = mlhp.PVtuOutput(filename=process.path + "_thermal_" + 
                str(tstate.index // process.interval), writemode=writemode)
            mlhp.writeBasisOutput(tstate.basis, postmesh, writer, processors)
    
    process.path=filebase
    process.interval=interval
    
    return process

def materialVtuOutput(filebase, interval=1, writemode=vtudefault):
    def process(thermalProblem, tstate):
        if tstate.index % process.interval == 0:
            processors = [mlhp.cellDataProcessor(3, tstate.history.data( ), "MaterialState")]
            postmesh = mlhp.gridOnCells([1]*3, mlhp.PostprocessTopologies.Volumes)
            writer = mlhp.PVtuOutput(filename=process.path + "_material_" + 
                str(tstate.index // process.interval), writemode=writemode)
            mlhp.writeMeshOutput(tstate.history.grid( ), postmesh, writer, processors)
    
    process.path=filebase
    process.interval=interval
    
    return process
    
def thermalEvaluator(state):
    return mlhp.scalarEvaluator(state.basis, state.dofs)

def meltingTemperature(materials, phi=0.5):
    if "structure" in materials:
        return (1.0 - phi) * materials["structure"].solidTemperature + phi * materials["structure"].liquidTemperature
    else:
        return 1e50
        
def meltPoolContourOutput(output, interval=1, resolution=None, writemode=vtudefault):
    def process(thermalProblem, tstate):
        if tstate.index % process.interval == 0:
            threshold = meltingTemperature(thermalProblem.materials)
            function = mlhp.implicitThreshold(thermalEvaluator(tstate), threshold)
            postmesh = mlhp.marchingCubesBoundary(function, 
                mlhp.degreeOffsetResolution(tstate.basis) if resolution is None else resolution)
            writer = mlhp.DataAccumulator( )   
            if isinstance(process.output, str):
                writer = mlhp.PVtuOutput(filename=process.output + "_meltpool_" + 
                    str(tstate.index // process.interval), writemode=writemode)
            mlhp.writeMeshOutput(tstate.mesh, postmesh, writer, [])
            if not isinstance(process.output, str):
                process.output(writer.mesh( ) )

    process.output=output
    process.interval=interval
    
    return process
 
def meltPoolBoundsPrinter(interval=1, resolution=None):
    def meltPoolBoundsCallback( mesh ):
        points = mesh.points( )
        bounds = [[1e50, 1e50, 1e50], [-1e50, -1e50, -1e50]]
        for ipoint in range(int(len(points)/3)):
            for icoord in range(3):
                bounds[0][icoord] = min(bounds[0][icoord], points[3*ipoint + icoord])
                bounds[1][icoord] = max(bounds[1][icoord], points[3*ipoint + icoord])
        print(f"    melt pool bounds: {[max(u - l, 0.0) for l, u in zip(*bounds)]}", flush=True)
    return meltPoolContourOutput(meltPoolBoundsCallback, interval, resolution)
  
def createMesh(min, max, elementSize, layerHeight=0.0, zfactor=1.0):
    return mlhp.makeGrid(createMeshTicks(min, max, elementSize, layerHeight, zfactor))
  
def laserRefinement(laserTrack, laserSigma, laserSpeed, depth):
    def refinement(problem, state0, state1):
        refinementPoints = [
            # delay, sigma (refinement width), depth (maximum refinement depth), zfactor
            LaserRefinementPoint(0.00*units.ms, 4*laserSigma+0.01*units.mm, depth+0.4, 0.5),
            LaserRefinementPoint(0.60*units.ms, 4*laserSigma+0.07*units.mm, depth-0.5, 0.5),
            LaserRefinementPoint(6.00*units.ms, 4*laserSigma+0.40*units.mm, depth-1.5, 0.8),
            LaserRefinementPoint(30.0*units.ms, 4*laserSigma+0.90*units.mm, depth-2.5, 1.0),
            LaserRefinementPoint(0.10*units.s,  4*laserSigma+1.10*units.mm, depth-3.0, 1.0)]
        return laserTrackPointRefinement(laserTrack, refinementPoints, state1.time, mlhp.maxdegree(state0.basis) + 2)
    refinement.laserTrack=laserTrack
    refinement.laserSigma=laserSigma
    refinement.laserSpeed=laserSpeed
    refinement.depth=depth
    return refinement

class ThermalProblem:
    def __init__(self):
        self.dirichlet   = []
        #self.residual    = []
        self.postprocess = []
        self.degree = 1
        self.theta = 1
        self.ambientTemperature = 25.0
        self.volumeSources = []
        self.refinements = []
        self.nfields = 1
        
    def addPostprocessor(self, postprocessor):
        self.postprocess.append(postprocessor)
        
    def addDirichletBC(self, condition):
        self.dirichlet.append(condition)
        
    def addSource(self, source):
        self.volumeSources.append(source)
        
    def addRefinement(self, refinement):
        self.refinements.append(refinement)
        
    def setMaterials(self, materials):
        self.materials = materials  
        
@dataclass
class State:
    time: float
    index: int
    mesh: None
    basis: None
    dofs: None
    history: None
    
def makeThermalState(thermalProblem, mesh, part=None, srefinement=0, powderHeight=0.0, time=0.0, index=0):
    if part is None:
        domain = mlhp.implicitHalfspace([0.0, 0.0, 0.0], [0.0, 0.0, 1.0])
    elif isinstance(part, (float, int)):
        domain = mlhp.implicitHalfspace([0.0, 0.0, part], [0.0, 0.0, 1.0])
    elif isinstance(part, mlhp.ImplicitFunction3D):
        domain = part
    else:
        raise ValueError("Invalid data type for part.")
        
    history = initializeThermalHistory(mesh, domain, srefinement, powderHeight, nseedpoints=4)
    refinedMesh = mlhp.makeRefinedGrid(mesh)
    basis = mlhp.makeHpTrunkSpace(refinedMesh, thermalProblem.degree, nfields=thermalProblem.nfields)
    dofs = mlhp.projectOnto(basis, mlhp.scalarField(3, thermalProblem.ambientTemperature))
    state = State(time, index, refinedMesh, basis, dofs, history)
    dirichletDofs = mlhp.combineDirichletDofs([f(thermalProblem, state) for f in thermalProblem.dirichlet])
    state.dofs = mlhp.inflateDofs(mlhp.split(state.dofs, dirichletDofs[0])[1], dirichletDofs)
    return state

def thermalTimeStep(thermalProblem, tstate0, deltaT):
    tstate1 = State(time    = tstate0.time + deltaT,
                    index   = tstate0.index + 1,
                    mesh    = mlhp.makeRefinedGrid(tstate0.mesh.baseGrid()),
                    basis   = None,
                    dofs    = None,
                    history = tstate0.history)
    
    if len(thermalProblem.refinements):
        refinements = [r(thermalProblem, tstate0, tstate1) for r in thermalProblem.refinements]
        tstate1.mesh.refine(mlhp.refinementOr(refinements))
        
    tstate1.basis = mlhp.makeHpTrunkSpace(tstate1.mesh, thermalProblem.degree)
    
    print(f"    thermal problem: {tstate1.basis.nelements( )} elements, {tstate1.basis.ndof( )} dofs", flush=True)
    
    # Gather dirichlet dofs
    dirichletDofs = mlhp.combineDirichletDofs([f(thermalProblem, tstate1) for f in thermalProblem.dirichlet])
    
    # Project solution from previous state
    K = mlhp.allocateUnsymmetricSparseMatrix(tstate1.basis)
    F = mlhp.allocateVectorWithSameSize(K)

    l2Integrand = mlhp.l2BasisProjectionIntegrand(3, tstate0.dofs)

    mlhp.integrateOnDomain(tstate0.basis, tstate1.basis, l2Integrand, [K, F])

    solve = mlhp.makeCGSolver(1e-12)
    projectedDofs0 = solve(K, F)
    tstate1.dofs = projectedDofs0
    
    del K, F
    
    # Prepare nonlinear iterations
    K = mlhp.allocateUnsymmetricSparseMatrix(tstate1.basis, dirichletDofs[0])
    F = mlhp.allocateVectorWithSameSize(K)
    F0 = mlhp.allocateVectorWithSameSize(K)
    
    projectionIntegrand = makeThermalInitializationIntegrand( thermalProblem.materials, 
        thermalProblem.volumeSources, tstate0.history, tstate0.dofs, tstate0.time, deltaT, thermalProblem.theta )
        
    mlhp.integrateOnDomain( tstate0.basis, tstate1.basis, projectionIntegrand, [F0], dirichletDofs=dirichletDofs)
    
    norm0 = 0.0
    print("    || F || --> ",end="", flush=True);

    # Newton-Raphson iterations
    for i in range(40):
        F = mlhp.copy(F0)
        mlhp.fill(K, 0.0 )
        
        dirichletIncrement = computeDirichletIncrement(dirichletDofs, tstate1.dofs, -1.0)
        
        domainIntegrand = makeTimeSteppingThermalIntegrand(thermalProblem.materials, tstate1.history, 
            projectedDofs0, tstate1.dofs, tstate1.time - tstate0.time, thermalProblem.theta)

        quadrature = mlhp.meshProjectionQuadrature(tstate1.history.grid( ))
        
        mlhp.integrateOnDomain(tstate1.basis, domainIntegrand, [K, F], 
            quadrature=quadrature, dirichletDofs=dirichletIncrement)

        norm1 = mlhp.norm(F)
        norm0 = norm1 if i == 0 else norm0

        print(f"{norm1:.2e} ", end="", flush=True)
        
        dx = mlhp.inflateDofs(solve( K, F ), dirichletIncrement)
        
        tstate1.dofs = mlhp.add(tstate1.dofs, dx, -1.0)
        
        if i == 0:
            tstate1.history = updateHistory(tstate0.history, tstate1.basis, tstate1.dofs, 
                meltingTemperature(thermalProblem.materials, phi=0.5) )
        
        if norm1 / norm0 <= 1e-6 or norm1 < 1e-11:
            break;
        if ( i + 1 ) % 6 == 0: 
            print("\n                ", end="", flush=True)
            
    tstate1.history = updateHistory(tstate0.history, tstate1.basis, tstate1.dofs, 
        meltingTemperature(thermalProblem.materials, phi=0.5) )

    print("", flush=True)
    
    return tstate1
       
def computeThermalProblem( thermalProblem, tstate0, deltaT, duration ):
    nsteps = int( math.ceil( duration / deltaT ) );
    realDT = duration / nsteps;
    
    print(f"Integrating thermal problem:", flush=True)
    print(f"    duration        = {duration}", flush=True)
    print(f"    number of steps = {nsteps}", flush=True)
    print(f"    step size       = {realDT}", flush=True)

    for pp in thermalProblem.postprocess:
        pp(thermalProblem, tstate0)

    for istep in range(nsteps):
        print(f"Time step {istep + 1} / {nsteps}", flush=True)
        
        tstate1 = thermalTimeStep(thermalProblem, tstate0, realDT)

        for pp in thermalProblem.postprocess:
            pp(thermalProblem, tstate1)

        tstate0 = tstate1

    return tstate0

def computeSteadyStateThermal(thermalProblem, tstate, laserVelocity):

    print(f"Computing steady-state problem ({tstate.basis.nelements( )} elements, {tstate.basis.ndof( )} dofs)", flush=True)
    
    # Gather dirichlet dofs
    dirichletDofs = mlhp.combineDirichletDofs([f(thermalProblem, tstate) for f in thermalProblem.dirichlet])

    # Prepare for nonlinear iterations
    K = mlhp.allocateUnsymmetricSparseMatrix(tstate.basis, dirichletDofs[0])
    F = mlhp.allocateVectorWithSameSize(K)
    tstate.dofs = mlhp.DoubleVector(tstate.basis.ndof( ), 0.0)

    slicedSources = [mlhp.sliceLast(f, tstate.time) for f in thermalProblem.volumeSources]

    norm0 = 1.0
    print("    || F || --> ",end="", flush=True);

    for i in range(40):
        mlhp.fill(F, 0.0);
        mlhp.fill(K, 0.0);
        
        dirichletIncrement = computeDirichletIncrement(dirichletDofs, tstate.dofs, -1.0)
        
        domainIntegrand = makeSteadyStateThermalIntegrand(thermalProblem.materials, 
            slicedSources, tstate.history, tstate.dofs, laserVelocity)

        quadrature = mlhp.meshProjectionQuadrature(tstate.history.grid( ))
        
        mlhp.integrateOnDomain(tstate.basis, domainIntegrand, [K, F], 
            quadrature=quadrature, dirichletDofs=dirichletIncrement)

        norm1 = mlhp.norm(F)
        norm0 = norm1 if i == 0 else norm0

        print(f"{norm1:.2e} ", end="", flush=True)
        
        P = mlhp.additiveSchwarzPreconditioner(K, tstate.basis, dirichletIncrement[0])
        dx = mlhp.bicgstab(K, F, preconditioner=P, maxit=1000, tolerance=1e-12)
        dx = mlhp.inflateDofs(dx, dirichletIncrement)

        tstate.dofs = mlhp.add(tstate.dofs, dx, -1.0)
        
        if norm1 / norm0 <= 1e-6 or norm1 < 1e-11:
            break;
        if ( i + 1 ) % 6 == 0: 
            print("\n                ", end="", flush=True)
        
    print("", flush=True)
    
    del K, F, dirichletDofs
    
    for pp in thermalProblem.postprocess:
        pp(thermalProblem, tstate)
    
def mechanicalVtuOutput(filebase, interval=1, writemode=vtudefault, functions=[]):
    def process(mechanicalProblem, mstate):
        if mstate.index % process.interval == 0:
            processors = []
            #processors = [mlhp.functionProcessor(mlhp.sliceLast(f, mstate.time), 
            #    "VolumeSource" + str(i)) for i, f in enumerate(thermalProblem.volumeSources)]
            processors += [mlhp.solutionProcessor(3, mstate.dofs, "Displacement")]
            #sliceF = lambda f : mlhp.sliceLast(f, mstate.time) if isinstance(f, mlhp.ScalarFunction4D) else f
            #processors += [mlhp.functionProcessor(sliceF(f), name) for f, name in functions]
            postmesh = mlhp.gridOnCells(mlhp.degreeOffsetResolution(mstate.basis))
            writer = mlhp.PVtuOutput(filename=process.path + "_mechanical_" + 
                str(mstate.index // process.interval), writemode=writemode)
            mlhp.writeBasisOutput(mstate.basis, postmesh, writer, processors)
    
    process.path=filebase
    process.interval=interval
    
    return process


class MechanicalProblem:
    def __init__(self):
        self.dirichlet   = []
        self.degree      = 1
        #self.residual    = []
        self.postprocess = []
        self.degree = 1
        self.theta = 1
        self.ambientTemperature = 25.0
        self.refinements = []
        self.nfields = 3
        
    def addPostprocessor(self, postprocessor):
        self.postprocess.append(postprocessor)
        
    def addDirichletBC(self, condition):
        self.dirichlet.append(condition)
        
    def addRefinement(self, refinement):
        self.refinements.append(refinement)
        
    def setMaterials(self, materials):
        self.materials = materials  
     
def makeMechanicalState(mechanicalProblem, mesh, part=None, time=0.0, index=0):
    domain = part if part is not None else mlhp.implicitHalfspace([0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
    refinedMesh = mlhp.makeRefinedGrid(mesh)
    basis = mlhp.makeHpTrunkSpace(refinedMesh, mechanicalProblem.degree, nfields=mechanicalProblem.nfields)
    #history = initializeHistory(mesh, domain, srefinement, powderHeight, nseedpoints=4)
    history = initializeMechanicalHistory(basis, mlhp.maxdegree(basis) + 1)
    dofs = mlhp.projectOnto(basis, mlhp.vectorField(3, [0.0]*3))
    state = State(time, index, refinedMesh, basis, dofs, history)
    dirichletDofs = mlhp.combineDirichletDofs([f(mechanicalProblem, state) for f in mechanicalProblem.dirichlet])
    state.dofs = mlhp.inflateDofs(mlhp.split(state.dofs, dirichletDofs[0])[1], dirichletDofs)
    return state

def mechanicalTimeStep(mechanicalProblem, mstate0, time1, thermalEvaluator):
    if mstate0.time > time1: 
        raise ValueError( "Previous mechanical time before next thermal time")
        
    mstate1 = State(time    = time1,
                    index   = mstate0.index + 1,
                    mesh    = mlhp.makeRefinedGrid(mstate0.mesh.baseGrid()),
                    basis   = None,
                    dofs    = None,
                    history = mstate0.history.clone( ))
                    
    mstate1.basis = mlhp.makeHpTrunkSpace(mstate1.mesh, degrees=mechanicalProblem.degree, nfields=mechanicalProblem.nfields)
    
    print(f"    mechanical problem: {mstate1.basis.nelements( )} elements, {mstate1.basis.ndof( )} dofs", flush=True)
    
    # Gather dirichlet dofs
    dirichletDofs = mlhp.combineDirichletDofs([f(mechanicalProblem, mstate1) for f in mechanicalProblem.dirichlet])
    
    # Project solution from previous state
    K = mlhp.allocateUnsymmetricSparseMatrix(mstate1.basis)
    F = mlhp.allocateVectorWithSameSize(K)

    l2Integrand = mlhp.l2BasisProjectionIntegrand(3, mstate0.dofs)

    mlhp.integrateOnDomain(mstate0.basis, mstate1.basis, l2Integrand, [K, F])

    solve = mlhp.makeCGSolver(1e-12)
    projectedDofs0 = solve(K, F)
    mstate1.dofs = projectedDofs0
    
    del K, F
    
    # Prepare nonlinear iterations
    K = mlhp.allocateUnsymmetricSparseMatrix(mstate1.basis, dirichletDofs[0])
    F = mlhp.allocateVectorWithSameSize(K)
    
    norm0 = 0.0
    print("    || F || --> ",end="", flush=True);

    # Newton-Raphson iterations
    for i in range(4):
        mlhp.fill(K, 0.0)
        mlhp.fill(F, 0.0)
        
        dirichletIncrement = computeDirichletIncrement(dirichletDofs, mstate1.dofs, -1.0)
        dofIncrement = mlhp.add(mstate1.dofs, projectedDofs0, -1.0)
        
        kinematics = mlhp.smallStrainKinematics(3)
        material = makeJ2Plasticity(mstate0.history, mstate1.history, thermalEvaluator)
        
        domainIntegrand = nonlinearStaticDomainIntegrand(kinematics, material, dofIncrement, mlhp.vectorField(3, [0.0]*3))
        
        mlhp.integrateOnDomain(mstate1.basis, domainIntegrand, [K, F], dirichletDofs=dirichletIncrement)
    
        norm1 = mlhp.norm(F)
        norm0 = norm1 if i == 0 else norm0
    
        print(f"{norm1:.2e} ", end="", flush=True)
        
        dx = mlhp.inflateDofs(solve( K, F ), dirichletIncrement)
        
        mstate1.dofs = mlhp.add(mstate1.dofs, dx)
        
        if norm1 / norm0 <= 1e-6 or norm1 < 1e-11:
            break;
        if ( i + 1 ) % 6 == 0: 
            print("\n                ", end="", flush=True)
            
    print("", flush=True)
   
    return mstate1

def computeThermomechanicalProblem( thermalProblem, mechanicalProblem, tstate0, mstate0, deltaT, duration ):
    nsteps = int( math.ceil( duration / deltaT ) );
    realDT = duration / nsteps;
    
    print(f"Integrating thermomechanical problem:", flush=True)
    print(f"    duration        = {duration}", flush=True)
    print(f"    number of steps = {nsteps}", flush=True)
    print(f"    step size       = {realDT}", flush=True)

    for pp in thermalProblem.postprocess:
        pp(thermalProblem, tstate0)
    for pp in mechanicalProblem.postprocess:
        pp(mechanicalProblem, mstate0)

    for istep in range(nsteps):
        print(f"Time step {istep + 1} / {nsteps}", flush=True)
        
        tstate1 = thermalTimeStep(thermalProblem, tstate0, realDT)
        
        for pp in thermalProblem.postprocess:
            pp(thermalProblem, tstate1)
            
        thermalEvaluator = makeThermalEvaluator(tstate0.basis, tstate1.basis, tstate0.dofs, 
            tstate1.dofs, tstate1.history, thermalProblem.materials, thermalProblem.ambientTemperature)
        
        mstate1 = mechanicalTimeStep(mechanicalProblem, mstate0, tstate1.time, thermalEvaluator)

        for pp in mechanicalProblem.postprocess:
            pp(mechanicalProblem, mstate1)

        tstate0 = tstate1
        mstate0 = mstate1

    return tstate0, mstate0

del os, sys, path
from mlhp import *
