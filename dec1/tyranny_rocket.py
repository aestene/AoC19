import pandas as pd
import math

def calculateFuel(mass: int) -> int:
    return (mass // 3) - 2

def recursiveFuelCalculation(mass: int) -> int:
    total_fuel_mass = 0
    fuel_mass = calculateFuel(mass)
    if fuel_mass > 0:
        total_fuel_mass = fuel_mass + recursiveFuelCalculation(fuel_mass)
    else:
        return total_fuel_mass
    return total_fuel_mass

df = pd.read_csv('dec1/input.txt', sep=" ", header=None)
df.columns = ['mass']

df = df.apply(lambda x: recursiveFuelCalculation(x.values[0]), axis=1)

print(df.sum())


