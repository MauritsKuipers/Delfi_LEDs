## Code made by MDMLK ##
import numpy as np
import matplotlib

## Data from the LED ##

Uf = {350: 2.5, 1000: 4.1} # Forward Voltage mA & V




## Data from the Camara ##

lens_diamter = 17*10^(-3) # m



### Calculation ###

## Post-Doc Thesis ###

# Extinction Loss Le #
delta1  = 1.6           # Particle Size Distribution Coefficient
V1      = ???           # Meteorological Visibility (m)
lambda1 = ???           # This is the wavelength of the emmited beam
d1      = ???           # Atmospheric Path Distance (This should be limited to 100km as maximum atmospheric thickness)

alphae  = 3.91 / V1 * (lambda1 / 550)^(-delta1)

Le      = -10 * np.log(e^(-alphae) * d1)      # dB

# Geometric Loss Lgeom #
Dr      = lens_diamter   # The diameter of the receiver
Dt      = ????           # The diameter of transmitter (might not be applicable to LED)
theta1  = ???            # Divergence Angle of the Beam (milli-radians)
L1      = ???            # Link Distance

Lgeom   = -20 * np.log( Dr / (Dt + theta1 * L1))      # dB

# Atmospheric Loss La #

(Need to revide this one)

la      = 10 * np.log( np.sqrt(1 - sigmai ^ (2)) )




# Total Link Budget #

Pt = ???        # Transmitter Power
Pr = ???        # Receiver Power
Gr = ???        # ?????

link_budget = Pt - (Pr + Gr + La + Le + Lgeom)

if link_budget = 3 or link_budget > 3:
    print("Link Budget Sufficient for the Margin Requirement of 3dB")
else:
    print("Link Budget Insufficient for the Margin Requirement of 3dB")


