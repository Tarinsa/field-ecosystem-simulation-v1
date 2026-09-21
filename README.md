# 🦊Field Ecosystem Simulation
An agent based model of a field ecosystem containing grass, rabbits and foxes in Python with Pygame. Inherited traits mutate through generations to allow for natural selection to emerge over time, with changes to population and traits plotted with matplotlib at the end of a simulation. Traits that can change include speed, detection radius and random wandering.
- Python
- Pygame
- Numpy
- Matplotlib

## Features
- Energy based actions so there are trade-offs to increases in speed and random wandering
- Inheritable traits (speed, detection radius, random wandering) with mutation over generations
- Seeded and headless options for reproducible results
- Species traits defined in an initial dictionary for easier addition of new fauna
- Spatial hash for optimised performance with large amounts of entities

## Running the Project
1. Clone the repository
2. Install dependencies (pip install pygame numpy matplotlib)
3. Set "ENABLE_RENDER", "MAX_TICKS" and the seed at the top of the .py file to configure the simulation to your liking. The population and trait-change plots will show once the simulation ends or is manually quit.
4. Run the .py file

## Preview and Results

### GUI Screenshots 

<img width="996" height="594" alt="image" src="https://github.com/user-attachments/assets/503c3a3b-a706-4b33-a7f9-5f1d9c8ed207" />


