"""
    optimized version:
    time: 46.2s

    cython optimized version:
    time: 24.1

        
"""
import itertools

cdef float PI = 3.14159265358979323
cdef float SOLAR_MASS = 4 * PI * PI
cdef float DAYS_PER_YEAR = 365.24

cdef dict BODIES = {
    'sun': ([0.0, 0.0, 0.0], [0.0, 0.0, 0.0], SOLAR_MASS),

    'jupiter': ([4.84143144246472090e+00,
                 -1.16032004402742839e+00,
                 -1.03622044471123109e-01],
                [1.66007664274403694e-03 * DAYS_PER_YEAR,
                 7.69901118419740425e-03 * DAYS_PER_YEAR,
                 -6.90460016972063023e-05 * DAYS_PER_YEAR],
                9.54791938424326609e-04 * SOLAR_MASS),

    'saturn': ([8.34336671824457987e+00,
                4.12479856412430479e+00,
                -4.03523417114321381e-01],
               [-2.76742510726862411e-03 * DAYS_PER_YEAR,
                4.99852801234917238e-03 * DAYS_PER_YEAR,
                2.30417297573763929e-05 * DAYS_PER_YEAR],
               2.85885980666130812e-04 * SOLAR_MASS),

    'uranus': ([1.28943695621391310e+01,
                -1.51111514016986312e+01,
                -2.23307578892655734e-01],
               [2.96460137564761618e-03 * DAYS_PER_YEAR,
                2.37847173959480950e-03 * DAYS_PER_YEAR,
                -2.96589568540237556e-05 * DAYS_PER_YEAR],
               4.36624404335156298e-05 * SOLAR_MASS),

    'neptune': ([1.53796971148509165e+01,
                 -2.59193146099879641e+01,
                 1.79258772950371181e-01],
                [2.68067772490389322e-03 * DAYS_PER_YEAR,
                 1.62824170038242295e-03 * DAYS_PER_YEAR,
                 -9.51592254519715870e-05 * DAYS_PER_YEAR],
                5.15138902046611451e-05 * SOLAR_MASS)}

cdef list pairsCopy = list(itertools.combinations(BODIES.keys(), 2))

cdef void update_vs( list v1,list  v2,float dt,float dx,float dy,float dz,float m1,float m2):
    mag = dt * pow(dx * dx + dy * dy + dz * dz , -1.5)
    b_m1 = m1*mag
    b_m2 = m2*mag
    v1[0] -= dx * b_m2
    v1[1] -= dy * b_m2
    v1[2] -= dz * b_m2
    v2[0] += dx * b_m1
    v2[1] += dy * b_m1
    v2[2] += dz * b_m1


cpdef void advance(float dt, list pairs, dict localBodies =BODIES):
    '''
        advance the system one timestep
    '''
    seenit = set()
    append = seenit.add
    bodyKeys = localBodies.keys()
    
    cdef float x1,y1,z1,m1,x2,y2,z2,m2 
    cdef list r, v1, v2

    for (body1,body2)in pairs:
        if not (body2 in seenit):
            ([ x1,  y1,  z1],  v1,  m1) = localBodies[body1]
            ([ x2,  y2, z2], v2, m2) = localBodies[body2]
            (dx, dy, dz) = (x1-x2, y1-y2, z1-z2)
            update_vs(v1, v2, dt, dx, dy, dz, m1, m2)
            append(body1)
    
    for body in bodyKeys:
        (r, [vx, vy, vz], m) = localBodies[body]
        #update_rs(r, dt, vx, vy, vz)
        r[0] += dt * vx
        r[1] += dt * vy
        r[2] += dt * vz


cpdef float report_energy( list pairs,dict BODIES=BODIES,float e=0.0):
    '''
        compute the energy and return it so that it can be printed
    '''

    seenit = set()
    cdef list bodyKeys = BODIES.keys()
    append = seenit.add

    cdef float x1,y1,z1,m1,x2,y2,z2,m2 
    cdef list r, v1, v2
    
    for (body1,body2)in pairs:
        if (body1 != body2) and not (body2 in seenit):
            (( x1,  y1,  z1),  v1,  m1) = BODIES[body1]
            ((x2, y2, z2), v2, m2) = BODIES[body2]
            (dx, dy, dz) = (x1-x2, y1-y2, z1-z2)
            e -= (m1 * m2) / pow(dx * dx + dy * dy + dz * dz,0.5 )
            append(body1)
    
    for body in bodyKeys:
        (r, [vx, vy, vz], m) = BODIES[body]
        e += m * (vx * vx + vy * vy + vz * vz) / 2.
        
    return e

cpdef void offset_momentum(tuple ref, float  px=0.0,float  py=0.0,float  pz=0.0, dict localBodies = BODIES):
    '''
        ref is the body in the center of the system
        offset values from this reference
    '''
    cdef float vx,vy,vz,m
    cdef list r 

    for body in localBodies.keys():
        ( r, [ vx, vy, vz], m) = localBodies[body]
        px -= vx * m
        py -= vy * m
        pz -= vz * m
        
    (r, v, m) = ref
    v[0] = px / m
    v[1] = py / m
    v[2] = pz / m


cpdef void nbody(int loops,str reference,int  iterations, list pairs = pairsCopy):
    '''
        nbody simulation
        loops - number of loops to run
        reference - body at center of system
        iterations - number of timesteps to advance
    '''
    # Set up global state
    offset_momentum(BODIES[reference])

    for _ in range(loops):
        # nothing is done with line below
        for _ in range(iterations):
            advance(0.01,pairs)
        print(report_energy(pairs))

def workAroundIpython():
    return nbody(100,'sun', 20000, pairsCopy)


