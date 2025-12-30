"""
Food Delivery Routing System
--------------------------------------------
SIMPLE VERSION FOR 3RD SEMESTER STUDENTS (PYTHON)
--------------------------------------------
Concepts Covered:
1. Classes/Objects: Storing data (Restaurant, Rider, Order).
2. Linked List (Manual): We build a list of Restaurants from scratch using nodes.
3. List (Python's Array): We use a standard list for Riders to easily sort them.
4. Queue (deque): First-In-First-Out (FIFO) for processing orders.
5. Stack (List): Last-In-First-Out (LIFO) for undoing actions.
6. Sorting: Organizing riders by workload using lambda functions.
"""

from collections import deque # Optimized for Queue operations
import math

# ==========================================
# 1. DATA MODELS (The "Things" in our system)
# ==========================================

class Restaurant:
    def __init__(self, id, name, rating, location):
        self.id = id
        self.name = name
        self.rating = rating
        self.location = location # 0 to 10

class Rider:
    def __init__(self, id, name, location, deliveries_done=0):
        self.id = id
        self.name = name
        self.location = location
        self.deliveries_done = deliveries_done

class Order:
    def __init__(self, order_id, restaurant_name, restaurant_loc, customer_loc):
        self.order_id = order_id
        self.restaurant_name = restaurant_name
        self.restaurant_loc = restaurant_loc
        self.customer_loc = customer_loc

# ==========================================
# 2. LINKED LIST IMPLEMENTATION (Manual)
# ==========================================
# TEACHING POINT: In Python, we use classes to represent Nodes and pointers.

class Node:
    def __init__(self, data):
        self.data = data # This will hold a Restaurant object
        self.next = None

class RestaurantLinkedList:
    def __init__(self):
        self.head = None

    # Insert a new restaurant at the end
    def add_restaurant(self, id, name, rating, loc):
        new_restaurant = Restaurant(id, name, rating, loc)
        new_node = Node(new_restaurant)

        if self.head is None:
            self.head = new_node
        else:
            temp = self.head
            while temp.next is not None:
                temp = temp.next
            temp.next = new_node

    # Display all restaurants
    def display(self):
        temp = self.head
        print("\n--- Available Restaurants (Linked List) ---")
        print(f"{'ID':<5} {'Name':<15} {'Rating':<8} {'Location'}")
        while temp is not None:
            print(f"{temp.data.id:<5} {temp.data.name:<15} {temp.data.rating:<8} {temp.data.location}")
            temp = temp.next
        print("-" * 45)

    # Find a restaurant by ID to get its details
    def find_by_id(self, id):
        temp = self.head
        while temp is not None:
            if temp.data.id == id:
                return temp.data
            temp = temp.next
        return None

# ==========================================
# 3. GLOBAL VARIABLES (Our Database)
# ==========================================

my_restaurants = RestaurantLinkedList() # Manual Linked List
my_riders = []                          # Standard Python List
order_queue = deque()                   # Queue (using deque for O(1) pop)
undo_stack = []                         # Stack (using standard list)
order_id_counter = 1

# ==========================================
# 4. HELPER FUNCTIONS
# ==========================================

# Setup some dummy data
def initialize_data():
    # Add Restaurants to Linked List
    my_restaurants.add_restaurant(101, "Burger King", 4.5, 2)
    my_restaurants.add_restaurant(102, "Pizza Hut", 4.2, 8)
    my_restaurants.add_restaurant(103, "Subway", 4.0, 5)

    # Add Riders to List
    my_riders.append(Rider(201, "Ali", 1, 0))
    my_riders.append(Rider(202, "Bilal", 6, 2)) # Bilal has already done 2 deliveries
    my_riders.append(Rider(203, "Hamza", 3, 0))

# ==========================================
# 5. MAIN FEATURES
# ==========================================

def place_order():
    global order_id_counter
    
    my_restaurants.display()
    
    try:
        rest_id = int(input("Enter Restaurant ID to order from: "))
        cust_loc = int(input("Enter Your Location (0-10): "))
    except ValueError:
        print("Invalid input! Please enter numbers.")
        return

    # Linked List Search
    r = my_restaurants.find_by_id(rest_id)
    if r is None:
        print("Invalid Restaurant ID!")
        return

    # Create Order
    new_order = Order(order_id_counter, r.name, r.location, cust_loc)
    order_id_counter += 1

    # Add to Queue
    order_queue.append(new_order)

    # Add to History (Stack)
    undo_stack.append(f"Placed Order #{new_order.order_id}")

    print(f"Success! Order #{new_order.order_id} is now in the Queue.")

def process_order():
    if not order_queue:
        print("No orders pending.")
        return

    # 1. Get the next order from Queue (FIFO)
    current_order = order_queue.popleft()

    print(f"\nProcessing Order #{current_order.order_id} from {current_order.restaurant_name}...")

    # 2. Find the best Rider (Simplest Logic: Closest Distance)
    # Distance Formula: abs(RiderLocation - RestaurantLocation)
    
    best_rider = None
    min_distance = 1000 # Start with a high number

    for rider in my_riders:
        dist = abs(rider.location - current_order.restaurant_loc)
        if dist < min_distance:
            min_distance = dist
            best_rider = rider

    if best_rider:
        # Calculate total delivery distance
        dist_to_cust = abs(current_order.restaurant_loc - current_order.customer_loc)
        total_dist = min_distance + dist_to_cust

        # Update Rider Stats
        best_rider.deliveries_done += 1
        best_rider.location = current_order.customer_loc # Rider moves to customer

        print(f">>> Assigned to Rider: {best_rider.name}")
        print(f">>> Time to Restaurant: {min_distance} mins")
        print(f">>> Time to Customer:   {dist_to_cust} mins")
        print(f">>> Total Time:         {total_dist} mins")
        
        undo_stack.append(f"Processed Order #{current_order.order_id}")
    else:
        print("No riders found!")

def show_riders_sorted():
    # TEACHING POINT: Sorting a list is easy with a lambda key
    # Sorts in-place based on deliveries_done
    my_riders.sort(key=lambda x: x.deliveries_done)

    print("\n--- Riders (Sorted by Workload) ---")
    print(f"{'Name':<10} {'Location':<10} {'Deliveries Done'}")
    for r in my_riders:
        print(f"{r.name:<10} {r.location:<10} {r.deliveries_done}")

def undo_last_action():
    if not undo_stack:
        print("Nothing to undo.")
        return

    last_action = undo_stack.pop()
    print(f"Undoing action: {last_action}")
    print("(Note: In this simple version, we just remove the log from history)")

# ==========================================
# 6. MAIN FUNCTION
# ==========================================

def main():
    initialize_data()
    
    while True:
        print("\n=== FOOD DELIVERY SYSTEM (PYTHON) ===")
        print("1. Place New Order")
        print("2. Process Next Order (Queue)")
        print("3. View Riders (Sorted)")
        print("4. Undo Last Action (Stack)")
        print("5. Exit")
        
        choice = input("Choice: ")

        if choice == '1':
            place_order()
        elif choice == '2':
            process_order()
        elif choice == '3':
            show_riders_sorted()
        elif choice == '4':
            undo_last_action()
        elif choice == '5':
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()