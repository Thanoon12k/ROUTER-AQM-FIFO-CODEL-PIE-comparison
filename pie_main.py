import random
import time
import sys
import threading
import csv
import matplotlib.pyplot as plt
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List, Dict
from queue import Queue as ThreadQueue
from abc import ABC, abstractmethod

@dataclass
class Packet:
    """Represents a network packet with all its properties."""
    packet_id: int
    data_length: int
    creation_time: float
    arrival_time: float = 0
    start_processing_time: float = 0
    completion_time: float = 0
    delete_time: float = 0
    drop_probability: float = 0  # PIE drop probability

    def __str__(self) -> str:
        return f"Packet {self.packet_id} (size: {self.data_length} bytes)"

class EventLogger:
    """Handles logging of simulation events with thread-safe operations."""
    
    def __init__(self, start_time: float):
        self.lock = threading.Lock()
        self.start_time = start_time
        self.events_file = "pie_events.txt"
        self._initialize_log_file()

    def _initialize_log_file(self) -> None:
        """Initialize the log file with a header."""
        with open(self.events_file, 'w') as f:
            f.write("=== PIE Network Simulation Events ===\n\n")

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
            transmission_time = (packet.data_length / self.speed) + self.latency
            time.sleep(transmission_time)
            packet.arrival_time = time.time() - sim_start_time
            return transmission_time

class PIEQueue:
    """Thread-safe queue implementing PIE (Proportional Integral controller Enhanced) algorithm."""
    
    def __init__(self, capacity: int, processing_speed: int = 200000):
        self.items: List[Packet] = []
        self.capacity = capacity
        self.processing_speed = processing_speed  # bytes per second
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        
        # PIE parameters (tuned)
        self.drop_probability = 0.0
        self.alpha = 0.01   # Proportional gain (less aggressive)
        self.beta = 0.05    # Integral gain (less aggressive)
        self.target_delay = 0.05  # Target delay in seconds (50ms)
        self.current_delay = 0.0
        self.last_update_time = 0.0
        self.accumulated_error = 0.0  # For integral control
        self.update_interval = 0.01  # Update PIE every 10ms
        
        # Queue statistics
        self.stats = {
            'total_packets': 0,
            'total_processed': 0,
            'total_dropped': 0,
            'total_processing_time': 0,
            'total_transmission_time': 0,
            'queue_delays': [],  # Track queue delays for PIE
            'last_queue_size': 0,
            'last_drop_probability': 0.0
        }

    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        return len(self.items) == 0

    def is_full(self) -> bool:
        """Check if the queue is full."""
        return len(self.items) == self.capacity

    def update_pie_parameters(self, current_time: float) -> None:
        """Update PIE parameters based on current queue state."""
        if self.last_update_time == 0:
            self.last_update_time = current_time
            return

        time_diff = current_time - self.last_update_time
        if time_diff < self.update_interval:
            return

        # Calculate current queue delay
        if not self.is_empty() and self.items[0] is not None:
            self.current_delay = (current_time - self.items[0].arrival_time)
        else:
            self.current_delay = 0.0

        # Calculate queue size change
        queue_size_change = len(self.items) - self.stats['last_queue_size']
        self.stats['last_queue_size'] = len(self.items)

        # Calculate error based on both delay and queue size (scaled queue error)
        delay_error = self.current_delay - self.target_delay
        queue_error = queue_size_change / self.capacity
        error = delay_error + 0.1 * queue_error  # Scale down queue error

        # Update accumulated error for integral control
        self.accumulated_error += error * time_diff
        
        # Update drop probability with both proportional and integral terms
        self.drop_probability += (self.alpha * error + self.beta * self.accumulated_error)
        
        # Ensure drop probability is between 0 and 1
        self.drop_probability = max(0.0, min(1.0, self.drop_probability))
        
        # Reset drop probability and accumulated error if queue is empty or drop_probability is too high
        if self.is_empty() or self.drop_probability > 0.95:
            self.drop_probability = 0.0
            self.accumulated_error = 0.0
        
        # Store last drop probability for statistics
        self.stats['last_drop_probability'] = self.drop_probability
        
        self.last_update_time = current_time

    def enqueue(self, packet: Optional[Packet]) -> bool:
        """Add a packet to the queue using PIE algorithm."""
        with self.lock:
            if packet is None:
                self.items.append(packet)
                self.condition.notify()
                return True

            current_time = time.time()
            self.update_pie_parameters(current_time)
            
            # Apply PIE drop decision based on queue state
            if len(self.items) > self.capacity * 0.5:  # Start PIE when queue is 50% full
                # Calculate dynamic drop threshold based on queue size
                drop_threshold = self.drop_probability * (len(self.items) / self.capacity)
                
                if random.random() < drop_threshold:
                    self.stats['total_dropped'] += 1
                    return False

            if not self.is_full():
                packet.drop_probability = self.drop_probability
                self.items.append(packet)
                self.condition.notify()
                return True
            
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
        time_to_process = current_packet.data_length / self.processing_speed

        current_packet.start_processing_time = current_time
        time.sleep(time_to_process)

        current_packet.completion_time = time.time() - sim_start_time
        self.stats['total_processing_time'] += time_to_process
        self.stats['total_processed'] += 1
        
        # Record queue delay for statistics
        if current_packet.arrival_time > 0:
            queue_delay = current_packet.start_processing_time - current_packet.arrival_time
            self.stats['queue_delays'].append(queue_delay)

        return self.dequeue(), ""

class StatisticsCollector:
    """Collects and plots simulation statistics over time."""
    
    def __init__(self):
        self.timestamps = []
        self.throughput = []
        self.queue_size = []
        self.processing_times = []
        self.drop_probabilities = []
        self.queue_delays = []
        self.lock = threading.Lock()

    def record_statistics(self, current_time: float, queue: 'PIEQueue') -> None:
        """Record statistics at the current time."""
        with self.lock:
            self.timestamps.append(current_time)
            if len(self.timestamps) > 1:
                throughput = queue.stats['total_processed'] / current_time if current_time > 0 else 0
            else:
                throughput = 0
            self.throughput.append(throughput)
            self.queue_size.append(len(queue.items))
            self.processing_times.append(queue.stats['total_processing_time'])
            self.drop_probabilities.append(queue.drop_probability)
            if queue.stats['queue_delays']:
                self.queue_delays.append(queue.stats['queue_delays'][-1])
            else:
                self.queue_delays.append(0)

    def plot_statistics(self) -> None:
        """Plot the collected statistics."""
        plt.figure(figsize=(10, 20))  # Adjusted figure size for vertical layout
        
        # Plot 1: Throughput over time
        plt.subplot(4, 1, 1)
        plt.plot(self.timestamps, self.throughput, 'b-', label='Throughput (packets/s)')
        plt.xlabel('Simulation Time (s)', fontsize=6)
        plt.ylabel('Throughput', fontsize=6)
        plt.grid(True)
        plt.legend()

        # Plot 2: Queue Size over time
        plt.subplot(4, 1, 2)
        plt.plot(self.timestamps, self.queue_size, 'r-', label='Queue Size (packets)')
        plt.xlabel('Simulation Time (s)', fontsize=6)
        plt.ylabel('Queue Size', fontsize=6)
        plt.grid(True)
        plt.legend()

        # Plot 3: Drop Probability over time
        plt.subplot(4, 1, 3)
        plt.plot(self.timestamps, self.drop_probabilities, 'g-', label='Drop Probability')
        plt.xlabel('Simulation Time (s)', fontsize=6)
        plt.ylabel('Drop Probability', fontsize=6)
        plt.grid(True)
        plt.legend()

        # Plot 4: Queue Delay over time
        plt.subplot(4, 1, 4)
        plt.plot(self.timestamps, self.queue_delays, 'm-', label='Queue Delay (s)')
        plt.xlabel('Simulation Time (s)', fontsize=6)
        plt.ylabel('Queue Delay', fontsize=6)
        plt.grid(True)
        plt.legend()

        plt.tight_layout(h_pad=6)
        plt.show()

class Simulation:
    """Main simulation class that coordinates the entire process."""
    
    def __init__(self, queue_capacity: int, network_speed: int, generation_speed: float = 0.05, csv_file: str = "packets.csv"):
        self.sim_start_time = time.time()
        self.event_logger = EventLogger(self.sim_start_time)
        self.packet_queue = PIEQueue(queue_capacity)
        self.network_link = NetworkLink(network_speed)
        self.generation_speed = generation_speed  # Time between packet generation in seconds
        self.csv_file = csv_file
        self.packets_data = self._load_packets_from_csv()
        self.stats_collector = StatisticsCollector()
        self.stats_interval = 0.1
        self.simulation_complete = threading.Event()

    def _load_packets_from_csv(self) -> List[Dict[str, int]]:
        """Load packet data from CSV file."""
        try:
            with open(self.csv_file, 'r') as f:
                reader = csv.DictReader(f)
                return [{'packet_id': int(row['packet_id']), 
                        'data_length': int(row['data_length'])} 
                        for row in reader]
        except FileNotFoundError:
            self.event_logger.log_event(f"Error: CSV file '{self.csv_file}' not found")
            sys.exit(1)
        except Exception as e:
            self.event_logger.log_event(f"Error reading CSV file: {str(e)}")
            sys.exit(1)

    def _collect_statistics(self) -> None:
        """Collect statistics periodically during simulation."""
        while not self.simulation_complete.is_set():
            current_time = time.time() - self.sim_start_time
            self.stats_collector.record_statistics(current_time, self.packet_queue)
            time.sleep(self.stats_interval)

    def generate_packets(self) -> None:
        """Generate packets with specified intervals."""
        self.event_logger.log_event("=== Starting Packet Generation ===")
        self.packet_queue.stats['total_packets'] = len(self.packets_data)

        for packet_data in self.packets_data:
            packet = Packet(
                packet_id=packet_data['packet_id'],
                data_length=packet_data['data_length'],
                creation_time=time.time() - self.sim_start_time
            )
            self.event_logger.log_event(f"Generated {packet}")
            
            if not self.packet_queue.enqueue(packet):
                self.event_logger.log_event(f"Packet dropped by PIE - {packet}")
            
            time.sleep(self.generation_speed)  # Use the configurable generation speed

        self.event_logger.log_event("=== Packet Generation Complete ===")
        self.packet_queue.enqueue(None)

    def process_packets(self) -> None:
        """Process packets from the queue."""
        self.event_logger.log_event("=== Starting Packet Processing ===")

        while True:
            packet = self.packet_queue.get()
            if packet is None:
                break

            transmission_time = self.network_link.transmit_packet(packet, self.sim_start_time)
            self.packet_queue.stats['total_transmission_time'] += transmission_time

            # Process the packet directly instead of re-enqueueing
            if not self.packet_queue.is_empty():
                processed_packet, _ = self.packet_queue.process_packets(self.sim_start_time)
                if processed_packet:
                    self.event_logger.log_event(f"{processed_packet} processed")
                    if self.packet_queue.stats['total_processed'] == len(self.packets_data):
                        self._print_statistics()
                        self.event_logger.log_event("=== All packets processed - Exiting ===")
                        self.simulation_complete.set()
                        return

        self._print_statistics()
        self.event_logger.log_event("=== All packets processed - Exiting ===")
        self.simulation_complete.set()

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
            f"Average Queue Delay: {self._calculate_avg_queue_delay():.2f}s",
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

    def _calculate_avg_queue_delay(self) -> float:
        """Calculate average queue delay safely."""
        delays = self.packet_queue.stats['queue_delays']
        return sum(delays) / len(delays) if delays else 0.0

    def run(self) -> None:
        """Run the simulation with proper thread management."""
        try:
            stats_thread = threading.Thread(target=self._collect_statistics, daemon=True)
            stats_thread.start()

            generator_thread = threading.Thread(target=self.generate_packets)
            processor_thread = threading.Thread(target=self.process_packets)

            generator_thread.start()
            processor_thread.start()

            generator_thread.join()
            processor_thread.join()

            self.simulation_complete.wait()
            self.stats_collector.plot_statistics()

        except KeyboardInterrupt:
            print("\nSimulation interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"\nError in simulation: {str(e)}")
            sys.exit(1)

def main():
    """Main entry point of the simulation."""
    simulation = Simulation(
        queue_capacity=500,  # Significantly increased queue capacity
        network_speed=100000,   # Increased to 100mbps
        generation_speed=0.02,  # 50ms between packets
        csv_file="dataset/video_210s480p_01.csv"
    )
    simulation.run()

if __name__ == "__main__":
    main() 

