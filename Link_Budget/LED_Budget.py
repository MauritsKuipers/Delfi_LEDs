## Code made by MDMLK ##
import numpy as np
import math
import matplotlib

#########################################################################################################
################## NEW VERSION USING CLASSES FOR ORGANIZATION ###########################################
######### FOR NOW IT IS ALL IN ONE File BUT IT MIGHT BE SEPARATED INTO DIFFERNT FILES ###################
#########################################################################################################

################### LED ###################
class LED:
    # Source: https://www.epigap-osa.com/Datasheets/Starboard/OCI-490-20_MUR_Star.pdf
    # COMMENT: This might become difficult to make an automatic parser as LEDs will have different Documentation (PROBLEM FOR FUTURE MAURITS)
    def __init__(self):
        self.wavelength                                 = 660                           # [nm] red colour
        self.Uf                                         = {350: 2.5, 1000: 4.1}         # Forward Voltage mA & V
        self.radiant_intensity                          = {"min": 450, "typ": 850}      # mW/sr radiant intensity per squared radian (steradian aka the solid angle)
        self.radiant_power                              = 260                           # [mW]
        self.LED_emitter_diameter                       = 5                             # [mm]
        self.divergence_angle                           = np.deg2rad(90)                # [rad] This angle was determined "by visual inspection" as there is no data given but the LED looks like for 180 dispersion
        self.performance_radiant_intensity              = {}                            # Possible Location to Save all Performance Characteristics Determined from the LinkBudget Calculations
        self.performance_radiant_power                  = {}                            # Possible Location to Save all Performance Characteristics Determined from the LinkBudget Calculations

    # Maybe more function inside this class can be made in case some characteristics needed to determined from the given data #

    def transmitted_power_link(self):
        self.P_transmitted = 10 * np.log10((self.radiant_power) / 1)                    # [dBm] This is the transmitted power in for use in the link budget

################### CONSTANTS & ORBIT ###################
class Constants:
    def __init__(self):
        self.PlanetRadius = 6378                                 # [km]

class Orbit:                                                        # Source: Dr. Speretta, Dr. Langbroek, Eventual Ir. Kuipers
    def __init__(self):
        self.OrbitAltitude          = 750                           # [km] Assumed Maximum Orbit Altitude
        self.Elevation              = 40                            # [deg] REASONING TO BE GIVEN, TEMPORARY VALUE


################### TELESCOPES ###################
class DelftTelescope:                                               # Source:
    def __init__(self):
        self.LensDiameter           = 17                            # [mm]
        self.TelescopeHeight        = 0                             # [m] Assumed 0 for simplification and "worse case scenario"
        self.maximum_distance       = None                          # Initiate the Attribute

    def maximum_link_distance(self, orbit, constants):                         # This is calculated using: "Link budget calculation in optical LEO satellite downlinks with on/off-keying and large signal divergence: A simplified methodology"
        L = np.sqrt( (constants.PlanetRadius + self.TelescopeHeight)**2 * (np.sin(np.deg2rad(orbit.Elevation)))**2 + 2*(orbit.OrbitAltitude - self.TelescopeHeight) *
                     (constants.PlanetRadius + self.TelescopeHeight) + (orbit.OrbitAltitude - self.TelescopeHeight)**2 ) - (constants.PlanetRadius + self.TelescopeHeight) * np.sin(np.deg2rad(orbit.Elevation))
        self.maximum_distance = L

class LeidenTelescope:                                              # Source:
    def __init__(self):
        self.LensDiameter           = 00                            # [mm] TBD
        self.TelescopeHeight        = 00                            # [m] Assumed 0 for simplification and "worse case scenario"
        self.maximum_distance       = None                          # Initiate the Attribute

    def maximum_link_distance(self, orbit):                         # This is calculated using: "Link budget calculation in optical LEO satellite downlinks with on/off-keying and large signal divergence: A simplified methodology"
        L = np.sqrt( (orbit.PlanetRadius + self.TelescopeHeight)**2 * (np.sin(np.deg2rad(orbit.Elevation)))**2 + 2*(orbit.OrbitRadius - self.TelescopeHeight) *
                     (orbit.PlanetRadius + self.TelescopeHeight) + (orbit.OrbitRadius - self.TelescopeHeight)**2 ) - (orbit.PlanetRadius + self.TelescopeHeight) * np.sin(np.deg2rad(orbit.Elevation))
        self.maximum_distance = L


################### LINK BUDGETS ###################
class LinkBudget_Naval:                                             # Source: https://apps.dtic.mil/sti/trecms/pdf/AD1201034.pdf
    def __init__(self):
        self.GeometricLoss          = 0                             # Initialization of Variable
        self.ExtinctionLoss         = 0                             # Initialization of Variable
        self.TransmittedPower       = 0                             # Initialization of Variable

    def geometric_loss(self, delft_telescope, led, orbit):
        Dr = delft_telescope.LensDiameter * 10 ** (-3)                       # The diameter of the receiving aperture [m]
        Dt = led.LED_emitter_diameter * 10 ** (-3)               # [m] The diameter of transmitting aperture (might not be applicable to LED) [m]
        theta1 = led.divergence_angle * 10 ** (3)               # [mrad] Divergence Angle of the Beam [milli-radians]
        L1 = orbit.OrbitAltitude                                # Link Distance [km]  COMMENT: FOR NOW IT IS AT JUST ORBIT HEIGHT, CAN BE CHANGED TO THE MAXIMUM LINK DISTANCE

        Lgeom = -20 * np.log10(Dr / (Dt + theta1 * L1))  # dB
        self.GeometricLoss = Lgeom

    def extinction_loss(self, led):
        # Extinction Loss Le #
        lambda1 = led.wavelength        # Wavelength of the emitted light
        delta1 = 1.6                # Particle Size Distribution Coefficient
        V1 = 100 * 10 ^ 3           # [m] Meteorological Visibility (as this is relatred to the atmosphere it is also capped at 100km)
        d1 = 100 * 10 ^ 3           # [m] Atmospheric Path Distance (This should be limited to 100km as maximum atmospheric thickness)

        alphae                  = 3.91 / V1 * (lambda1 / 550) ** (-delta1)

        Le                      = -10 * np.log10(np.e ** (-alphae * d1))  # dB
        self.ExtinctionLoss     = Le


    def link_budget(self, led):
        La = 0
        Gr = 0  # Assumed a receiver gain of 0 for safety
        self.link_budget = led.P_transmitted - (Gr + La + self.ExtinctionLoss + self.GeometricLoss)


class LinkBudget_source:        # Source: Given as a PDF but I believe it is this one - https://onlinelibrary.wiley.com/doi/10.1002/sat.1478

    def __init__(self):
        return

class LinkBudgetTUD:                                               # Source: Slides from Dr. Speretta
    def __init__(self):
        self.L_free_space_loss          = 0                             # Initialization of Variable

    def free_space_loss(self, orbit, led):
        d1                      = orbit.OrbitAltitude                                                   # [km] Distance between transmitter and receiver
        lambda1                 = led.wavelength                                                        # [nm] Wavelength
        self.L_free_space_loss  = 20 * np.log10(4 * np.pi * (d1 * 10 ** 3) / (lambda1 * 10 ** (-9)))
    def link_budget(self, led):
        La = 0
        Gr = 0  # Assumed a receiver gain of 0 for safety
        self.link_budget = led.P_transmitted - (Gr + La + self.L_free_space_loss)


## Initiate the Generic Classes for Any Method ##
print("WARNING: ATTENTION TO THE DISTANCE USED, AS FOR NOW IT IS JUST TAKEN THE ORBITAL HEIGHT")
led = LED()
led.transmitted_power_link()
constants = Constants()
orbit = Orbit()
delft_telescope = DelftTelescope()
delft_telescope.maximum_link_distance(orbit, constants)

## Using the Naval PostGraduate Method ##
linkBudget_naval = LinkBudget_Naval()
linkBudget_naval.geometric_loss(delft_telescope, led, orbit)
linkBudget_naval.extinction_loss(led)
linkBudget_naval.link_budget(led)

print("=====================NAVAL POSTGRADUATE========================================")
print("The Geometric Loss is: ", linkBudget_naval.GeometricLoss)
print("The Extinction Loss is: ", linkBudget_naval.ExtinctionLoss)
print("The Transmitted Power Link is: ", led.P_transmitted)
print("The determined link budget of the LED is", linkBudget_naval.link_budget)


## Using the TU Delft Method ##
linkBudget_TUD = LinkBudgetTUD()
linkBudget_TUD.free_space_loss(orbit, led)
linkBudget_TUD.link_budget(led)

print("=====================TUD========================================")
print("The Transmitted Power Link is: ", led.P_transmitted)
print("The Free Space Loss is: ", linkBudget_TUD.L_free_space_loss)
print("The determined link budget of the LED is", linkBudget_TUD.link_budget)

