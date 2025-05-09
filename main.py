import random
import time
import sys
import threading
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List, Dict
from queue import Queue as ThreadQueue
from abc import ABC, abstractmethod

@dataclass
class Packet:
    """Represents a network packet with all its properties."""
    packet_id: int
    data_size: int
    creation_time: float
    arrival_time: float = 0
    start_processing_time: float = 0
    completion_time: float = 0
    delete_time: float = 0

    def __str__(self) -> str:
        return f"Packet {self.packet_id} (size: {self.data_size} bytes)"

class EventLogger:
    """Handles logging of simulation events with thread-safe operations."""
    
    def __init__(self, start_time: float):
        self.lock = threading.Lock()
        self.start_time = start_time
        self.events_file = "events.txt"
        self._initialize_log_file()

    def _initialize_log_file(self) -> None:
        """Initialize the log file with a header."""
        with open(self.events_file, 'w') as f:
            f.write("=== Network Simulation Events ===\n\n")

    def _get_elapsed_time(self) -> str:
        """Calculate and format elapsed time since simulation start."""
        elapsed_time = time.time() - self.start_time
        minutes = int(elapsed_time // 60)
        seconds = elapsed_time % 60
        return f"{minutes:02d}:{seconds:06.3f}"

    def log_event(self, event: str) -> None:
        """Log an event with timestamp to both console and file."""
        with self.lock:
            timestamp = self._get_elapsed_time()
            log_message = f"{timestamp} - {event}"
            print(log_message)
            with open(self.events_file, 'a') as f:
                f.write(f"{log_message}\n")

class NetworkLink:
    """Represents a network link with transmission capabilities."""
    
    def __init__(self, speed: int, latency: float = 0.1):
        self.speed = speed  # bytes per second
        self.latency = latency  # seconds
        self.lock = threading.Lock()

    def transmit_packet(self, packet: Packet, sim_start_time: float) -> float:
        """Transmit a packet through the network link."""
        with self.lock:
            transmission_time = (packet.data_size / self.speed) + self.latency
            time.sleep(transmission_time)
            packet.arrival_time = time.time() - sim_start_time
            return transmission_time

class PacketQueue:
    """Thread-safe queue for managing network packets."""
    
    def __init__(self, capacity: int, processing_speed: int = 1000):
        self.items: List[Packet] = []
        self.capacity = capacity
        self.processing_speed = processing_speed  # bytes per second
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        self.stats = {
            'total_packets': 0,
            'total_processed': 0,
            'total_dropped': 0,
            'total_processing_time': 0,
            'total_transmission_time': 0
        }

    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        return len(self.items) == 0

    def is_full(self) -> bool:
        """Check if the queue is full."""
        return len(self.items) == self.capacity

    def enqueue(self, packet: Optional[Packet]) -> bool:
        """Add a packet to the queue if there's space."""
        with self.lock:
            if packet is None or not self.is_full():
                self.items.append(packet)
                self.condition.notify()
                return True
            if packet is not None:
                self.stats['total_dropped'] += 1
            return False

    def dequeue(self) -> Optional[Packet]:
        """Remove and return the first packet from the queue."""
        with self.lock:
            return self.items.pop(0) if not self.is_empty() else None

    def get(self) -> Optional[Packet]:
        """Get the next packet, waiting if the queue is empty."""
        with self.lock:
            while self.is_empty():
                self.condition.wait()
            return self.items.pop(0)

    def process_packets(self, sim_start_time: float) -> tuple[Optional[Packet], str]:
        """Process the next packet in the queue."""
        if self.is_empty():
            return None, ""

        current_packet = self.items[0]
        if current_packet is None:
            return self.dequeue(), ""

        current_time = time.time() - sim_start_time
        time_to_process = current_packet.data_size / self.processing_speed

        current_packet.start_processing_time = current_time
        time.sleep(time_to_process)

        current_packet.completion_time = time.time() - sim_start_time
        self.stats['total_processing_time'] += time_to_process
        self.stats['total_processed'] += 1

        return self.dequeue(), ""

class Simulation:
    """Main simulation class that coordinates the entire process."""
    
    def __init__(self, num_packets: int, queue_capacity: int, network_speed: int):
        self.sim_start_time = time.time()
        self.event_logger = EventLogger(self.sim_start_time)
        self.packet_queue = PacketQueue(queue_capacity)
        self.network_link = NetworkLink(network_speed)
        self.num_packets = num_packets
        self.data_sizes = [10, 20, 30, 500, 80, 90, 110, 120, 130, 100]

    def generate_packets(self) -> None:
        """Generate packets with specified intervals."""
        self.event_logger.log_event("=== Starting Packet Generation ===")
        self.packet_queue.stats['total_packets'] = self.num_packets

        for i in range(self.num_packets):
            packet = Packet(
                packet_id=i,
                data_size=self.data_sizes[i],
                creation_time=time.time() - self.sim_start_time
            )
            self.event_logger.log_event(f"Generated {packet}")
            
            if not self.packet_queue.enqueue(packet):
                self.event_logger.log_event(f"Queue full - {packet} dropped")
            
            time.sleep(0.1)  # Simulate time between packet generation

        self.event_logger.log_event("=== Packet Generation Complete ===")
        self.packet_queue.enqueue(None)  # Signal end of processing

    def process_packets(self) -> None:
        """Process packets from the queue."""
        self.event_logger.log_event("=== Starting Packet Processing ===")

        while True:
            packet = self.packet_queue.get()
            if packet is None:
                break

            transmission_time = self.network_link.transmit_packet(packet, self.sim_start_time)
            self.packet_queue.stats['total_transmission_time'] += transmission_time

            if self.packet_queue.enqueue(packet):
                self.event_logger.log_event(f"{packet} enqueued for processing")
            else:
                self.event_logger.log_event(f"Queue full - {packet} dropped")

            if not self.packet_queue.is_empty():
                processed_packet, _ = self.packet_queue.process_packets(self.sim_start_time)
                if processed_packet:
                    self.event_logger.log_event(f"{processed_packet} dequeued")
                    if self.packet_queue.stats['total_processed'] == self.num_packets:
                        self._print_statistics()
                        self.event_logger.log_event("=== All packets processed - Exiting ===")
                        sys.exit(0)

        self._print_statistics()
        self.event_logger.log_event("=== All packets processed - Exiting ===")
        sys.exit(0)

    def _print_statistics(self) -> None:
        """Print simulation statistics."""
        total_time = time.time() - self.sim_start_time
        stats = [
            "\n=== Simulation Statistics ===",
            f"Total Simulation Time: {total_time:.2f}s",
            f"Total Packets Generated: {self.packet_queue.stats['total_packets']}",
            f"Total Packets Processed: {self.packet_queue.stats['total_processed']}",
            f"Total Packets Dropped: {self.packet_queue.stats['total_dropped']}",
            f"Average Processing Time: {self._calculate_avg_processing_time():.2f}s",
            f"Queue Capacity: {self.packet_queue.capacity}",
            "===========================\n"
        ]
        self.event_logger.log_event("\n".join(stats))

    def _calculate_avg_processing_time(self) -> float:
        """Calculate average processing time safely."""
        if self.packet_queue.stats['total_processed'] > 0:
            return (self.packet_queue.stats['total_processing_time'] / 
                   self.packet_queue.stats['total_processed'])
        return 0.0

    def run(self) -> None:
        """Run the simulation with proper thread management."""
        try:
            generator_thread = threading.Thread(target=self.generate_packets)
            processor_thread = threading.Thread(target=self.process_packets)

            generator_thread.start()
            processor_thread.start()

            generator_thread.join()
            processor_thread.join()

        except KeyboardInterrupt:
            print("\nSimulation interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"\nError in simulation: {str(e)}")
            sys.exit(1)

def main():
    """Main entry point of the simulation."""
    simulation = Simulation(
        num_packets=10,
        queue_capacity=1,
        network_speed=1000
    )
    simulation.run()

if __name__ == "__main__":
    main()
