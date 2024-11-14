## Code made by MDMLK ##
import numpy as np
import matplotlib

## Data from the LED ##

wavelength = ???
Uf = {350: 2.5, 1000: 4.1}                      # Forward Voltage mA & V
radiant_intensity = {"min": 450, "typ": 850}    # mW/sr radiant intensity per squared radian (steradian aka the solid angle)


## Orbit Properties ##
h = 750 # [km]
## Data from the Camara ##

lens_diamter = 17*10^(-3) # m



### Calculation ###

## Some Physics Questions ##
# Solid Angles #
A1          = np.pi * (lens_diamter/2)^(2)
r           = h * 10^(3)                    # [m]
solidangle1 = A1 / r^(2)

# Power Reached to the Camera #
P_transmitted_reached_area = radiant_intensity * solidangle1    # Would this be geometric loss?


## Post-Doc Thesis ###
# Extinction Loss Le #
lambda1     = 1.6           # Particle Size Distribution Coefficient
V1          = 100*10^3      # Meteorological Visibility [m] (as this is relatred to the atmosphere it is also capped at 100km)
wavelength  = wavelength    # This is the wavelength of the emmited beam [nanometer]
d1          = 100*10^3      # Atmospheric Path Distance (This should be limited to 100km as maximum atmospheric thickness)

alphae  = 3.91 / V1 * (lambda1 / 550)^(-delta1)

Le      = -10 * np.log(e^(-alphae * d1))      # dB

# Geometric Loss Lgeom #
Dr      = lens_diamter   # The diameter of the receiving aperture [m]
Dt      = ????           # The diameter of transmitting aperture (might not be applicable to LED) [m]
theta1  = ???            # Divergence Angle of the Beam [milli-radians]
L1      = ???            # Link Distance [km]

Lgeom   = -20 * np.log( Dr / (Dt + theta1 * L1))      # dB

# Atmospheric Loss La #

(Need to revide this one)

la      = 10 * np.log( np.sqrt(1 - sigmai ^ (2)) )




# Total Link Budget #

Pt = ???        # Transmitter Power
Pr = ???        # Receiver Power
Gr = ???        # ?????

link_budget = P_transmitted_reached_area - ( Gr + La + Le + Lgeom)

if link_budget = 3 or link_budget > 3:
    print("Link Budget Sufficient for the Margin Requirement of 3dB")
else:
    print("Link Budget Insufficient for the Margin Requirement of 3dB")


