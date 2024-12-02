### Thid file was made to attempt to make a "link budget"using luminous "properties"of known detectable LED light emitted ###
### This will start very simplistic method as first level "analysis"

import numpy as np
import math

def find_closest_key_with_numpy(number, dictionary):
    keys = np.array(list(dictionary.keys()))
    closest_key = keys[np.abs(keys - number).argmin()]
    return closest_key


################### Optical Properties Required by Dr. Langbroek ###################
class requirement_optical_prop:

    def __init__(self):
        self.EmittedCandelas    = 180                           # Given by Dr. Langbroek


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
        self.forward_voltage = 2.5  # [V]
        self.current_drain = 0.350  # [A]
        self.LED_area = 20 * 20  # [mm2]


################### CONSTANTS & ORBIT ###################
class Constants:
    def __init__(self):
        self.PlanetRadius           = 6378                          # [km]
        self.atmospheric_altitude   = 100                           # [km]
        self.Boltzmann_mW           = 1.38 *10**(-20)               # [mW/Hz/K]
class Orbit:                                                        # Source: Dr. Speretta, Dr. Langbroek, Eventual Ir. Kuipers
    def __init__(self):
        self.OrbitAltitude          = [598]   # [km] This altitude because that is what Dr. Langbroek Informed us for the Specific Value of Candelas
        self.Elevation              = 45                                                        # [deg] Requirement Given by Dr. Langbroek


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



################### Calculations ###################

# To determnine how much Luminous Intensity (candela) the LED Generates #
class LuminousMethod:

    def __init__(self):
        self.LEDCandela = 0
        self.LEDCount = 0


    def candela_calc(self, led):

        self.LEDCandela = 683.002 * led.radiant_intensity["typ"] * 10**(-3) * 0.061            # This is a semi temporary formula, found online Wikipedia (I am going insane with this one)
        print("The Candelas of One LED is: ", self.LEDCandela)
    def LED_Count(self, requirements):
        self.LEDCount = math.ceil(requirements.EmittedCandelas / self.LEDCandela)
        print("LED Count: ", self.LEDCount)



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
        print("The determined required sensing power is: ", self.P_required_db)

    ## Link Budget ##

    def Transmitted_Power(self, luminousmethod, led, constants):
        self.P_transmitted = 10 * np.log10((led.radiant_power) * luminousmethod.LEDCount / 1)
    # This is the simplified link budget for one LED #

    def link_budget(self):
        La = 0
        Gr = 0  # Assumed a receiver gain of 0 for safety
        for L_free_space in self.L_free_space_loss:
            self.LinkBudget.append( self.P_transmitted - (Gr + La + L_free_space) - self.P_required_db )






## Initiate the Generic Classes for Any Method ##
print("WARNING: ATTENTION TO THE DISTANCE USED, AS FOR NOW IT IS JUST TAKEN THE ORBITAL HEIGHT")
led = LED()
constants = Constants()
orbit = Orbit()
delft_telescope = DelftTelescope()
requirements = requirement_optical_prop()

## Luminous Method ##
luminousmethod = LuminousMethod()
luminousmethod.candela_calc(led)
luminousmethod.LED_Count(requirements)

## Using the TU Delft Method ##
print("=====================TUD========================================")
linkBudget_TUD = LinkBudgetTUD()
linkBudget_TUD.maximum_link_distance(orbit, constants, delft_telescope)
linkBudget_TUD.free_space_loss(orbit, led)
linkBudget_TUD.required_sensing_power(delft_telescope, led, constants)
linkBudget_TUD.Transmitted_Power(luminousmethod , led, constants)
linkBudget_TUD.link_budget()

print("The Transmitted Power Link is: ", linkBudget_TUD.P_transmitted)
print("The Free Space Loss is: ", linkBudget_TUD.L_free_space_loss)
print("The determined link budget of the LED is", linkBudget_TUD.LinkBudget)