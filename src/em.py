import numpy as np
import utility

# All units are in standard SI units

class Field:
    def __init__(self):
        self.name = "Field"
        self.field_methods = (self.field_B,) # a tuple of field method functions for the all_fields method to use for calling individual field methods

    def all_fields(self, position):
        """Returns a dictionary with entries having keys denoting field type and value denoting field strength at position argument
        """
        return dict(method(position) for method in self.field_methods)

    def field_B(self, position):
        return ("field_B", utility.zero_vec.copy())

class Uniform_B_Field(Field):
    """
    Simulates an uniform magnetic field
    """
    def __init__(self, B_vector):
        super().__init__()
        self.field_methods = (self.field_B,)
        self.B_vector = B_vector
        self.name = "Uniform_B_Field"

    def field_B(self, position):
        return ("field_B", self.B_vector)

class EB_Field(Uniform_B_Field):
    """
    Simulates an uniform magnetic and electric field
    """
    def __init__(self, B_vector, E_vector):
        super().__init__(B_vector)
        self.field_methods = (self.field_B, self.field_E,)
        self.E_vector = E_vector
        self.name = "EB_Field"
    
    def field_E(self, position):
        return ("field_E", self.E_vector)

class GB_Field(Uniform_B_Field):
    """
    Simulates an uniform magnetic and gravitational field
    """
    def __init__(self, B_vector, G_vector):
        super().__init__(B_vector)
        self.field_methods = (self.field_B, self.field_G,)
        self.G_vector = G_vector
        self.name = "GB_Field"
    
    def field_G(self, position):
        return ("field_G", self.G_vector)

class Toroidal_B_Field(Field): 
    """
    Simulates a toroidal magnetic field
    """
    def __init__(self, coil_num, current, inner_radius, outer_radius):
        self.field_methods = (self.field_B, )
        self.coil_num = coil_num
        self.current = current
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.z_top = (self.outer_radius - self.inner_radius) / 2
        self.z_bot = -self.z_top
        self.name = "Toroidal_B_Field"
        self.strength_factor = utility.permeability_of_free_space * self.coil_num * self.current / (2 * np.pi)# the constant part of the magnetic field equation for toroid, placed here to improve speed
    
    def field_B(self, position):
        """
        The toroidal B field is shaped with a square cross section and centred about the axis x=y=0; B vectors point anti-clockwise when viewed downwards from the +z direction, i.e. in the direction where +90 degrees separation exists from +x direction to +y direction
        """
        radius_vec = self.radius_vec(position)
        r = np.sqrt(radius_vec.dot(radius_vec)) # modulus of radius_vec; 
        if r > self.inner_radius and r < self.outer_radius and position[2] < self.z_top and position[2] > self.z_bot: # checks that particle position is within the toroidal field region
            # Below cross product yields vector in direction perpendicular to radius vector and vector pointing in the +z axis direction; the resulting vector is also scaled to have magnitude = self.strength_factor / r
            B_vector = np.cross(np.array((0,0, self.strength_factor / r), utility.dtype), radius_vec) / r
        else:
            B_vector = utility.zero_vec.copy()
        return ("field_B", B_vector)
    
    def radius_vec(self, position):
        return np.array((position[0], position[1], 0), utility.dtype)


class Tokamak_Field(Toroidal_B_Field):
    """
    Simulates a tokamak field based on the toroidal B field above with the addition of uniform electric and gravitational field
    """
    def __init__(self, coil_num, current, inner_radius, outer_radius, E_vector, G_vector):
        super().__init__(coil_num, current, inner_radius, outer_radius)
        self.field_methods = (self.field_B, self.field_E, self.field_G)
        self.E_vector = E_vector
        self.G_vector = G_vector
        self.name = "Tokamak_Field"

    def field_E(self, position):
        return ("field_E", self.E_vector)

    def field_G(self, position):
        return ("field_G", self.G_vector)

class Particle:
    """
    Represents a general charged particle
    """
    def __init__(self, mass=0, charge=0, position=utility.zero_vec.copy(), velocity=utility.zero_vec.copy(), field=Field()):
        self.mass = mass
        self.charge = charge
        self.position = position
        self.velocity = velocity
        self.field = field # the class instance representing the field as to which the particle lies in

        # Initialses confinement escape status variable; assumes input particle parameters leave particle inside confinement magnetic field to start with
        if self.field.name in ("Tokamak_Field", "Toroidal_B_Field"):
            self.escaped = False
    
    def update(self, dt):
        """Updates particle kinematics according to some input timestep dt using RK4
        Args:
            dt: float value representing timestep in units s
        For toroidal field and tokamak field; this method also checks for whether particle has escaped magnetic confinement, if so it returns True, else by default returns None
        """
        self.position, self.velocity = utility.two_eq_rk4(self.position, self.get_v, self.velocity, self.get_a, dt)

        # Returns signal at the first time when particle escapes magnetic confinement
        if self.field.name in ("Tokamak_Field", "Toroidal_B_Field"):
            if self.escaped == False and np.all(self.field.field_B(self.position)[1] == utility.dtype(0)):
                self.escaped = True # set escape status as True such that the method won't return True again after the first time particle escapes confinement
                return True

    def get_a(self, position, velocity):
        """Returns particle acceleration given position and velocity arguments
        """
        return self.total_force(position, velocity) / self.mass

    def get_v(self, position, velocity):
        """Returns particle velocity given position and velocity arguments (trivial but included for sake of consistency with get_a when calling RK4)
        """
        return velocity
    
    def total_force(self, position, velocity):
        """ Returns total force vector on particle given position vector, velocity vector argumements 
        """
        total_force = utility.zero_vec.copy()
        fields = self.field.all_fields(position)
        if "field_B" in fields: 
            total_force += self.charge * utility.cross(velocity, fields["field_B"])
        if "field_E" in fields: 
            total_force += self.charge * fields["field_E"]
        if "field_G" in fields: 
            total_force += self.mass * fields["field_G"]             
        return total_force

class Electron(Particle):
    """
    Subclass of Particle representing electrons
    """
    def __init__(self, position=utility.zero_vec.copy(), velocity=utility.zero_vec.copy(), field=Field()):
        super().__init__(utility.electron_mass, -utility.elementary_charge, position, velocity, field)

class Deuterium_Ion(Particle):
    """
    Subclass of Particle representing deuterium ions
    """
    def __init__(self, position=utility.zero_vec.copy(), velocity=utility.zero_vec.copy(), field=Field()):
        super().__init__(utility.deuterium_mass, utility.elementary_charge, position, velocity, field)