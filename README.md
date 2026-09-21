# 🦊Field Ecosystem Simulation
An ecosystem simulation with natural selection and graphing of population and trait changes over time made with Python using pygame, numpy and matplotlib. Contains a food chain with grass, rabbits and foxes with traits that can change over generations, shown at the end of each simulation in an array of subplots.

## Technologies
- Python
- Pygame
- Numpy
- Matplotlib

## Features
- Energy based actions so there are trade-offs to trait changes
- Inheritable traits (speed, detection radius, random wandering) with mutation over generations
- Seeded and headless options for reproducible results
- Species traits defined in an initial dictionary for seamless addition of new fauna
- Spatial hash for optimised performance with large amounts of entities

## Running the Project
1. Clone the repository
2. Install dependencies (pip install pygame numpy matplotlib)
3. Set "ENABLE_RENDER", "MAX_TICKS" and the seed at the top of the .py file to configure the simulation to your liking. The population and trait-change plots will show once the simulation ends or is manually quit.
4. Run the .py file




