import numpy as np

# All units are standard SI units

dtype = np.float64 # A type conversion function used to help avoid type coercion problems
zero_vec = np.array([0,0,0], dtype) # zero vector as frequently used

# Some constants/frequently used variables
# Below either taken or derived from values and equations given by Walker et al. (2014)
electron_mass = dtype(9.1094*10**(-31))
deuterium_mass = dtype(2.0136*1.6605*10**(-27))
elementary_charge = dtype(1.6022*10**(-19))
permeability_of_free_space = dtype(1.2566*10**(-6))
permittivity_of_free_space = dtype(8.8542*10**(-12))
gas_constant = dtype(8.3145)
avogadro = dtype(6.0221 * 10**23)
electron_molar_mass = electron_mass * avogadro
deuterium_molar_mass = deuterium_mass * avogadro

def two_eq_rk4(x, x_prime, y, y_prime, h):
    """Returns numerically computed solution to 2 var coupled 1st order differential after 1 timestep using RK4 given starting x, y values and respective derivative functions
    """
    j1 = y_prime(x, y)
    k1 = x_prime(x, y)
    j2 = y_prime(x + h*k1/2, y + h*j1/2)
    k2 = x_prime(x + h*k1/2, y + h*j1/2)
    j3 = y_prime(x + h*k2/2, y + h*j2/2)
    k3 = x_prime(x + h*k2/2, y + h*j2/2)
    j4 = y_prime(x + h*k3, y + h*j3)
    k4 = x_prime(x + h*k3, y + h*j3)
    x_result = x + (h/6) * (k1+2*k2+2*k3+k4)
    y_result = y + (h/6) * (j1+2*j2+2*j3+j4)
    return (x_result, y_result)

def generate_field_vectors(vector_num, field_function, x, y, z):
    """Returns lists u, v, w denoting components of field vectors generated via field_function form input positions specified by x,y,z
    Args:
        field_function: function that takes in position input tuple (x,y,z) to return field vector there in format (field_name, field_vector)
        x, y, z: variables denoting multiple position coordinates (x,y,z) that is expected to be generated from np.meshgrid
        vector_num: integer denoting number of vectors along each axis' direction
    """
    u = []
    v = []
    w = []
    for i in range(vector_num):
        u.append([])
        v.append([])
        w.append([])
        for j in range(vector_num):
            u[i].append([])
            v[i].append([])
            w[i].append([])
            for k in range(vector_num):
                field_vector = field_function((x[i][j][k], y[i][j][k], z[i][j][k]))[1]
                u[i][j].append(field_vector[0])
                v[i][j].append(field_vector[1])
                w[i][j].append(field_vector[2])
    return (u, v, w)

def cross(x, y):
    """Returns cross product of vectors x, y (can be numpy arrays, lists, tuples, or any indexable vector like structures with 3 entries)
    This was done as numpy's cross product function had too much overhead and was thus too slow for the uses in this project
    """
    a = ((x[1] * y[2]) - (x[2] * y[1]))
    b = ((x[2] * y[0]) - (x[0] * y[2]))
    c = ((x[0] * y[1]) - (x[1] * y[0]))
    return np.array((a,b,c), dtype)