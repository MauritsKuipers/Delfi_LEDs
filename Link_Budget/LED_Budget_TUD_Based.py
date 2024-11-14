## Code made by MDMLK ##
import numpy as np
import matplotlib

## Data from the LED ##

Uf = {350: 2.5, 1000: 4.1} # Forward Voltage mA & V




## Data from the Camara ##

lens_diamter = 17 # mm



### Calculation ###

# Free Space Loss L_free_space_loss #
d1      = ???   # Distance between transmitter and receiver
lambda1 = ???   # Wavelength

L_free_space_loss = 20 * np.log(4 * np.pi * d1 / lambda1)

#
