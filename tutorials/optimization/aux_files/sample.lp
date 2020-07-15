\Problem name: my problem

Minimize
 obj: x - y + 10 z + [ x ^2 - 2 y * z ] / 2
Subject To
 lin_eq:  x + 2 y  = 1
 lin_leq: x + 2 y <= 1
 lin_geq: x + 2 y >= 1
 quad_eq:  x + y + [ x ^2 - y * z + 2 z ^2 ]  = 1
 quad_leq: x + y + [ x ^2 - y * z + 2 z ^2 ] <= 1
 quad_geq: x + y + [ x ^2 - y * z + 2 z ^2 ] >= 1
Bounds
 0 <= x <= 1
-1 <= y <= 5
-1 <= z <= 5
Binaries
 x 
Generals
 y 
End
