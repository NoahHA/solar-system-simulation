# Solar System Simulation using Python and RK4 Integration Algorithm


This project uses the RK4 algorithm to simulate the orbits of Mercury, Venus, Earth, and Mars around the Sun. The project is written in python making use of matplotlib to animate the orbits and numpy to perform the integrations.

The relative velocities, orbital time periods, sizes, and distances of the planets are all accurate. The size of the Sun is just chosen to look good as the actual Sun size is so large that it would eclipse many of the planets and ruin the look of the simulation. I initially tried to simulate all 8 planets in the solar system but found that the size of the orbits for the gas giants were so large that the inner planets couldn't be seen anymore. There was also the problem that making planets like Jupiter to scale meant that smaller planets like mercury became invisible, especially if I wanted the planets to still be larger than the Sun.

The program is very simple to use, simply enter a number of years to run the simulation (between 0 and 50) and the simulation will run for that time period. I decided to cut it off at 50 as the program does all the integration before running so longer simulations end up taking too long to run. In the future I might make it so that the user can select the number of planets they want to simulate rather than always doing 4, but that would require making some concessions to the accuracy of the simulation in order for it to actually be interesting to watch.
