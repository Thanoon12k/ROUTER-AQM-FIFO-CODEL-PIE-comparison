# Project Structure

[Back to Project Overview](project.md)

## Class Hierarchy Diagram

```mermaid
classDiagram
    class Simulation {
        +queue_capacity: int
        +network_speed: float
        +generation_speed: float
        +csv_file: str
        +run()
    }
    class EventLogger {
        +log_event(event_type, data)
    }
    class PacketQueue {
        <<abstract>>
        +process_packet(packet)*
    }
    class FIFOQueue {
        +capacity: int
        +packets: List[Packet]
        +process_packet(packet)
    }
    class PIEQueue {
        +target_delay: float
        +current_delay: float
        +drop_probability: float
        +alpha: float
        +beta: float
        +update_drop_probability()
        +process_packet(packet)
    }
    class NetworkLink {
        +bandwidth: float
        +latency: float
        +transmit(packet)
    }
    class StatisticsCollector {
        +metrics: Dict
        +collect_metrics(queue)
        +plot_statistics()
    }

    Simulation *-- EventLogger
    Simulation *-- PacketQueue
    Simulation *-- NetworkLink
    Simulation *-- StatisticsCollector
    PacketQueue <|-- FIFOQueue
    PacketQueue <|-- PIEQueue
    StatisticsCollector o-- PacketQueue
```

## Description
This diagram shows the main classes and their relationships in the project. Use the links above to explore specific components. 