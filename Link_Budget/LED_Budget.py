## Code made by MDMLK ##
import numpy as np
import matplotlib


## Choices ##
power_choice = "radiant_power"




## Data from the LED ##
wavelength          = 660                           # [nm] red colour
Uf                  = {350: 2.5, 1000: 4.1}         # Forward Voltage mA & V
radiant_intensity   = {"min": 450, "typ": 850}      # mW/sr radiant intensity per squared radian (steradian aka the solid angle)
radiant_power       = 260                           # [mW]
LED_emiter_diameter = 5                             # [mm]
divergence_angle    = np.deg2rad(180)               # [rad]


## Orbit Properties ##
h = 750 # [km]

## Data from the Camara ##
lens_diamter = 17*10**(-3) # [m]



### Calculation ###
## Some Physics Questions ##

if power_choice == "radiant_intensity":
    # Solid Angles #
    A1          = np.pi * (lens_diamter/2)^(2)  # [m2]
    r           = h * 10^(3)                    # [m]
    solidangle1 = A1 / r^(2)                    # [rad]

    # Power Reached to the Camera #
    P_transmitted_reached_area = radiant_intensity * solidangle1    # Would this be geometric loss?
    P_transmitted = P_transmitted_reached_area

if power_choice == "radiant_power":
    P_transmitted = 10 * np.log10( (radiant_power) / 1)       # [dBm]

## Post-Doc Thesis ###
# Extinction Loss Le #
lambda1     = wavelength    # Wavelength of the emitted light
delta1      = 1.6           # Particle Size Distribution Coefficient
V1          = 100*10^3      # [m] Meteorological Visibility (as this is relatred to the atmosphere it is also capped at 100km)
wavelength  = wavelength    # This is the wavelength of the emmited beam [nanometer]
d1          = 100*10^3      # [m] Atmospheric Path Distance (This should be limited to 100km as maximum atmospheric thickness)

alphae  = 3.91 / V1 * (lambda1 / 550)**(-delta1)

Le      = -10 * np.log10(np.e**(-alphae * d1))      # dB

# Geometric Loss Lgeom #
Dr      = lens_diamter                              # The diameter of the receiving aperture [m]
Dt      = LED_emiter_diameter * 10**(-3)            # [m] The diameter of transmitting aperture (might not be applicable to LED) [m]
theta1  = divergence_angle * 10**(3)               # [mrad] Divergence Angle of the Beam [milli-radians]
L1      = h                                         # Link Distance [km]

Lgeom   = -20 * np.log10( Dr / (Dt + theta1 * L1))      # dB

# Atmospheric Loss La #

# (Need to revide this one)
#
# la      = 10 * np.log( np.sqrt(1 - sigmai ^ (2)) )




# Total Link Budget #
La = 0
Gr = 0                                                      # Assumed a receiver gain of 0 for safety
link_budget = P_transmitted - ( Gr + La + Le + Lgeom)

if link_budget == 3 or link_budget > 3:
    print("Link Budget Sufficient for the Margin Requirement of 3dB", link_budget)
    print("Transmitted Power: ", P_transmitted)
    print("Geometric Loss: ", Lgeom)
    print("Extinction Losses: ", Le)
else:
    print("Link Budget Insufficient for the Margin Requirement of 3dB", link_budget)
    print("Transmitted Power: ", P_transmitted)
    print("Geometric Loss: ", Lgeom)
    print("Extinction Losses: ", Le)

