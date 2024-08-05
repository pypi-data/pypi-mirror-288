import numpy as np
import sympy as sym
import spheretrig as spt

# 1. Case: one angle and two sides

A1 = spt.angle((50,8,0),'dms')
b1 = spt.angle((65,55,53),'dms')
c1 = spt.angle((78,32,11),'dms')

T1 = spt.solve_triang((A1,None,None),(None,b1,c1))

print(f'T1: angles={T1.anglesdeg},sides={T1.sidesdeg}')
T1.plot()

# 3. Case: two angles and one opposite side

A3 = spt.angle((69,9,9),'dms')
C3 = spt.angle((137,9,38),'dms')
c3 = spt.angle((141,31,33),'dms')

T3 = spt.solve_triang((A3,None,C3),(None,None,c3))

if isinstance(T3, list):
    print(f'T3: angles={T3[0].anglesdeg},sides={T3[0].sidesdeg}')
    T3[0].plot()
    print(f'T3: angles={T3[1].anglesdeg},sides={T3[1].sidesdeg}')
    T3[1].plot()
else:
    print(f'T1: angles={T3.anglesdeg},sides={T3.sidesdeg}')
    T3.plot()

# 5. Case: all sides

a5 = spt.angle((27,59,22),'dms')
b5 = spt.angle((41,5,6),'dms')
c5 = spt.angle((60,22,25),'dms')

T5 = spt.solve_triang((None,None,None),(a5,b5,c5))

print(f'T5: angles={T5.anglesdeg},sides={T5.sidesdeg}')
T5.plot()

# 7. Case: all angles

A7 = spt.angle((58,8,0),'dms')
B7 = spt.angle((68,36,0),'dms')
C7 = spt.angle((92,2,0),'dms')

T7 = spt.solve_triang((A7,B7,C7),(None,None,None))

print(f'T7: angles={T7.anglesdeg},sides={T7.sidesdeg}')
T7.plot()

# 8. Case: two angles and one side

A8 = spt.angle((71,9,46),'dms')
B8 = spt.angle((71,9,46),'dms')
c8 = spt.angle((115,2,4),'dms')

T8 = spt.solve_triang((A8,B8,None),(None,None,c8))

print(f'T8: angles={T8.anglesdeg},sides={T8.sidesdeg}')
T8.plot()

# 10. Case: two sides and one opposite angle

A10 = spt.angle((51,28,21),'dms')
a10 = spt.angle((43,46,28),'dms')
c10 = spt.angle((60,15,7),'dms')

T10 = spt.solve_triang((A10,None,None),(a10,None,c10))

if isinstance(T10, list):
    print(f'T10: angles={T10[0].anglesdeg},sides={T10[0].sidesdeg}')
    T10[0].plot()
    print(f'T10: angles={T10[1].anglesdeg},sides={T10[1].sidesdeg}')
    T10[1].plot()
else:
    print(f'T1: angles={T10.anglesdeg},sides={T10.sidesdeg}')
    T10.plot()
