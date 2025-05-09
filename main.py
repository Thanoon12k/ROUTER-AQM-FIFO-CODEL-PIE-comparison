import random
import time
class Queue:
    def __init__(self, capacity):
        self.items = []
        self.capacity = capacity
        self.processing_speed = 1000  # bytes per second
        self.current_time = 0

    def is_empty(self):
        return len(self.items) == 0
    
    def enqueue(self, item):
        if not self.is_full():
            self.items.append(item)
            return True
        return False

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def size(self):
        return len(self.items)

    def print_queue(self):
        print("Current queue state:")
        for packet in self.items:
            print(f"Packet {packet.packet_id} (size: {packet.data_size} bytes)   packet timings: {packet.creation_time} {packet.arrival_time} {packet.start_processing_time} {packet.completion_time}")
    
    def is_full(self):
        return len(self.items) == self.capacity

    def process_packets(self,sim_start_time):
        current_time = time.time() - sim_start_time
        current_packet = self.items[0]
        time_to_process = current_packet.data_size / self.processing_speed
        current_packet.start_processing_time = current_time
        print(f" start Processing packet {current_packet.packet_id} at time {current_time:.2f}s")
        time.sleep(time_to_process)
        
        # Get actual time after processing
        current_packet.completion_time = time.time() - sim_start_time
        print(f" completed Processing packet {current_packet.packet_id} at time {current_packet.completion_time:.2f}s")

        # Remove and return the processed packet
        return self.dequeue()

class Packets:
    def __init__(self, packet_id,data_size, creation_time,arrival_time, start_processing_time,completion_time,delete_time):
        self.packet_id = packet_id
        self.data_size = data_size   #byte
        self.creation_time = creation_time
        self.arrival_time = arrival_time
        self.start_processing_time = start_processing_time
        self.completion_time = completion_time
        self.delete_time = delete_time

    def __str__(self):
        return f"Packet {self.packet_id} - Arrival Time: {self.arrival_time}, Processing Time: {self.start_processing_time}"


def generate_packets(num_packets,sim_start_time):
    packets = []
    data_sizes = [10, 20, 30, 500, 80, 90, 110, 120, 130, 100]
    for i in range(num_packets):
        create_time = time.time() - sim_start_time  # Calculate relative time
        packet = Packets(
            packet_id=i,
            data_size=data_sizes[i],
            creation_time=create_time,
            arrival_time=0,
            start_processing_time=0,
            completion_time=0,
            delete_time=0
        )
        packets.append(packet)
        print(f"Packet {packet.packet_id} created at time {create_time:.2f} s")
        time.sleep(1)  # Wait 1 second between packet creation
    return packets

class Netwrok_Link:
    def __init__(self, speed): 
        self.speed = speed      # bytes per second
        self.node_type = "link"
        self.latency = 0.1      # 100ms latency
        self.current_time = 0

    def transmit_packet(self, packet,sim_start_time):
        # Add latency to the packet
        current_time = time.time() - sim_start_time
        transmission_time = (packet.data_size / self.speed) + self.latency
        time.sleep(transmission_time)
        packet.arrival_time = time.time() - sim_start_time
        return transmission_time

def main():
    sim_start_time = time.time()
    queue = Queue(10)
    packets = generate_packets(1,sim_start_time)
    link = Netwrok_Link(speed=1000)  # 1000 bytes per second

    # Sort packets by creation time
    packets.sort(key=lambda x: x.creation_time)
    
    print("\nProcessing packets:")
    print("------------------")
    
    for packet in packets:
        # Transmit packet through the link
        transmission_time = link.transmit_packet(packet,sim_start_time)
        print(f"Packet {packet.packet_id} transmitted through link:")
        print(f"  - Transmission time: {transmission_time:.2f}s")
        print(f"  - Arrival time at queue: {packet.arrival_time:.2f}s")
        
        # Enqueue packet
        if queue.enqueue(packet):
            print(f"  - Successfully enqueued")
        else:
            print(f"  - Queue is full! Packet dropped")
        
        # Process packets in queue
        while not queue.is_empty():
            processed_packet = queue.process_packets(sim_start_time)
            if processed_packet:
                print(f"\nProcessed Packet {processed_packet.packet_id}:")
                print(f"  - Size: {processed_packet.data_size} bytes")
                print(f"  - Start processing: {processed_packet.start_processing_time:.2f}s")
                print(f"  - Completion time: {processed_packet.completion_time:.2f}s")
        print("------------------")

if __name__ == "__main__":
    main()
