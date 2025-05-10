# FIFO Algorithm

[Back to Project Overview](project.md)

## FIFO Class Diagram

```mermaid
classDiagram
    class FIFOQueue {
        +capacity: int
        +packets: List[Packet]
        +enqueue(packet)
        +dequeue()
        +process_packet(packet)
    }
    class Packet {
        +packet_id: int
        +data_length: int
        +creation_time: float
    }
    FIFOQueue --> Packet
```

## Description
FIFO (First-In-First-Out) is a simple queue management algorithm where packets are processed in the order they arrive. If the queue is full, new packets are dropped (tail-drop). 