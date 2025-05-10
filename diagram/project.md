# Project Overview

Welcome to the Network Queue Management Simulation project!

## Navigation
- [FIFO Algorithm](fifo.md)
- [Project Structure](structure.md)
- [Simulation Flow](simulation.md)

## System Overview

```mermaid
graph TD
    A[Simulation] --> B[FIFO Queue]
    A --> C[PIE Queue]
    A --> D[Network Link]
    A --> E[Statistics Collector]
    B --> F[Packet Processing]
    C --> F
    D --> F
    E --> F
```

This project simulates and compares FIFO and PIE queue management algorithms in a network environment. Use the links above to explore specific aspects of the project. 