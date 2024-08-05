import numpy as np
import sympy as sym
import plotly.graph_objects as go

# Classes

class angle:
    '''
    angle(x,'deg') -> angle in degrees
    angle(x,'rad') -> angle in radians
    angle((d,m,s),'dms') -> angle in degrees-minutes-seconds

    Converts a float number, or a tuple, to an angle in the given units.
    
    Attributes:

    - unit: unit of the angle.
    - deg: value of the angle in degrees.
    - rad: value of the angle in radians.
    - dms: angle in degrees-minutes-seconds.
    '''
    def __init__(self,val,unit:str):
        deg = np.pi/180
        rad = 1/deg
        self.unit = unit

        if self.unit == 'deg':
            self.deg = val
            self.rad = val*deg
            d = int(self.deg)
            min = (self.deg-d)*60
            m = int(min)
            s = (min-m)*60
            self.dms = (d,m,s)
        
        elif self.unit == 'rad':
            self.deg = val*rad
            self.rad = val
            d = int(self.deg)
            min = (self.deg-d)*60
            m = int(min)
            s = (min-m)*60
            self.dms = (d,m,s)

        elif self.unit == 'dms':
            self.dms = val
            d,m,s = self.dms
            self.deg = d+m/60+s/3600
            self.rad = self.deg*deg

    # define la suma de ángulos
    def __add__(self,other):
        '''returns self+other in degrees.'''
        return angle(self.deg+other.deg,'deg')
    
    # define la resta de ángulos
    def __sub__(self,other):
        '''returns self-other in degrees.'''
        return angle(self.deg-other.deg,'deg')
    
    # define la multiplicación por escalar
    def __mul__(self,val):
        '''returns self*val in degrees. Val must be int or float.'''
        if (isinstance(val,float) or isinstance(val,int)):
            newang = val*self.deg
            return angle(newang,'deg')
    
    def __rmul__(self,val):
        '''returns val*self in degrees. Val must be int or float.'''
        if (isinstance(val,float) or isinstance(val,int)):
            return self*val
        
    # define las interacciones con las funciones seno, coseno y tangente de numpy
    def __array_ufunc__(self,ufunc,method,inputs,*args,**kwargs):
        if ufunc.__name__ == 'sin':
            return np.sin(self.rad)
        if ufunc.__name__ == 'cos':
            return np.cos(self.rad)
        if ufunc.__name__ == 'tan':
            return np.tan(self.rad)

class sphtriangle:
    '''
    Converts two tuples of angles (one for the angles (A,B,C), one for the sides (a,b,c)) into a spherical triangles,
    if they satisfy the following properties:
    
    Property 1: A,B,C<180°
    Property 2: a+b+c<360°
    Property 3: 180<A+B+C<540°
    Property 4: A>B <=> a>b
    Property 5: A=B <=> a=b

    Attributes:

    - angles: angles of the spherical triangle.
    - sides: sides of the spherical triangle.
    - anglesdeg: angles of the triangle in degrees.
    - sidesdeg: sides of the triangle in degrees.
    - sphexcess: spherical excess of the triangle, useful to calculate the area.

    Methods:

    - plot(): graphs the triangle in a unit sphere.
    '''
    def __init__(self,angles:tuple,sides:tuple):
        # Propiedades de los triángulos esféricos
        prop1 = all([ang.deg<180 for ang in angles])
        prop2 = np.sum(np.array(sides)).deg<360
        prop3 = np.sum(np.array(angles)).deg>180 and np.sum(np.array(angles)).deg<540
        prop4 = []
        for i in range(len(angles)):
            for j in range(i,len(angles)):
                if j!=i:
                    p = sides[i].deg>sides[j].deg
                    q = angles[i].deg>angles[j].deg
                    prop4.append((p and q) or (not p and not q))
        prop4 = all(prop4)
        prop5 = []
        for i in range(len(angles)):
            for j in range(i,len(angles)):
                if j!=i:
                    p = (sides[i]-sides[j]).rad<1e-7
                    q = (angles[i]-angles[j]).rad<1e-7
                    prop5.append((p and q) or (not p and not q))
        prop5 = all(prop5)
        dic = {'Property 1':prop1,
               'Property 2':prop2,
               'Property 3':prop3,
               'Property 4':prop4,
               'Property 5':prop5}
        if not all(list(dic.values())):
            vals = np.array(list(dic.values()))
            keys = np.array(list(dic.keys()))
            notsatisfied = keys[[val == False for val in vals]]
            raise Exception(f'This is not a spherical triangle. {notsatisfied} is (are) not satisfied')

        # Atributos
        self.angles = angles
        self.sides = sides
        self.anglesdeg = tuple([ang.deg for ang in self.angles])
        self.sidesdeg = tuple([sid.deg for sid in self.sides])
        self.sphexcess = (np.sum(np.array(angles))-angle(180,'deg')).rad

    # Función plot
    def plot(self):
        '''
        Graphs the spherical triangle on a sphere of radius 1.
        '''
        theta, phi = np.mgrid[0:np.pi:100j,0:2*np.pi:100j]
        fig = go.Figure(go.Surface(
            x = np.sin(theta)*np.cos(phi),
            y = np.sin(theta)*np.sin(phi),
            z = np.cos(theta),
            colorscale = 'Purp',
            showscale=False
        ))
        pi = angle(np.pi,'rad')
        zero = angle(0,'rad')
        xsph = lambda th,ph: np.cos(th)*np.cos(ph)
        ysph = lambda th,ph: np.cos(th)*np.sin(ph)
        zsph = lambda th,ph: np.sin(th)
        hp = sidecos_th(None,pi*0.5-self.sides[2],self.sides[0],pi-self.angles[1],'A')
        Cp = sidecos_th(self.sides[0],hp,pi*0.5-self.sides[2],None,'A')

        vertx = [xsph(zero,zero),xsph(self.sides[2],zero),xsph(pi*0.5-hp,Cp)]
        verty = [ysph(zero,zero),ysph(self.sides[2],zero),ysph(pi*0.5-hp,Cp)]
        vertz = [zsph(zero,zero),zsph(self.sides[2],zero),zsph(pi*0.5-hp,Cp)]
        fig.add_trace(go.Scatter3d(x=[vertx[0]], y=[verty[0]], z=[vertz[0]], mode='markers',marker=dict(size=8,color='red'),name='A'))
        fig.add_trace(go.Scatter3d(x=[vertx[1]], y=[verty[1]], z=[vertz[1]], mode='markers',marker=dict(size=8,color='green'),name='B'))
        fig.add_trace(go.Scatter3d(x=[vertx[2]], y=[verty[2]], z=[vertz[2]], mode='markers',marker=dict(size=8,color='blue'),name='C'))

        uc = np.linspace(0,self.sides[2].rad,100)
        cx = xsph(uc,zero)
        cy = ysph(uc,zero)
        cz = zsph(uc,zero) 
        fig.add_trace(go.Scatter3d(x=cx, y=cy, z=cz, mode='lines',line=dict(width=10,color='blue'),name='c'))

        rot1 = np.array([[1,0,0],
                         [0,np.cos(0.5*pi-self.angles[0]),-np.sin(0.5*pi-self.angles[0])],
                         [0,np.sin(0.5*pi-self.angles[0]),np.cos(0.5*pi-self.angles[0])]])

        ub = np.linspace(0,self.sides[1].rad,100)
        b_prop = np.array([xsph(zero,ub),ysph(zero,ub),np.zeros(100)])
        b_ref = rot1@b_prop
        fig.add_trace(go.Scatter3d(x=b_ref[0], y=b_ref[1], z=b_ref[2], mode='lines',line=dict(width=10,color='green'),name='b'))

        rot2 = np.array([[np.cos(self.sides[2]),0,-np.sin(self.sides[2])],
                         [0,1,0],
                         [np.sin(self.sides[2]),0,np.cos(self.sides[2])]])
        rot3 = np.array([[1,0,0],
                         [0,np.cos(0.5*pi-self.angles[1]),np.sin(0.5*pi-self.angles[1])],
                         [0,-np.sin(0.5*pi-self.angles[1]),np.cos(0.5*pi-self.angles[1])]])
        ua = np.linspace(0,self.sides[0].rad,100)
        a_prop = np.array([xsph(zero,ua),ysph(zero,ua),np.zeros(100)])
        a_ref = rot2@(rot3@a_prop)
        fig.add_trace(go.Scatter3d(x=a_ref[0], y=a_ref[1], z=a_ref[2], mode='lines',line=dict(width=10,color='red'),name='a'))

        fig.update(layout_showlegend=True,layout_coloraxis_showscale=False)
        fig.update_layout(scene = dict(
            xaxis = dict(showticklabels=False,showbackground=False,visible=False),
            yaxis = dict(showticklabels=False,showbackground=False,visible=False),
            zaxis = dict(showticklabels=False,showbackground=False,visible=False),),
            width=700,
            margin=dict(
            r=10, l=10,
            b=10, t=10),
            )
        fig.show()

# Functions

# funciones trigonométricas inversas
def Arcsin(x):
    'Calculates the values of the angle for which the sin equals x in the interval [0°,360°)'
    pi = angle(np.pi,'rad')
    ref = angle(np.arcsin(abs(x)),'rad')
    if x >= 0:
        return np.array([ref,pi-ref])
    else:
        return np.array([pi+ref,2*pi-ref])
    
def Arccos(x):
    'Calculates the values of the angle for which the cos equals x in the interval [0°,360°)'
    pi = angle(np.pi,'rad')
    ref = angle(np.arccos(abs(x)),'rad')
    if x >= 0:
        return np.array([ref,2*pi-ref])
    else:
        return np.array([pi-ref,pi+ref])
    
def Arctan(x):
    'Calculates the values of the angle for which the tan equals x in the interval [0°,360°)'
    pi = angle(np.pi,'rad')
    ref = angle(np.arctan(abs(x)),'rad')
    if x >= 0:
        return np.array([ref,ref+pi])
    else:
        return np.array([pi-ref,2*pi-ref])

# teorema del seno
def sin_th(A,a,B,b,symbolic=False):
    '''
    Solves the missing element using the theorem of sines of spherical trigonometry.

    sin(A)/sin(a)=sin(B)/sin(b)

    INPUT:
    -A: angle, angle type object.
    -a: side opposite to angle A, angle type object.
    -B: angle, angle type object.
    -b: side obposite to angle B, angle type object.
    -symbolic: get symbolic output, Flase by default.

    Write None in the argument position of the desired element, for example:

    sin_th(A,None,B,b)

    The symbolic output is useful in case there is more than one unknown element.
    '''
    
    # argumentos y variable a resolver
    args = np.array([A,a,B,b])
    mask = [arg==None for arg in args]
    unk = sum(mask)

    # definición simbólica del teorema
    Asym, asym, Bsym, bsym = sym.symbols('A a B b')
    argsym = np.array([Asym, asym, Bsym, bsym])
    lhs = sym.sin(Asym)/sym.sin(asym)
    rhs = sym.sin(Bsym)/sym.sin(bsym)
    sin_theorem = sym.Eq(lhs,rhs)
    sins = []

    # solución simbólica de la ecuación
    for symbol in argsym:
        sins.append(sym.solve(sin_theorem,sym.sin(symbol))[0])
    sins = np.array(sins)
    if unk>1:
        return sins[mask]
    elif unk==0:
        raise Exception('There must be at least one unknown argument.')
    else:
        # solución numérica de la ecuación
        solvesin = sym.lambdify(argsym[[not el for el in mask]],sins[mask][0])
        sol_ = Arcsin(solvesin(*args[[not el for el in mask]]))
        sols1 = np.copy(args)
        sols2 = np.copy(args)
        ind = np.array(list(enumerate(args)))[mask][0][0]
        sols1[ind] = sol_[0]
        sols2[ind] = sol_[1]

        # propiedad de los triángulos esféricos
        p1 = sols1[0].deg>sols1[2].deg
        q1 = sols1[1].deg>sols1[3].deg
        p2 = sols2[0].deg>sols2[2].deg
        q2 = sols2[1].deg>sols2[3].deg

        solsfin = []

        if (p1 and q1) or (not p1 and not q1):
            solsfin.append(sol_[0])
        if (p2 and q2) or (not p2 and not q2):
            solsfin.append(sol_[1])

        if symbolic:
            return solsfin,sins
        else:
            return solsfin

# Teorema del coseno para lados
def sidecos_th(a,b,c,A,name_angle,symbolic=False):
    '''
    Solves the missing element using the theorem of cosines for sides of spherical trigonometry.

    cos(a)=cos(b)cos(c)+sin(b)sin(c)cos(A)

    INPUT:
    -a: side, angle type object.
    -b: side, angle type object.
    -c: side, angle type object.
    -A: angle opposite to side a, angle type object.
    -name_angle: name of the angle in the input, can be A, B or C. Required for the symbolic calculations.
    -symbolic: get symbolic output, Flase by default.

    Write None in the argument position of the side A or its opposite angle a, for example:

    sidecos_th(None,b,c,A,'B')

    The symbolic output is useful to do successive calculations.
    '''
    # Argumentos y variable a resolver
    args = np.array([a,b,c,A])
    mask1 = [arg==None for arg in args]
    unk = sum(mask1)

    # Nombres de los elementos
    angle_names = np.array(['A','B','C'])
    side_names = np.array([let.lower() for let in angle_names])
    mask2 = [let!=name_angle for let in angle_names]

    # Definición simbólica del teorema
    anglesym = sym.symbols(name_angle)
    oppsym = sym.symbols(name_angle.lower())
    side1sym, side2sym = sym.symbols(' '.join(str(_) for _ in side_names[mask2]))
    argsym = np.array([oppsym,side1sym,side2sym,anglesym])
    lhs = sym.cos(oppsym)
    rhs = sym.cos(side1sym)*sym.cos(side2sym)+sym.sin(side1sym)*sym.sin(side2sym)*sym.cos(anglesym)
    sidecos_theorem = sym.Eq(lhs,rhs)

    # Solución numérica de la ecuación
    if unk!=1:
        raise Exception('There must be only one unknown argument.')
    else:
        if b==None or c==None:
            raise Exception('This function only solves for the side or its opposite angle. Try another method.')
        elif a==None:
            solvecos = sym.lambdify(argsym[[not _ for _ in mask1]],rhs)
            sol = Arccos(solvecos(*args[[not el for el in mask1]]))[0]
            if symbolic:
                return sol,rhs
            else:
                return sol
        elif A==None:
            cosA = sym.solve(sidecos_theorem,sym.cos(anglesym))[0]
            solvecos = sym.lambdify(argsym[[not _ for _ in mask1]],cosA)
            sol = Arccos(solvecos(*args[[not el for el in mask1]]))[0]
            if symbolic:
                return sol,cosA
            else:
                return sol

# Teorema del coseno para ángulos
def anglecos_th(A,B,C,a,name_side,symbolic=False):
    '''
    Solves the missing element using the theorem of cosines for angles of spherical trigonometry.

    cos(A)=-cos(B)cos(C)+sin(B)sin(C)cos(a)

    INPUT:
    -A: angle, angle type object.
    -B: angle, angle type object.
    -C: angle, angle type object.
    -a: side opposite to angle A, angle type object.
    -name_side: name of the side in the input, can be a, b or c. Required for the symbolic calculations.
    -symbolic: get symbolic output, Flase by default.

    Write None in the argument position of the side A or its opposite angle a, for example:

    anglecos_th(None,B,C,a,'b')

    The symbolic output is useful to do successive calculations.
    '''
    # Argumentos y variable a resolver
    args = np.array([A,B,C,a])
    mask1 = [arg==None for arg in args]
    unk = sum(mask1)

    # Nombres de los elementos
    angle_names = np.array(['A','B','C'])
    side_names = np.array([let.lower() for let in angle_names])
    mask2 = [let!=name_side for let in side_names]

    # Definición simbólica del teorema
    sidesym = sym.symbols(name_side)
    oppsym = sym.symbols(name_side.upper())
    angle1sym, angle2sym = sym.symbols(' '.join(str(_) for _ in angle_names[mask2]))
    argsym = np.array([oppsym,angle1sym,angle2sym,sidesym])
    lhs = sym.cos(oppsym)
    rhs = -sym.cos(angle1sym)*sym.cos(angle2sym)+sym.sin(angle1sym)*sym.sin(angle2sym)*sym.cos(sidesym)
    anglecos_theorem = sym.Eq(lhs,rhs)

    # Solución simbólica del teorema
    if unk!=1:
        raise Exception('There must be only one unknown argument.')
    else:
        if B==None or C==None:
            raise Exception('This function only solves for the angle or its opposite side. Try another method.')
        elif A==None:
            solvecos = sym.lambdify(argsym[[not _ for _ in mask1]],rhs)
            sol = Arccos(solvecos(*args[[not el for el in mask1]]))[0]
            if symbolic:
                return sol,rhs
            else:
                return sol
        elif a==None:
            cosa = sym.solve(anglecos_theorem,sym.cos(sidesym))[0]
            solvecos = sym.lambdify(argsym[[not _ for _ in mask1]],cosa)
            sol = Arccos(solvecos(*args[[not el for el in mask1]]))[0]
            if symbolic:
                return sol,cosa
            else:
                return sol

def solve_triang(angles,sides):
    '''
    Solves the spherical triangle given three of its elements using the theorems of
    spherical trigonometry.

    INPUT:
    -angles: tuple of angle-type objects containing the spherical angles of the triangle.
    -sides: tuple of angle-type objects containing the sides of the triangle.

    OUTPUT:
    -spherical triangle with the given elements, sphtriangle object.

    The input tuples must be ordered like so:
    angles = (A,B,C)
    sides = (a,b,c)

    That is, the first side must be opposite to the first angle.
    Type None for the unknown elements.    
    '''
    # Definition of the elements
    A,B,C = angles
    a,b,c = sides
    angles = np.array(angles)
    sides = np.array(sides)
    angle_names = np.array(['A','B','C'])
    side_names = np.array([let.lower() for let in angle_names])

    # Masks
    mask_ang = [ang==None for ang in angles]
    antimask_ang = [not _ for _ in mask_ang]
    mask_sid = [sid==None for sid in sides]
    antimask_sid = [not _ for _ in mask_sid]

    # Cases for the given elements
    all_sides = all(angles == None)
    all_angles = all(sides == None)
    twoangles_oneside = sum(mask_ang)==1 and angle_names[mask_ang][0].lower() not in side_names[mask_sid]
    twosides_oneangle = sum(mask_sid)==1 and side_names[mask_sid][0].upper() not in angle_names[mask_ang]
    twoangles_sinth = sum(mask_ang)==1 and angle_names[mask_ang][0].lower() in side_names[mask_sid]
    twosides_sinth = sum(mask_sid)==1 and side_names[mask_sid][0].upper() in angle_names[mask_ang]

    # Verifies that the number of unknown elements is correct
    if sum(mask_ang)+sum(mask_sid)!=3:
        raise Exception('This number of unknowns is not allowed. Please enter 3 unknowns')
    
    else:
        # Evaluates the cases and solves according to the situation
        if all_sides:
            A = sidecos_th(a,b,c,None,'A')
            B = sidecos_th(b,a,c,None,'B')
            C = sidecos_th(c,a,b,None,'C')

            angles = (A,B,C)
            triangle = sphtriangle(angles,tuple(sides))
            return triangle
        
        elif all_angles:
            a = anglecos_th(A,B,C,None,'a')
            b = anglecos_th(B,A,C,None,'b')
            c = anglecos_th(C,A,B,None,'c')

            sides = (a,b,c)
            triangle = sphtriangle(tuple(angles),sides)
            return triangle

        elif twoangles_oneside:
            angles[mask_ang] = anglecos_th(angles[mask_ang][0],
                                           angles[antimask_ang][0],
                                           angles[antimask_ang][1],
                                           sides[antimask_sid][0],
                                           side_names[mask_ang][0])
            side1 = anglecos_th(angles[mask_sid][0],
                                   angles[mask_sid][1],
                                   angles[antimask_sid][0],
                                   sides[mask_sid][0],
                                   side_names[mask_sid][0])
            side2 = anglecos_th(angles[mask_sid][1],
                                   angles[mask_sid][0],
                                   angles[antimask_sid][0],
                                   sides[mask_sid][1],
                                   side_names[mask_sid][1])
            sides[mask_sid] = [side1,side2]

            triangle = sphtriangle(tuple(angles),tuple(sides))
            return triangle
        elif twosides_oneangle:
            sides[mask_sid] = sidecos_th(sides[mask_sid][0],
                                           sides[antimask_sid][0],
                                           sides[antimask_sid][1],
                                           angles[antimask_ang][0],
                                           angle_names[mask_sid][0])
            angle1 = sidecos_th(sides[mask_ang][0],
                                   sides[mask_ang][1],
                                   sides[antimask_ang][0],
                                   angles[mask_ang][0],
                                   angle_names[mask_ang][0])
            angle2 = sidecos_th(sides[mask_ang][1],
                                   sides[mask_ang][0],
                                   sides[antimask_ang][0],
                                   angles[mask_ang][1],
                                   angle_names[mask_ang][1])
            angles[mask_ang] = [angle1,angle2]

            triangle = sphtriangle(tuple(angles),tuple(sides))
            return triangle
        elif twoangles_sinth:
            a_sinth = angles[antimask_ang]
            s_sinth = sides[antimask_ang]

            a_sinth2 = np.copy(a_sinth)
            s_sinth2 = np.copy(s_sinth)

            mask_sinth = s_sinth == None

            s_sinth[mask_sinth],s_sinth2[mask_sinth] = sin_th(a_sinth[0],s_sinth[0],a_sinth[1],s_sinth[1])

            Asym,Bsym,Csym,asym,bsym,csym = sym.symbols('A B C a b c')

            cosC = anglecos_th(None,0,0,0,'c',symbolic=1)[1]

            cosc = sidecos_th(None,0,0,0,'C',symbolic=1)[1]

            cosc = sym.solve(sym.Eq(cosc.subs(sym.cos(Csym),cosC),sym.cos(csym)),sym.cos(csym))[0]

            cosc = sym.lambdify((Asym,Bsym,asym,bsym),cosc)

            cosc1 = cosc(a_sinth[0],a_sinth[1],s_sinth[0],s_sinth[1])
            cosc2 = cosc(a_sinth2[0],a_sinth2[1],s_sinth2[0],s_sinth2[1])

            c1 = Arccos(cosc1)[0]
            c2 = Arccos(cosc2)[0]

            C1 = anglecos_th(None,a_sinth[0],a_sinth[1],c1,'c')
            C2 = anglecos_th(None,a_sinth2[0],a_sinth2[1],c2,'c')

            sols = []

            try:
                T1 = sphtriangle((a_sinth[0],a_sinth[1],C1),(s_sinth[0],s_sinth[1],c1))
            except:
                pass
            else:
                sols.append(T1)

            try:
                T2 = sphtriangle((a_sinth2[0],a_sinth2[1],C2),(s_sinth2[0],s_sinth2[1],c2))
            except:
                pass
            else:
                sols.append(T2)

            return sols

        elif twosides_sinth:
            a_sinth = angles[antimask_sid]
            s_sinth = sides[antimask_sid]

            a_sinth2 = np.copy(a_sinth)
            s_sinth2 = np.copy(s_sinth)

            mask_sinth = a_sinth == None

            a_sinth[mask_sinth],a_sinth2[mask_sinth] = sin_th(a_sinth[0],s_sinth[0],a_sinth[1],s_sinth[1])

            Asym,Bsym,Csym,asym,bsym,csym = sym.symbols('A B C a b c')

            cosC = anglecos_th(None,0,0,0,'c',symbolic=1)[1]

            cosc = sidecos_th(None,0,0,0,'C',symbolic=1)[1]

            cosc = sym.solve(sym.Eq(cosc.subs(sym.cos(Csym),cosC),sym.cos(csym)),sym.cos(csym))[0]

            cosc = sym.lambdify((Asym,Bsym,asym,bsym),cosc)

            cosc1 = cosc(a_sinth[0],a_sinth[1],s_sinth[0],s_sinth[1])
            cosc2 = cosc(a_sinth2[0],a_sinth2[1],s_sinth2[0],s_sinth2[1])

            c1 = Arccos(cosc1)[0]
            c2 = Arccos(cosc2)[0]

            C1 = anglecos_th(None,a_sinth[0],a_sinth[1],c1,'c')
            C2 = anglecos_th(None,a_sinth2[0],a_sinth2[1],c2,'c')

            sols = []

            try:
                T1 = sphtriangle((a_sinth[0],a_sinth[1],C1),(s_sinth[0],s_sinth[1],c1))
            except:
                pass
            else:
                sols.append(T1)

            try:
                T2 = sphtriangle((a_sinth2[0],a_sinth2[1],C2),(s_sinth2[0],s_sinth2[1],c2))
            except:
                pass
            else:
                sols.append(T2)

            return sols