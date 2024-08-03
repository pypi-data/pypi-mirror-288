# UUVMissionSim

## Table of Contents

- [Package Description](#package-description)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Acknowledgements](#acknowledgements)
- [Contact](#contact)

## Package Description

The UUVMissionSim package was developed as part of my master's thesis to provide a comprehensive tool for simulating UUV missions.The package presents a Regional Ocean Modelling System (ROMS)-based Unmanned Underwater Vehicle (UUV) mission simulator. The primary focus was on creating a sophisticated simulation tool that integrates ROMS data to replicate realistic ocean environments and accurately mimic the behavior and data collection processes of UUVs, with a specific emphasis on the T-REMUS vehicle. The developed simulator aims to provide a safe and efficient way to develop and test advanced navigation systems for UUVs.

This package provideas researchers and engineers with a robust foundation for advancing UUV navigation and data collection strategies, providing a tool for developing and testing advanced navigational algorithms in a cost effective way. The simulator's applications span mission planning, virtual ocean studies, and educational purposes, contributing significantly to oceanography and UUV navigation systems.

## Installation

You can install the package using `pip`:

```
bash
pip install UUVMissionSim
```

Alternatively, if you want to install from source:

git clone https://github.com/Prakarsha01/UUVMissionSim.git
cd UUVMissionSim
pip install -e 

## Usage

### Basic Usage

Here is a basic example of how to use the UUVMissionSim package to run a UUV mission simulation. 

Sample dataset is hosted on [huggingface](https://huggingface.co/datasets/Prakarsha01/uuvmissionsim).The below example can be used on the provided dataset:

```
import UUVMissionSim.simulator as simulator

# Define mission parameters
current_point = (13000, 33502, 4)
waypoints = [(13080, 33502, 4), (13005, 34510, 4)]
instructions = [1]
start_time = '2019-05-02T15:04:43.499997011'
max_depth = 8.0
min_depth = 4.0
z_resolution = 0.25
t_resolution = 60
horizontal_speed = 2.0
triangle_speed = 0.5

# Run the simulation
adcp_data, ctd_data, original_path, drift_path, original_time = simulator.run(
    current_point, waypoints, start_time, instructions, max_depth, min_depth, z_resolution, t_resolution, horizontal_speed, triangle_speed
)

# Print or handle the results as needed
print("ADCP Data:", adcp_data)
print("CTD Data:", ctd_data)
print("Original Path:", original_path)
print("Drift Path:", drift_path)
print("Original Time:", original_time)

```
#### Updating Dataset Path
To update the datapaths to your own data you can update the paths as shown below:

```
new_config = {
        'U_PATH': "/data/u.nc",
        'V_PATH': "/data/v.nc",
        'W_PATH': "/data/w.nc",
        'CTD_DATA_PATHS': [
            "/data/salt.nc",
            "/data/rho.nc",
            "/data/temp.nc"
        ]
    }

 # Update configuration
cg.update_config(**new_config)

```

## Configuration

The package uses a config.py file to store various configuration settings such as data paths and sensor frequencies. Ensure to set the appropriate paths and values in config.py:

```
# config.py

# Data Paths
U_PATH = "/path/to/u.nc"
V_PATH = "/path/to/v.nc"
W_PATH = "/path/to/w.nc"
CTD_DATA_PATHS = ["/path/to/salt.nc", "/path/to/temp.nc", "/path/to/rho.nc"]

# Sensor frequency
ADCP_FREQUENCY = 2  # Hz
CTD_FREQUENCY = 16  # Hz

# ADCP Settings
VERTICAL_SPACING = 0.25  # Spacing between z points
Z_ABOVE_PATH = 4  # Maximum depth above the original path
Z_BELOW_PATH = -4  # Maximum depth below the original path
BLANKING_DISTANCE = 0.75 # Blanking distance around UUV
```

## Acknowledgements

This project was made possible with the support and guidance of my advisors, [Dr. Daniel McDonald](https://www.umassd.edu/directory/dmacdonald/) and [Dr. Shelley Zhang](http://www.cis.umassd.edu/~x2zhang/). I am grateful for their trust in my abilities and for giving me the opportunity to tackle such a fascinating problem. Special thanks to [Ágata Piffer Braga](https://www.linkedin.com/in/%C3%A1gata-piffer-braga-42724873/) for her invaluable guidance and support throughout the project. I also want to express my gratitude to [Aakash Kardam](https://www.linkedin.com/in/aakash-kardam-558aaa81/) for his valuable feedback and suggestions; I look forward to seeing his work with the simulator in developing advanced UUV navigation algorithms.

I would also like to thank the [University of Massachusetts Dartmouth](https://www.umassd.edu/) for providing the resources necessary for this research. This package was developed as part of my master's thesis at the University of Massachusetts Dartmouth.

Finally, I extend my heartfelt thanks to my family and friends for their unwavering support and encouragement throughout this journey.

## Contact

For further information, please feel free to connect with me on [LinkedIn](https://www.linkedin.com/in/rp-kandukuri/).