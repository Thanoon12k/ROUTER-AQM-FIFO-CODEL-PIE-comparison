import random
import time
class Queue:
    def __init__(self, capacity):
        self.items = []
        self.capacity = capacity

    def is_empty(self):
        return len(self.items) == 0
    
    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.pop(0)

    def size(self):
        return len(self.items)

    def print_queue(self):
        print(self.items)   
    
    def is_full(self):
        return len(self.items) == self.capacity
        
        
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


def generate_packets(sim_start_time):
    packets = []
    data_sizes = [10, 20, 30, 500, 80, 90, 110, 120, 130, 100]
    for i in range(10):
        create_time = time.time() - sim_start_time  # Calculate relative time
        packet = Packets(
            packet_id=float(i+1)/10,
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
    def __init__(self,speed): 
        self.speed = speed      
        self.node_type = "link"   # byte per second


def main():
    sim_start_time = time.time()

    queue = Queue(10)
    
    packets = generate_packets(sim_start_time)

    link = Netwrok_Link(speed=1)

    



if __name__ == "__main__":
    main()
