import unittest, pbf

units = pbf.units

class AMB201802Test(unittest.TestCase):
    def test(self):
        IN625 = pbf.makeMaterial("IN625")

        ## Parameters from 2022 space-time paper 
        #density = 8440.0 * units.kg / ( units.m * units.m * units.m )
        #cp  = 4.05e-1 * units.J / ( units.g * units.C )
        #dcp = 2.47e-4 * units.J / ( units.g * units.C )
        #k = 9.50e-2 * units.W / ( units.cm * units.C )
        #dk = 1.50e-4 * units.W / ( units.cm * units.C )
        #IN625.density = pbf.temperatureFunction([0.0], [density], extrapolate="constant")
        #IN625.specificHeatCapacity = pbf.temperatureFunction([0.0, 1290.0], [cp, cp + 1290.0 * dcp], extrapolate="constant")
        #IN625.heatConductivity = pbf.temperatureFunction([0.0, 1290.0], [k, k + 1290.0 * dk], extrapolate="constant")
        #IN625.latentHeatOfFusion = 2.8e5 * units.J / units.kg

        # General parameters
        laserD4Sigma = 170 * units.um
        laserSpeed = 800 * units.mm / units.s
        laserPower = 179.2 * units.W

        x0 = 2.004 * units.cm
        x1 = 0.604 * units.cm
        
        dur = abs( x1 - x0 ) / laserSpeed
        
        # Set to dur to simulate full benchmark
        simulationTime = 10.0 / 256.0 * dur
        
        elementSize = 0.368 * laserD4Sigma;
        refinement = 5
        timestep = 0.322 * laserD4Sigma / laserSpeed;
                
        laserTrack = [pbf.LaserPosition(xyz=[x0, 0.0, 0.0], time=0.0, power=laserPower),
                      pbf.LaserPosition(xyz=[x1, 0.0, 0.0], time=dur, power=laserPower)]

        laserBeam = pbf.gaussianBeam(sigma=laserD4Sigma / 4, absorptivity=0.32)
        heatSource = pbf.volumeSource(laserTrack, laserBeam, depthSigma=0.28 * laserD4Sigma / 4)

        domainMin = [0.0 * units.mm, -24.82 * units.mm / 2.0, -3.18 * units.mm]
        domainMax = [24.08 * units.mm, 24.82 * units.mm / 2.0, 0.0]

        filebase = "outputs/pbftests/amb2018-02"
        grid = pbf.createMesh(domainMin, domainMax, elementSize * 2**refinement, zfactor=0.5)

        # Setup problem
        tsetup = pbf.ThermalProblem( )
        
        materials = { "powder"    : pbf.makePowder(IN625), 
                      "structure" : IN625, 
                      "baseplate" : IN625, 
                      "air"       : pbf.makeAir( ) }

        tsetup.setMaterials(materials)
        tsetup.addSource(heatSource) 
        
        # Setup custom refinement
        refinementPoints = [
            pbf.LaserRefinementPoint(0.00*units.ms, 0.18*units.mm, 5.4, 0.5),
            pbf.LaserRefinementPoint(1.20*units.ms, 0.24*units.mm, 3.5, 0.5),
            pbf.LaserRefinementPoint(6.00*units.ms, 0.40*units.mm, 2.5, 0.8),
            pbf.LaserRefinementPoint(30.0*units.ms, 0.90*units.mm, 1.5, 1.0),
            pbf.LaserRefinementPoint(0.10*units.s,  1.10*units.mm, 1.0, 1.0)]
            
        refinement = lambda problem, state0, state1: pbf.laserTrackPointRefinement(laserTrack, 
            refinementPoints, state1.time, pbf.maxdegree(state0.basis) + 2)
        refinementFunction = pbf.laserTrackPointRefinementFunction(laserTrack, refinementPoints)     
        
        tsetup.degree = 3
        tsetup.addRefinement(refinement)
        tsetup.addPostprocessor(pbf.thermalVtuOutput(filebase, interval=2, functions=[(refinementFunction, "RefinementLevel")]))
        
        # Compute melt pool dimensions every other step
        meltPoolBoundsList = []
        def meltPoolBoundsAccumulator(mesh):
            points = mesh.points( )
            bounds = [[1e50, 1e50, 1e50], [-1e50, -1e50, -1e50]]
            for ipoint in range(int(len(points)/3)):
                for icoord in range(3):
                    bounds[0][icoord] = min(bounds[0][icoord], points[3*ipoint + icoord])
                    bounds[1][icoord] = max(bounds[1][icoord], points[3*ipoint + icoord])
            meltPoolBoundsList.append([max(u - l, 0.0) for l, u in zip(*bounds)])
            
        tsetup.addPostprocessor(pbf.meltPoolContourOutput(meltPoolBoundsAccumulator, interval=2))
        
        # Save number of elements and number of dofs every time step
        computedNElementsList, computedNDofList = [], []
        
        def meshDataAccumulator(thermalProblem, tstate):
            computedNElementsList.append(tstate.basis.nelements( ))
            computedNDofList.append(tstate.basis.ndof( ))
        
        tsetup.addPostprocessor(meshDataAccumulator)
        
        # Setup initial state and compute problem
        tstate0 = pbf.makeThermalState(tsetup, grid)
        tstate1 = pbf.computeThermalProblem(tsetup, tstate0, timestep, simulationTime)
        
        # Check whether results are consistent with previous versions
        expectedNElementsList = [432, 586, 600, 614, 614, 642, 656, 670, 656, 670, 670]
        expectedNDofList = [4186, 4964, 5047, 5130, 5130, 5296, 5379, 5462, 5379, 5462, 5462]
        
        assert(len(expectedNElementsList) == len(computedNElementsList))
        assert(len(expectedNDofList) == len(computedNDofList))
        
        for expectedNCells, computedNCells in zip(expectedNElementsList, computedNElementsList):
            assert(expectedNCells == computedNCells)
        for expectedNDof, computedNDof in zip(expectedNDofList, computedNDofList):
            assert(expectedNDof == computedNDof)
        
        expectedBoundsList = [[0.0, 0.0, 0.0], 
                              [0.126396484375000, 0.10520087348090286, 0.025447591145833316], 
                              [0.207884657118058, 0.11900322808159715, 0.031313476562500005], 
                              [0.278431532118056, 0.11933987087673618, 0.032089843750000006], 
                              [0.328565538194443, 0.11900322808159715, 0.032003580729166634], 
                              [0.345385742187499, 0.11866658528645833, 0.032003580729166634]]
        
        assert(len(meltPoolBoundsList) == len(expectedBoundsList))
        
        for computedBounds, expectedBounds in zip(meltPoolBoundsList, expectedBoundsList):
            for computedAxis, expectedAxis in zip(computedBounds, expectedBounds):
                self.assertAlmostEqual(computedAxis, expectedAxis, delta=1e-6)
        
        temperature = pbf.thermalEvaluator(tstate1)
        
        self.assertAlmostEqual(temperature([19.53,  0.03, 0.0]), 2405.20217684007, delta=1e-6)
        self.assertAlmostEqual(temperature([19.86, -0.07, 0.0]), 769.370817398213, delta=1e-6)
        self.assertAlmostEqual(temperature([13.0,   5.0,  0.0]), 25.0000002086494, delta=1e-6)
