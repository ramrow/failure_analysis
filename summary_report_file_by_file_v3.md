# File-by-file analysis (v3)

Rule: case_name=top case folder (e.g., BernardCells), file_name=basename, include files under any nested 0/constant/system path, then keep only pairs present in jsonl.

- standard scanned=542 matched=27 missing=515
- benchmark scanned=412 matched=27 missing=385

- common matched pairs=9
- only standard matched pairs=0
- only benchmark matched pairs=0

## sample missing from jsonl (standard, up to 40)
- BernardCells / 1/0/epsilon (file=epsilon)
- BernardCells / 1/0/k (file=k)
- BernardCells / 1/0/p (file=p)
- BernardCells / 1/0/p_rgh (file=p_rgh)
- BernardCells / 1/0/T (file=T)
- BernardCells / 1/0/U (file=U)
- BernardCells / 1/constant/g (file=g)
- BernardCells / 1/constant/momentumTransport (file=momentumTransport)
- BernardCells / 1/constant/physicalProperties (file=physicalProperties)
- BernardCells / 1/system/blockMeshDict (file=blockMeshDict)
- BernardCells / 1/system/controlDict (file=controlDict)
- BernardCells / 1/system/fvSchemes (file=fvSchemes)
- BernardCells / 1/system/fvSolution (file=fvSolution)
- BernardCells / 1/constant/polyMesh/boundary (file=boundary)
- BernardCells / 1/constant/polyMesh/faces (file=faces)
- BernardCells / 1/constant/polyMesh/neighbour (file=neighbour)
- BernardCells / 1/constant/polyMesh/owner (file=owner)
- BernardCells / 1/constant/polyMesh/points (file=points)
- BernardCells / 2/0/epsilon (file=epsilon)
- BernardCells / 2/0/k (file=k)
- BernardCells / 2/0/p (file=p)
- BernardCells / 2/0/p_rgh (file=p_rgh)
- BernardCells / 2/0/T (file=T)
- BernardCells / 2/0/U (file=U)
- BernardCells / 2/constant/g (file=g)
- BernardCells / 2/constant/momentumTransport (file=momentumTransport)
- BernardCells / 2/constant/physicalProperties (file=physicalProperties)
- BernardCells / 2/system/blockMeshDict (file=blockMeshDict)
- BernardCells / 2/system/controlDict (file=controlDict)
- BernardCells / 2/system/fvSchemes (file=fvSchemes)
- BernardCells / 2/system/fvSolution (file=fvSolution)
- BernardCells / 2/constant/polyMesh/boundary (file=boundary)
- BernardCells / 2/constant/polyMesh/faces (file=faces)
- BernardCells / 2/constant/polyMesh/neighbour (file=neighbour)
- BernardCells / 2/constant/polyMesh/owner (file=owner)
- BernardCells / 2/constant/polyMesh/points (file=points)
- BernardCells / 3/0/epsilon (file=epsilon)
- BernardCells / 3/0/k (file=k)
- BernardCells / 3/0/p (file=p)
- BernardCells / 3/0/p_rgh (file=p_rgh)

## sample missing from jsonl (benchmark, up to 40)
- BernardCells / 1/0/epsilon (file=epsilon)
- BernardCells / 1/0/k (file=k)
- BernardCells / 1/0/p_rgh (file=p_rgh)
- BernardCells / 1/0/T (file=T)
- BernardCells / 1/0/U (file=U)
- BernardCells / 1/constant/g (file=g)
- BernardCells / 1/constant/momentumTransport (file=momentumTransport)
- BernardCells / 1/constant/physicalProperties (file=physicalProperties)
- BernardCells / 1/system/blockMeshDict (file=blockMeshDict)
- BernardCells / 1/system/controlDict (file=controlDict)
- BernardCells / 1/system/fvSchemes (file=fvSchemes)
- BernardCells / 1/system/fvSolution (file=fvSolution)
- BernardCells / 2/0/epsilon (file=epsilon)
- BernardCells / 2/0/k (file=k)
- BernardCells / 2/0/p_rgh (file=p_rgh)
- BernardCells / 2/0/T (file=T)
- BernardCells / 2/0/U (file=U)
- BernardCells / 2/constant/g (file=g)
- BernardCells / 2/constant/momentumTransport (file=momentumTransport)
- BernardCells / 2/constant/physicalProperties (file=physicalProperties)
- BernardCells / 2/system/blockMeshDict (file=blockMeshDict)
- BernardCells / 2/system/controlDict (file=controlDict)
- BernardCells / 2/system/fvSchemes (file=fvSchemes)
- BernardCells / 2/system/fvSolution (file=fvSolution)
- BernardCells / 2/constant/polyMesh/boundary (file=boundary)
- BernardCells / 2/constant/polyMesh/faces (file=faces)
- BernardCells / 2/constant/polyMesh/neighbour (file=neighbour)
- BernardCells / 2/constant/polyMesh/owner (file=owner)
- BernardCells / 2/constant/polyMesh/points (file=points)
- BernardCells / 3/0/epsilon (file=epsilon)
- BernardCells / 3/0/k (file=k)
- BernardCells / 3/0/p_rgh (file=p_rgh)
- BernardCells / 3/0/T (file=T)
- BernardCells / 3/0/U (file=U)
- BernardCells / 3/constant/g (file=g)
- BernardCells / 3/constant/momentumTransport (file=momentumTransport)
- BernardCells / 3/constant/physicalProperties (file=physicalProperties)
- BernardCells / 3/system/blockMeshDict (file=blockMeshDict)
- BernardCells / 3/system/controlDict (file=controlDict)
- BernardCells / 3/system/fvSchemes (file=fvSchemes)

## common matched pairs (up to 80)
- BernardCells / alphat
- BernardCells / nut
- counterFlowFlame2D / T
- damBreakWithObstacle / blockMeshDict
- forwardStep / blockMeshDict
- forwardStep / fvSchemes
- pitzDaily / controlDict
- pitzDaily / k
- pitzDaily / nut