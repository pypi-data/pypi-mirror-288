import unittest, math, pbf
from functools import reduce

units = pbf.units

distance = lambda xyz0, xyz1 : math.sqrt(reduce(lambda a, b : a + b, [(x1 - x0)**2 for x0, x1 in zip(xyz0, xyz1)]))

class AMB201802Test(unittest.TestCase):
    def test(self):
        material = pbf.makeMaterial("SS316L")

        # General parameters
        laserD4Sigma = 120 * units.um
        laserSpeed = 1000 * units.mm / units.s
        laserPower = 180 * units.W
        layerHeight = 30 * units.um
        
        recoaterLevel = 20 * layerHeight
        totalHeight = 30 * layerHeight

        xyz0 = [-0.55 * units.mm, 1.45 * units.mm, recoaterLevel]
        xyz1 = [0.55 * units.mm, 2.55 * units.mm, recoaterLevel]
        
        dur = distance(xyz0, xyz1) / laserSpeed
        
        # Set to dur to simulate full benchmark
        simulationTime = 1.7 * dur
        
        elementSize = 0.12 * laserD4Sigma;
        trefinement = 5
        srefinement = 5
        timestep = 0.3 * laserD4Sigma / laserSpeed;
                
        laserTrack = [pbf.LaserPosition(xyz=xyz0, time=0.0, power=laserPower),
                      pbf.LaserPosition(xyz=xyz1, time=dur, power=laserPower)]

        laserBeam = pbf.gaussianBeam(sigma=laserD4Sigma / 4, absorptivity=0.32)
        heatSource = pbf.volumeSource(laserTrack, laserBeam, depthSigma=10 * units.um)

        domainMin = [-2.0 * units.mm, 0.0 * units.mm, -1.0 * units.mm]
        domainMax = [2.0 * units.mm, 4.0 * units.mm, totalHeight]

        # Construct part
        circles = pbf.implicitSubtraction([pbf.implicitSphere([0.0, 0.0], 1 * units.mm),
                                           pbf.implicitSphere([0.0, 0.0], 0.55 * units.mm)])
                                           
        cylinder = pbf.extrude(circles, 0.0, 2 * units.mm, 0)
        
        translation = [-(1/math.sqrt(2))*units.mm, (1/math.sqrt(2) + 2)*units.mm, 0*units.mm]
        transformation = pbf.concatenate([pbf.rotation([0.0, 0.0, 1.0], -0.25 * math.pi), 
                                          pbf.translation(translation)])
               
        part = pbf.implicitIntersection([pbf.implicitTransformation(cylinder, transformation), 
                                         pbf.implicitHalfspace([0.0, 0.0, recoaterLevel-layerHeight], [0.0, 0.0, 1.0])])
        
        # Setup problem
        filebase = "outputs/pbftests/bridge"
        grid = pbf.createMesh(domainMin, domainMax, elementSize * 2**trefinement, layerHeight=layerHeight, zfactor=0.5)
        
        tsetup = pbf.ThermalProblem( )
        
        materials = { "powder"    : pbf.makePowder(material), 
                      "structure" : material, 
                      "baseplate" : material, 
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
        
        tsetup.addRefinement(refinement)
        tsetup.addPostprocessor(pbf.materialVtuOutput(filebase, interval=2))
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
        computedNElementsList, computedMaterialNCellsList, computedNDofList = [], [], []
        
        def meshDataAccumulator(thermalProblem, tstate):
            computedNElementsList.append(tstate.basis.nelements( ))
            computedNDofList.append(tstate.basis.ndof( ))
            computedMaterialNCellsList.append(tstate.history.grid().ncells())
        
        tsetup.addPostprocessor(meshDataAccumulator)
        
        # Setup initial state and compute problem
        tstate0 = pbf.makeThermalState(tsetup, grid, powderHeight=recoaterLevel, srefinement=srefinement, part=part)
        tstate1 = pbf.computeThermalProblem(tsetup, tstate0, timestep, simulationTime)
        
        # Check whether results are consistent with previous versions
        expectedNElementsList = [512, 5370, 5748, 6406, 7036, 7414, 8170, 8408, 
            8912, 9416, 9598, 10151, 10389, 10683, 11033, 11061, 11313, 11383, 
            11635, 11789, 11901, 12041, 12111, 12321, 12531, 12643, 12755, 
            12839, 12825, 12979, 13147, 13126, 13238, 13280, 13266, 13476, 
            13378, 13462, 13672, 13476, 13714, 13700, 13644, 13854, 13504, 
            12902, 12272, 11656, 11124, 10354, 9948, 9290, 8842, 8436, 7708, 
            7414, 6826, 6490, 6196, 5706, 5594, 5356, 5244, 5076, 4866, 4838, 
            4628, 4628, 4460, 4334, 4306, 4110, 4054, 3984, 3802]
            
        expectedMaterialNCellsList = [186264, 111735, 111805, 111854, 111882, 
            111889, 111959, 112029, 112078, 112106, 112113, 112183, 112253, 
            112302, 112330, 112393, 112407, 112456, 112526, 112554, 112610, 
            112631, 112666, 112778, 112792, 112848, 112855, 112897, 113002, 
            113030, 113072, 113079, 113121, 113226, 113240, 113296, 113317, 
            113345, 113436, 113464, 113520, 113548, 113569, 113632, 113632, 
            113632, 113632, 113632, 113632, 113632, 113632, 113632, 113632, 
            113632, 113632, 113632, 113632, 113632, 113632, 113632, 113632, 
            113632, 113632, 113632, 113632, 113632, 113632, 113632, 113632, 
            113632, 113632, 113632, 113632, 113632, 113632]
            
        expectedNDofList = [729, 4447, 4789, 5325, 5857, 6172, 6794, 6983, 
            7385, 7794, 7939, 8375, 8558, 8777, 9078, 9109, 9304, 9362, 9545, 
            9684, 9797, 9885, 9943, 10062, 10260, 10363, 10433, 10507, 10449, 
            10584, 10713, 10687, 10796, 10801, 10817, 10975, 10912, 10969, 
            11117, 10966, 11152, 11144, 11104, 11237, 10956, 10455, 9919, 9388, 
            8932, 8299, 7957, 7419, 7050, 6702, 6121, 5866, 5404, 5141, 4909, 
            4542, 4460, 4271, 4189, 4052, 3894, 3866, 3699, 3695, 3564, 3466, 
            3441, 3294, 3250, 3195, 3069]
        
        assert(len(expectedNElementsList) == len(computedNElementsList))
        assert(len(expectedMaterialNCellsList) == len(computedMaterialNCellsList))
        assert(len(expectedNDofList) == len(computedNDofList))
        
        for expectedNCells, computedNCells in zip(expectedNElementsList, computedNElementsList):
            assert(expectedNCells == computedNCells)
        for expectedNCells, computedNCells in zip(expectedMaterialNCellsList, computedMaterialNCellsList):
            assert(expectedNCells == computedNCells)
        for expectedNDof, computedNDof in zip(expectedNDofList, computedNDofList):
            assert(expectedNDof == computedNDof)
        
        expectedBoundsList = [[0.0, 0.0, 0.0], 
                              [0.10986328125,    0.10986328125,    0.03603515624999998  ], 
                              [0.1549072265625,  0.1549072265625,  0.04763671874999997  ], 
                              [0.1959228515625,  0.1959228515625,  0.05167968750000007  ], 
                              [0.22314453125,    0.22314453125,    0.052617187499999996 ], 
                              [0.25,             0.25,             0.052734375          ], 
                              [0.270263671875,   0.270263671875,   0.05255859374999994  ], 
                              [0.2808837890625,  0.2808837890625,  0.052617187499999996 ], 
                              [0.2864990234375,  0.2864990234375,  0.05267578125000005  ], 
                              [0.28466796875,    0.28466796875,    0.05279296875000006  ], 
                              [0.28564453125,    0.28564453125,    0.05314453124999996  ], 
                              [0.288818359375,   0.288818359375,   0.05525390624999993  ], 
                              [0.2908935546875,  0.2908935546875,  0.05947265624999998  ], 
                              [0.2957763671875,  0.2957763671875,  0.06193359375000007  ], 
                              [0.3145751953125,  0.3145751953125,  0.06483398437499999  ], 
                              [0.337890625,      0.337890625,      0.065302734375       ], 
                              [0.371826171875,   0.371826171875,   0.05589843750000001  ], 
                              [0.4044189453125,  0.4044189453125,  0.05249999999999999  ], 
                              [0.4295654296875,  0.4295654296875,  0.05249999999999999  ], 
                              [0.46148681640625, 0.46148681640625, 0.05255859375000005  ], 
                              [0.2904052734375,  0.2904052734375,  0.052617187499999996 ], 
                              [0.285888671875,   0.285888671875,   0.05267578125000005  ], 
                              [0.2581787109375,  0.2581787109375,  0.05191406249999997  ], 
                              [0.2022705078125,  0.2022705078125,  0.04335937499999998  ], 
                              [0.1312255859375,  0.1312255859375,  0.024433593749999982 ], 
                              [0.01708984375,    0.01708984375,    0.0007617187499999734], 
                              [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], 
                              [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], 
                              [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], 
                              [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
        
        assert(len(meltPoolBoundsList) == len(expectedBoundsList))
        
        for computedBounds, expectedBounds in zip(meltPoolBoundsList, expectedBoundsList):
            for computedAxis, expectedAxis in zip(computedBounds, expectedBounds):
                self.assertAlmostEqual(computedAxis, expectedAxis, delta=1e-6)
        
        temperature = pbf.thermalEvaluator(tstate1)
        
        self.assertAlmostEqual(temperature([0.0, 2.0, recoaterLevel]), 730.0888019468413, delta=1e-6)
