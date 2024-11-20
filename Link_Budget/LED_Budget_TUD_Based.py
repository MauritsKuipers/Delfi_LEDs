## Code made by MDMLK ##
import numpy as np
import math
import matplotlib


## Choices ##
power_choice = "radiant_power"
# power_choice = "radiant_intensity"




## Data from the LED ##
wavelength          = 660                           # [nm] red colour
Uf                  = {350: 2.5, 1000: 4.1}         # Forward Voltage mA & V
radiant_intensity   = {"min": 450, "typ": 850}      # [mW/sr] radiant intensity per squared radian (steradian aka the solid angle)
radiant_power       = 260                           # [mW]
LED_emiter_diameter = 5                             # [mm]
divergence_angle    = np.deg2rad(180)               # [rad] This is a "guess" taken by looking at the LED and it looks like it is intended for 180deg dispersion
forward_voltage     = 2.5                           # [V]
current_drain       = 0.350                         # [A]
LED_area            = 20 * 20                       # [mm2]

## Orbit Properties ##
h = 750 # [km]

## Data from the Camara ##
lens_diamter = 17*10**(-3) # [m]

### Calculation ###
# Free Space Loss L_free_space_loss #
d1      = h             # [km] Distance between transmitter and receiver
lambda1 = wavelength    # [nm] Wavelength

L_free_space_loss = 20 * np.log10(4 * np.pi * (d1* 10**3) / (lambda1 * 10**(-9)))

# Transmitted Power #
if power_choice == "radiant_intensity":
    # Solid Angles #
    A1          = np.pi * (lens_diamter/2)**(2)  # [m2]
    r           = h * 10**(3)                    # [m]
    solidangle1 = A1 / r**(2)                    # [rad]

    # Power Reached to the Camera #
    P_transmitted_reached_area = radiant_intensity["typ"] * solidangle1     # Would this be geometric loss?
    P_transmitted = 10 * np.log10(P_transmitted_reached_area / 1)           # [dBm]

if power_choice == "radiant_power":
    P_transmitted = 10 * np.log10( (radiant_power) / 1)       # [dBm]

# Link Budget #
if power_choice == "radiant_intensity":
    La = 0
    Gr = 0
    link_budget = P_transmitted - (Gr + La)

if power_choice == "radiant_power":
    La = 0
    Gr = 0  # Assumed a receiver gain of 0 for safety
    link_budget = P_transmitted - (Gr + La + L_free_space_loss)



if link_budget == 3 or link_budget > 3:
    print("Link Budget Sufficient for the Margin Requirement of 3dB", link_budget)
    print("Transmitted Power: ", P_transmitted)
    print("Free Space Loss: ", L_free_space_loss)
else:
    print("Link Budget Insufficient for the Margin Requirement of 3dB", link_budget)
    print("Transmitted Power: ", P_transmitted)
    print("Free Space Loss: ", L_free_space_loss)

print("========================================================================")

### Estimating How Many LEDs Needed for Positive Link Budget of at Least 3dB ###
# Estimation of Required Transmitted Power #
Margin      = 3                                 # [dB] as assumed in meeting
P_required  = 10 ** ((L_free_space_loss + Margin) / 10)

# Estimation of Necessary Minimum Amount of LEDs #
number_LEDs = math.ceil(P_required / radiant_power)                 # Need To Check Numbers Snoop Dogg HIGH
print("Estimated Minimum Number of LEDs Needed: ", number_LEDs)

# Some Requirements for the Satellite #

power_drain = (forward_voltage * current_drain) * number_LEDs
total_area  = LED_area * number_LEDs

print("Required Power to Light the LEDs: ", power_drain, "W")
print("Surface Area Needed to Place the LEDs: ", total_area, "mm2")