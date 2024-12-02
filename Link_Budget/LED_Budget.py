## Code made by MDMLK ##
import numpy as np
import math
import matplotlib.pyplot as plt
import os
#########################################################################################################
################## NEW VERSION USING CLASSES FOR ORGANIZATION ###########################################
######### FOR NOW IT IS ALL IN ONE File BUT IT MIGHT BE SEPARATED INTO DIFFERNT FILES ###################
#########################################################################################################

################### Support Functions that Can be Used Around ###################

# This function was made because here we have the problem of discretized dictionaries but values that dont exactly exist in the dictionary so we get the closest
def find_closest_key_with_numpy(number, dictionary):
    keys = np.array(list(dictionary.keys()))
    closest_key = keys[np.abs(keys - number).argmin()]
    return closest_key

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
        self.PlanetRadius           = 6378                          # [km]
        self.atmospheric_altitude   = 100                           # [km]
        self.Boltzmann_mW           = 1.38 *10**(-20)               # [mW/Hz/K]
class Orbit:                                                        # Source: Dr. Speretta, Dr. Langbroek, Eventual Ir. Kuipers
    def __init__(self):
        self.OrbitAltitude          = [250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750]                           # [km] Assumed Maximum Orbit Altitude
        self.Elevation              = 40                                                        # [deg] REASONING TO BE GIVEN, TEMPORARY VALUE


################### TELESCOPES ###################
class DelftTelescope:                                               # Camera ZWO ASI 6200MM PRO Source: Dr. Langbroek and https://www.zwoastro.com/product/asi6200/
    def __init__(self):
        self.LensDiameter           = 17                            # [mm]
        self.TelescopeHeight        = 0                             # [m] Assumed 0 for simplification and "worse case scenario"
        self.RelativeSpectralResponse       = {350: 0.25, 400: 0.8, 450: 0.98, 500: 0.98, 550: 0.98, 600: 0.98,
                                       650: 0.96, 700: 0.95, 750: 0.92, 800: 0.9, 850: 0.85, 900: 0.82,
                                       950: 0.8, 1000: 0.78, 1050: 0.75, 1100: 0.72}  # [nm: -] This is taken from an image sent by Dr. Langbroek and it is just an eye estimation for initial calculations
        self.TemperatureSystem      = 308.15                        # [K] taken from the webpage from "Cooling temperature"
        self.SN = 46  # [dB]
        self.TemperatureSystem = 313.15  # [K] took the highest operating temperature from the source


class LeidenTelescope:                                              # Camera WATEC 902H2 Supreme Source: Dr. Langbroek (Emails) and https://www.watec-shop.com/_bibli/catalogue/2/docs/1-wat-902h2-supreme-specifications.pdf
    def __init__(self):
        self.LensDiameter           = 00                            # [mm] TBD
        self.TelescopeHeight        = 00                            # [m] Assumed 0 for simplification and "worse case scenario"
        self.RelativeSpectralResponse       = {400: 0.5, 450: 0.7, 500: 0.95, 550: 0.92, 600: 0.98, 620: 1,
                                       650: 0.9, 700: 0.72, 750: 0.55, 800: 0.42, 850: 0.3, 900: 0.2,
                                       950: 0.1, 1000: 0.7 }        # [nm: -] This is taken from an image sent by Dr. Langbroek and it is just an eye estimation for initial calculations
        self.MinimumIllumincation   = 0.0003                        # [lx F1.4 (AGC=HI)]
        self.SN                     = 46                            # [dB]
        self.TemperatureSystem      = 313.15                        # [K] took the highest operating temperature from the source


################### LINK BUDGETS ###################
class LinkBudget_Naval:                                             # Source: https://apps.dtic.mil/sti/trecms/pdf/AD1201034.pdf
    def __init__(self):
        self.maximum_distance       = []                                # Initialization of Variable
        self.GeometricLoss          = []                                # Initialization of Variable
        self.ExtinctionLoss         = 0                                 # Initialization of Variable
        self.TransmittedPower       = []                                # Initialization of Variable
        self.LinkBudget            = []

    ## Maximum Link Distance ##
    def maximum_link_distance(self, orbit, constants, telescope):                         # This is calculated using: "Link budget calculation in optical LEO satellite downlinks with on/off-keying and large signal divergence: A simplified methodology"
        print(orbit.OrbitAltitude)
        for alt in orbit.OrbitAltitude:
            L = np.sqrt( (constants.PlanetRadius + telescope.TelescopeHeight)**2 * (np.sin(np.deg2rad(orbit.Elevation)))**2 + 2*(alt - telescope.TelescopeHeight) *
                     (constants.PlanetRadius + telescope.TelescopeHeight) + (alt - telescope.TelescopeHeight)**2 ) - (constants.PlanetRadius + telescope.TelescopeHeight) * np.sin(np.deg2rad(orbit.Elevation))
            self.maximum_distance.append(L)

    ## Distance Related Losses ##
    def geometric_loss(self, delft_telescope, led, orbit):
        Dr = delft_telescope.LensDiameter * 10 ** (-3)                       # The diameter of the receiving aperture [m]
        Dt = led.LED_emitter_diameter * 10 ** (-3)               # [m] The diameter of transmitting aperture (might not be applicable to LED) [m]
        theta1 = led.divergence_angle * 10 ** (3)               # [mrad] Divergence Angle of the Beam [milli-radians]
        L1 = self.maximum_distance                                # Link Distance [km]  COMMENT: FOR NOW IT IS AT JUST ORBIT HEIGHT, CAN BE CHANGED TO THE MAXIMUM LINK DISTANCE

        for alt in L1:
            Lgeom = -20 * np.log10(Dr / (Dt + theta1 * alt))  # dB
            self.GeometricLoss.append(Lgeom)

    ## Atmosphere Related Losses ##
    def extinction_loss(self, led):
        # Extinction Loss Le #
        lambda1 = led.wavelength        # Wavelength of the emitted light
        delta1 = 1.6                # Particle Size Distribution Coefficient
        V1 = 100 * 10 ^ 3           # [m] Meteorological Visibility (as this is relatred to the atmosphere it is also capped at 100km)
        d1 = 100 * 10 ^ 3           # [m] Atmospheric Path Distance (This should be limited to 100km as maximum atmospheric thickness)

        alphae                  = 3.91 / V1 * (lambda1 / 550) ** (-delta1)

        Le                      = -10 * np.log10(np.e ** (-alphae * d1))  # dB
        self.ExtinctionLoss     = Le

    ## Link Budget ##
    def link_budget(self, led):
        La = 0
        Gr = 0  # Assumed a receiver gain of 0 for safety
        for Lgeom in self.GeometricLoss:
            lb = led.P_transmitted - (Gr + La + self.ExtinctionLoss + Lgeom)
            self.LinkBudget.append(lb)


class LinkBudgetTUD:                                               # Source: Slides from Dr. Speretta
    def __init__(self):
        self.maximum_distance       = []                                # Initialization of Variable
        self.L_free_space_loss          = []                             # Initialization of Variable
        self.LinkBudget                 = []

    def maximum_link_distance(self, orbit, constants, telescope):                         # This is calculated using: "Link budget calculation in optical LEO satellite downlinks with on/off-keying and large signal divergence: A simplified methodology"
        print(orbit.OrbitAltitude)
        for alt in orbit.OrbitAltitude:
            L = np.sqrt( (constants.PlanetRadius + telescope.TelescopeHeight)**2 * (np.sin(np.deg2rad(orbit.Elevation)))**2 + 2*(alt - telescope.TelescopeHeight) *
                     (constants.PlanetRadius + telescope.TelescopeHeight) + (alt - telescope.TelescopeHeight)**2 ) - (constants.PlanetRadius + telescope.TelescopeHeight) * np.sin(np.deg2rad(orbit.Elevation))
            self.maximum_distance.append(L)

    ## Distance Related Losses ##
    def free_space_loss(self, orbit, led):
        for d1 in self.maximum_distance:                                                  # [km] Distance between transmitter and receiver
            lambda1                 = led.wavelength                                                        # [nm] Wavelength
            self.L_free_space_loss.append( 20 * np.log10(4 * np.pi * (d1 * 10 ** 3) / (lambda1 * 10 ** (-9))) )

    ## Required Received Power ##

    def required_sensing_power(self, telescope, LED, constants):
        SNR                 = telescope.SN
        Temperature_system  = telescope.TemperatureSystem
        Bandwidth           = 1                                 # This needs review as normally this noise is given for communications that occur over a bandwidth of Hz but I am looking at one frequency of light emitted by the LED
        approx_wavelength   = find_closest_key_with_numpy(LED.wavelength, telescope.RelativeSpectralResponse)
        QE                  = telescope.RelativeSpectralResponse[approx_wavelength]
        P_noise_dB  = 10 * np.log10((constants.Boltzmann_mW * Temperature_system * Bandwidth) / QE)

        self.P_required_db       = SNR + P_noise_dB
        print("The determined required power is: ", self.P_required_db)

    ## Link Budget ##
    # This is the simplified link budget for one LED #
    def link_budget(self, led):
        La = 0
        Gr = 0  # Assumed a receiver gain of 0 for safety
        for L_free_space in self.L_free_space_loss:
            self.LinkBudget.append( led.P_transmitted - (Gr + La + L_free_space) - self.P_required_db )


class LinkBudget_source:        # Source: Given as a PDF but I believe it is this one - https://onlinelibrary.wiley.com/doi/10.1002/sat.1478

    def __init__(self):
        self.L_free_space_loss = 0


################### FUNCTIONS TO MAKE THE GRAPHS ###################
def plot_geometric_loss(naval, TUD, source, orbit):

    geometric_loss_naval = naval.GeometricLoss
    free_space_loss_TUD = TUD.L_free_space_loss
    free_space_loss_Source = source.L_free_space_loss

    x = orbit.OrbitAltitude

    plt.plot(x, geometric_loss_naval, color="blue", marker='o', label="NAVAL")
    plt.plot(x, free_space_loss_TUD, color="red", marker='x', label="TUD")
    # plt.plot(x, free_space_loss_Source, color="green", marker='s', label="SOURCE")

    plt.title("Geometric Losses of Different Methods")
    plt.xlabel("Distance [km]")
    plt.ylabel("Loss [dB]")
    plt.grid(False)
    plt.legend()
    plt.show()

def plot_atmospheric_loss(naval, TUD, source):

    atmospheric_loss_naval = naval.GeometricLoss
    atmospheric_TUD = TUD.L_free_space_loss
    atmospheric_Source = source.L_free_space_loss

    x = 750

    plt.plot(x, atmospheric_loss_naval, color="blue", marker='o', label="NAVAL")
    plt.plot(x, atmospheric_TUD, color="red", marker='x', label="TUD")
    plt.plot(x, atmospheric_Source, color="green", marker='s', label="SOURCE")

    plt.title("Atmospheric Losses of Different Methods")
    plt.xlabel("Distance [km]")
    plt.ylabel("Loss [dB]")
    plt.grid(False)
    plt.legend()
    plt.show()

def plot_budget_link(naval, TUD, source):

    link_budget_naval = naval.link_budget
    link_budget_TUD = TUD.link_budget
    link_budget_Source = source.link_budget

    x = 750

    plt.plot(x, link_budget_naval, color="blue", marker='o', label="NAVAL")
    plt.plot(x, link_budget_TUD, color="red", marker='x', label="TUD")
    plt.plot(x, link_budget_Source, color="green", marker='s', label="SOURCE")

    plt.title("Geometric Losses of Different Methods")
    plt.xlabel("Distance [km]")
    plt.ylabel("Loss [dB]")
    plt.grid(False)
    plt.legend()
    plt.show()

## Initiate the Generic Classes for Any Method ##
print("WARNING: ATTENTION TO THE DISTANCE USED, AS FOR NOW IT IS JUST TAKEN THE ORBITAL HEIGHT")
led = LED()
led.transmitted_power_link()
constants = Constants()
orbit = Orbit()
delft_telescope = DelftTelescope()

## Using the Naval PostGraduate Method ##
print("=====================NAVAL POSTGRADUATE========================================")
linkBudget_naval = LinkBudget_Naval()
linkBudget_naval.maximum_link_distance(orbit, constants, delft_telescope)
linkBudget_naval.geometric_loss(delft_telescope, led, orbit)
linkBudget_naval.extinction_loss(led)
linkBudget_naval.link_budget(led)

print("The Geometric Loss is: ", linkBudget_naval.GeometricLoss)
print("The Extinction Loss is: ", linkBudget_naval.ExtinctionLoss)
print("The Transmitted Power Link is: ", led.P_transmitted)
print("The determined link budget of the LED is", linkBudget_naval.LinkBudget)


## Using the TU Delft Method ##
print("=====================TUD========================================")
linkBudget_TUD = LinkBudgetTUD()
linkBudget_TUD.maximum_link_distance(orbit, constants, delft_telescope)
linkBudget_TUD.free_space_loss(orbit, led)
linkBudget_TUD.required_sensing_power(delft_telescope, led, constants)
linkBudget_TUD.link_budget(led)

print("The Transmitted Power Link is: ", led.P_transmitted)
print("The Free Space Loss is: ", linkBudget_TUD.L_free_space_loss)
print("The determined link budget of the LED is", linkBudget_TUD.LinkBudget)


## Using the Source Given ##
print("=====================SOURCE========================================")
linkBudget_source = LinkBudget_source()

print("The Transmitted Power Link is: ", led.P_transmitted)
print("The Free Space Loss is: ", linkBudget_TUD.L_free_space_loss)
print("The determined link budget of the LED is", linkBudget_TUD.LinkBudget)


print("=====================GRAPHS========================================")
## Making Plots ##
plot_geometric_loss(linkBudget_naval, linkBudget_TUD, linkBudget_source, orbit)

