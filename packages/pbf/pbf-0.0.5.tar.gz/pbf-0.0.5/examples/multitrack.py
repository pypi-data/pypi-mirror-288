import pbf
units = pbf.units

# material
#inconel = pbf.makeMaterial("IN625")
inconel = pbf.readMaterialFile("C:/Users/Massimo/workspace/mlhp/src/materials/IN625.json")

# process parameters
laserD4Sigma = 0.100 * units.mm
laserSpeed = 800.0 * units.mm/units.s
laserPower = 280.0 * units.W
layerThickness = 0.050 * units.mm
hatching = 0.100 * units.mm
nLayers = 1
nLayerTracks = 2

# domain
origin0 = 0.0 * units.mm
origin1 = -0.3 * units.mm
origin2 = -0.3 * units.mm
length0 = 1.0 * units.mm
length1 = 0.6 * units.mm
basePlateHeight = 0.3 * units.mm
domainMin = [origin0, origin1, origin2]
domainHeight = origin2 + basePlateHeight + layerThickness * 2
print(domainHeight)
domainMax = [origin0+length0, origin1+length1, domainHeight]

# scan path
x0 = 0.25 * units.mm
x1 = 0.75 * units.mm
dwellTime = 0.1 * units.ms
totalTime = (x1 - x0) * nLayerTracks * nLayers / laserSpeed + dwellTime * nLayerTracks
layerTime = totalTime / nLayers
singleTrackTime = (x1 - x0) / laserSpeed
laserTrack = [pbf.LaserPosition(xyz=[x0, 0.0, layerThickness], time=0.0, power=laserPower),
              pbf.LaserPosition(xyz=[x1, 0.0, layerThickness], time=singleTrackTime*1, power=laserPower),
              pbf.LaserPosition(xyz=[x1, hatching, layerThickness], time=singleTrackTime*1 + dwellTime, power=0),
              pbf.LaserPosition(xyz=[x1, hatching, layerThickness], time=singleTrackTime*1 + dwellTime, power=laserPower),
              pbf.LaserPosition(xyz=[x0, hatching, layerThickness], time=singleTrackTime*2 + dwellTime, power=laserPower)]

# discretization
elementSize = 0.025 #0.12 * laserD4Sigma
grid = pbf.createMesh(domainMin, domainMax, elementSize, layerThickness*2) # zfactor??
timestep = 0.5 * laserD4Sigma / laserSpeed #0.2 * laserD4Sigma / laserSpeed

# laser heat source
laserBeam = pbf.gaussianBeam(sigma=laserD4Sigma / 4, absorptivity=0.32)
heatSource = pbf.volumeSource(laserTrack, laserBeam, depthSigma=0.045 * units.mm)

# output
filebase = "C:/Users/Massimo/workspace/mlhp/outputs/multitrack"

# thermal problem definition
tsetup = pbf.ThermalProblem()
tsetup.addPostprocessor(pbf.thermalVtuOutput(filebase))
tsetup.addPostprocessor(pbf.materialVtuOutput(filebase))
tsetup.addPostprocessor(pbf.meltPoolBoundsPrinter())
tsetup.setMaterials({"powder": pbf.makePowder(inconel), "structure": inconel, "baseplate": inconel, "air": pbf.makeAir()})
# tsetup.addDirichletBC(pbf.temperatureBC(4, tsetup.ambientTemperature))
tsetup.addSource(heatSource)
tstate0 = pbf.makeThermalState(tsetup, grid, powderHeight=layerThickness)
#tstate0 = pbf.makeThermalState(tsetup, grid, pbf.mlhp.implicitHalfspace([0.0, 0.0, 0.0], [0.0, 0.0, 0.0]),0, layerThickness)

# mechanical problem definition
msetup = pbf.MechanicalProblem()
msetup.addPostprocessor(pbf.mechanicalVtuOutput(filebase))
msetup.setMaterials({"powder": pbf.makePowder(inconel), "structure": inconel, "baseplate": inconel, "air": pbf.makeAir()})
mstate0 = pbf.makeMechanicalState(msetup, grid)

# solver thermomechanical problem
# tstate1 = pbf.computeThermalProblem(tsetup, tstate0, timestep, dur)#3 * dur)
tstate1, mstate1 = pbf.computeThermomechanicalProblem(tsetup, msetup, tstate0, mstate0, timestep, totalTime)