# Network Queue Management Simulation - Visual Documentation

## System Architecture

```mermaid
graph TB
    subgraph "Network Simulation"
        A[Simulation Controller] --> B[Packet Generator]
        A --> C[Queue Manager]
        A --> D[Network Link]
        A --> E[Statistics Collector]
        
        B --> C
        C --> D
        D --> F[Output]
        
        C --> G[FIFO Queue]
        C --> H[PIE Queue]
        
        E --> I[Performance Metrics]
        E --> J[Visualization]
    end
```

## Packet Lifecycle

```mermaid
sequenceDiagram
    participant G as Generator
    participant Q as Queue
    participant N as Network
    participant S as Statistics

    G->>Q: Generate Packet
    Q->>Q: Check Queue Status
    alt Queue Full
        Q->>S: Record Drop
    else Queue Available
        Q->>Q: Enqueue Packet
        Q->>N: Process Packet
        N->>S: Update Statistics
    end
```

## FIFO vs PIE Comparison

```mermaid
graph LR
    subgraph "FIFO Algorithm"
        A[Packet Arrival] --> B[Check Queue]
        B -->|Full| C[Drop Packet]
        B -->|Space| D[Enqueue]
        D --> E[Process in Order]
    end

    subgraph "PIE Algorithm"
        F[Packet Arrival] --> G[Calculate Delay]
        G --> H[Update Probability]
        H --> I{Queue > 50%?}
        I -->|Yes| J[Apply PIE Logic]
        I -->|No| K[Direct Enqueue]
        J --> L[Drop/Enqueue Decision]
    end
```

## Performance Metrics Visualization

```mermaid
graph TD
    subgraph "Key Metrics"
        A[Throughput] --> B[Packets/Second]
        C[Queue Size] --> D[Buffer Utilization]
        E[Drop Rate] --> F[Packet Loss]
        G[Delay] --> H[Latency]
    end
```

## Queue State Transitions

```mermaid
stateDiagram-v2
    [*] --> Empty
    Empty --> Filling: Packet Arrival
    Filling --> Full: Queue Capacity Reached
    Full --> Dropping: New Arrivals
    Dropping --> Filling: Space Available
    Filling --> Empty: All Packets Processed
    Empty --> [*]
```

## PIE Control Loop

```mermaid
graph TD
    A[Measure Current Delay] --> B[Calculate Error]
    B --> C[Update Drop Probability]
    C --> D[Apply Drop Decision]
    D --> E[Update Queue State]
    E --> A
```

## ASCII Art: Network Node

```
    +------------------+
    |   Network Node   |
    +------------------+
           |
    +------+------+
    |    Queue    |
    +------+------+
           |
    +------+------+
    |   Network   |
    +------+------+
```

## ASCII Art: Packet Flow

```
    Generator --> [Queue] --> Processor
       |            |           |
       v            v           v
    [Create]    [Buffer]    [Process]
       |            |           |
       +------------+-----------+
                    |
                    v
                [Network]
```

## Performance Comparison Chart

```mermaid
graph TD
    subgraph "FIFO Performance"
        A[Queue Size] --> B[Linear Growth]
        C[Drop Rate] --> D[Sudden Increase]
    end

    subgraph "PIE Performance"
        E[Queue Size] --> F[Controlled Growth]
        G[Drop Rate] --> H[Gradual Increase]
    end
```

## Implementation Flow

```mermaid
graph TD
    A[Start] --> B[Initialize Components]
    B --> C[Load Configuration]
    C --> D[Start Threads]
    D --> E[Generate Packets]
    E --> F[Process Queue]
    F --> G[Update Statistics]
    G --> H[Visualize Results]
    H --> I[End]
```

## Class Relationships

```mermaid
classDiagram
    class Simulation {
        +run()
        +generate_packets()
        +process_packets()
    }
    class Packet {
        +packet_id
        +data_length
        +creation_time
    }
    class Queue {
        +enqueue()
        +dequeue()
        +process()
    }
    class Statistics {
        +collect()
        +plot()
    }
    Simulation --> Packet
    Simulation --> Queue
    Simulation --> Statistics
```

## Network Topology

```mermaid
graph TB
    subgraph "Network Components"
        A[Source] --> B[Router]
        B --> C[Destination]
        B --> D[Queue Manager]
        D --> E[FIFO/PIE]
    end
```

## Performance Metrics Dashboard

```mermaid
graph TD
    subgraph "Real-time Metrics"
        A[Throughput] --> B[Current Rate]
        C[Queue Size] --> D[Buffer Status]
        E[Drop Rate] --> F[Loss Statistics]
        G[Delay] --> H[Latency Metrics]
    end
```

## Configuration Parameters

```mermaid
graph LR
    A[Queue Capacity] --> B[500 packets]
    C[Network Speed] --> D[100 Mbps]
    E[Generation Rate] --> F[50 ms]
    G[Processing Speed] --> H[200 Mbps]
```

## Error Handling Flow

```mermaid
graph TD
    A[Error Detection] --> B{Error Type}
    B -->|Queue Full| C[Drop Packet]
    B -->|Network Error| D[Retry]
    B -->|Processing Error| E[Skip Packet]
    C --> F[Update Stats]
    D --> F
    E --> F
```

## Thread Management

```mermaid
graph TD
    A[Main Thread] --> B[Generator Thread]
    A --> C[Processor Thread]
    A --> D[Statistics Thread]
    B --> E[Queue]
    C --> E
    D --> F[Metrics]
```

These diagrams provide a comprehensive visual representation of:
1. System architecture
2. Algorithm flows
3. Performance metrics
4. Implementation details
5. Network topology
6. Thread management
7. Error handling
8. Configuration parameters

The diagrams use Mermaid syntax which can be rendered by many Markdown viewers and documentation systems. They provide both high-level overview and detailed implementation views of the system.

Would you like me to:
1. Add more specific diagrams for any component?
2. Create additional performance visualization charts?
3. Add more detailed flow diagrams?
4. Include more ASCII art representations?

Let me know what aspects you'd like me to enhance or clarify further. 