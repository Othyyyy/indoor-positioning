# indoor-positioning

## Indoor Positioning System using Raspberry Pis and Hotspot Connectivity
This project aims to estimate the coordinates of a phone inside a classroom using an indoor positioning script. The system utilizes four Raspberry Pis connected to the phone's hotspot for data collection and analysis.

## Setup
- Hardware : Four Raspberry Pis and an iPhone 13 Pro serving as a hotspot.
- Connect the Raspberry Pis to the iPhone's hotspot to establish an internet connection.
## Data Collection
- The Raspberry Pis utilize the iwconfig command to extract the Received Signal Strength Indicator (RSSI) of the signal received from the phone.
- Using the Okumura-Hata model, the distance between each Raspberry Pi and the phone is calculated based on the obtained RSSI values. The Okumura-Hata model utilizes the formula d = 10^((P̅ - b) / (10 * a)), where P̅ is the received power, a and b are parameters of a linear equation, and d represents the distance.
- The parameters a and b are calculated using the least squares method, resulting in values of a = -2.07 and b = -32.81. These values allow for distance calculation from the RSSI values.
## Data Sharing and Processing
- One of the Raspberry Pis opens a socket to share the calculated distances with the main Raspberry Pi responsible for the final estimation of the phone's location.
- Each Raspberry Pi has its own IP address, and the main Raspberry Pi verifies that the three IPv4 addresses match those of the connected Raspberry Pis.
- Once all three Raspberry Pis are connected, they share the distances they have calculated with the main Raspberry Pi.
## Location Estimation
- The main Raspberry Pi utilizes the Euclidean distance formula, treating the four distances as the radii of four circles. The center coordinates of the four circles are known, as the coordinates of the four Raspberry Pis are already determined.
- The location estimation is optimized using the Nelder-Mead algorithm for minimization.
- Finally, the system provides an estimation of the coordinates of the phone based on the collected data and calculations.
