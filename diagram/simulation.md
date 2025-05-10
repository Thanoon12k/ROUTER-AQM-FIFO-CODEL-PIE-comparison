# Simulation Flow

[Back to Project Overview](project.md)

## Simulation Flowchart

```mermaid
graph TD
    A[Start Simulation] --> B[Initialize Components]
    B --> C[Start Statistics Thread]
    C --> D[Start Generator Thread]
    D --> E[Start Processor Thread]
    E --> F[Generate Packets]
    F --> G{Queue Full?}
    G -->|Yes| H[Drop Packet]
    G -->|No| I[Enqueue Packet]
    I --> J[Process Packet]
    J --> K[Update Statistics]
    K --> L{All Packets Processed?}
    L -->|No| F
    L -->|Yes| M[End Simulation]
```

## Description
This flowchart shows the main steps in the simulation process, from initialization to packet processing and statistics collection. 