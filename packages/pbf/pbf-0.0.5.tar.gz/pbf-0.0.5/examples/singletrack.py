import pbf
units = pbf.units

IN625 = pbf.makeMaterial("IN625")
#IN625 = pbf.readMaterialFile("materials/IN625.json")

laserD4Sigma = 170 * units.um
laserSpeed = 800 * units.mm / units.s
laserPower = 179.2 * units.W
layerHeight = 40.0 * units.um

# One layer of powder above base plate (set to zero for bare plate)
recoaterHeight = 1 * layerHeight

x0 = 0.25 * units.mm;
x1 = 0.75 * units.mm;

dur = ( x1 - x0 ) / laserSpeed

elementSize = 0.12 * laserD4Sigma;
timestep = 0.2 * laserD4Sigma / laserSpeed;
        
laserTrack = [pbf.LaserPosition(xyz=[x0, 0.0, recoaterHeight], time=0.0, power=laserPower),
              pbf.LaserPosition(xyz=[x1, 0.0, recoaterHeight], time=dur, power=laserPower)]

laserBeam = pbf.gaussianBeam(sigma=laserD4Sigma / 4, absorptivity=0.32)
heatSource = pbf.volumeSource(laserTrack, laserBeam, depthSigma=12 * units.um)

domainMin = [x0 - 0.25 * units.mm, -0.3 * units.mm, -0.3 * units.mm]
domainMax = [x1 + 0.25 * units.mm, +0.3 * units.mm, recoaterHeight]

filebase = "outputs/singletrack"
grid = pbf.createMesh(domainMin, domainMax, elementSize, layerHeight)

materials = { "powder"    : pbf.makePowder(IN625), 
              "structure" : IN625, 
              "baseplate" : IN625, 
              "air"       : pbf.makeAir( ) }

tsetup = pbf.ThermalProblem( )
tsetup.addPostprocessor(pbf.thermalVtuOutput(filebase))
tsetup.addPostprocessor(pbf.materialVtuOutput(filebase))
tsetup.addPostprocessor(pbf.meltPoolBoundsPrinter())
tsetup.setMaterials(materials)
#tsetup.addDirichletBC(pbf.temperatureBC(4, tsetup.ambientTemperature))
tsetup.addSource(heatSource) 

msetup = pbf.MechanicalProblem( )
msetup.addPostprocessor(pbf.mechanicalVtuOutput(filebase))
msetup.setMaterials(materials)

tstate0 = pbf.makeThermalState(tsetup, grid, powderHeight=recoaterHeight, srefinement=2)
mstate0 = pbf.makeMechanicalState(msetup, grid)

tstate1 = pbf.computeThermalProblem(tsetup, tstate0, timestep, dur)#3 * dur)
#tstate1, mstate1 = pbf.computeThermomechanicalProblem(tsetup, msetup, tstate0, mstate0, timestep, dur)


