# Network Simulation: FIFO vs CODEL AQM Comparison

This project implements a network simulation comparing two Active Queue Management (AQM) algorithms: FIFO and CODEL. The simulation models a network with three different types of traffic sources (FTP, WEB, and VIDEO) and analyzes their performance under different queue management strategies.

## Project Structure

- `network_components.py`: Contains the core network components (Host, Router, Server) and packet definitions
- `simulation.py`: Main simulation script that runs the comparison and generates results
- `requirements.txt`: Python package dependencies
- `simulation_results.png`: Generated plots comparing FIFO and CODEL performance
- `simulation_report.json`: Detailed simulation results and metrics

## Requirements

- Python 3.7+
- Required packages (install using `pip install -r requirements.txt`):
  - simpy
  - numpy
  - pandas
  - matplotlib

## Running the Simulation

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the simulation:
   ```bash
   python simulation.py
   ```

The simulation will:
- Run for 60 seconds
- Generate 100 packets from each host type (FTP, WEB, VIDEO)
- Compare FIFO and CODEL queue management
- Generate performance plots and a detailed report

## Simulation Parameters

- Queue Size: 100 packets
- Simulation Time: 60 seconds
- Packet Size Ranges:
  - FTP: 500-1500 bytes
  - WEB: 100-1000 bytes
  - VIDEO: 1000-5000 bytes
- CODEL Parameters:
  - Target Delay: 5ms
  - Interval: 100ms

## Output

The simulation generates two main output files:

1. `simulation_results.png`: Contains four plots:
   - Packet Loss Comparison
   - Average Queue Delay
   - Throughput
   - Per-Host Average Delay

2. `simulation_report.json`: Detailed metrics including:
   - Total packets sent/received
   - Packet loss statistics
   - Average delays
   - Per-host metrics
   - Simulation parameters

## Understanding the Results

- **Packet Loss**: Lower is better. CODEL typically shows better packet loss characteristics by proactively dropping packets when delays exceed the target.
- **Queue Delay**: Lower is better. CODEL aims to maintain a target delay by dropping packets when necessary.
- **Throughput**: Higher is better. This shows the rate of successfully delivered packets.
- **Per-Host Delay**: Shows how different traffic types are affected by each AQM strategy.

## Customization

You can modify the simulation parameters in `simulation.py`:
- Queue size
- Simulation duration
- Packet size ranges
- CODEL parameters (target delay and interval) 