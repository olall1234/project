import tkinter as tk
# from tkinter import messagebox


class Store:
    def __init__(self, store_id, name, rent_value, is_rented):
        self.store_id = store_id
        self.name = name
        self.rent_value = rent_value
        self.is_rented = is_rented

class Warehouse:
    def __init__(self, warehouse_id, is_available):
        self.warehouse_id = warehouse_id
        self.is_available = is_available

class Mall:
    def __init__(self, total_stores, total_warehouses, expenses):
        self.total_stores = total_stores
        self.total_warehouses = total_warehouses
        self.expenses = expenses
        self.stores = [Store(i, f"Store {i}", 1000 + i * 200, False) for i in range(1, total_stores + 1)]
        self.warehouses = [Warehouse(i, True) for i in range(1, total_warehouses + 1)]
        self.rented_stores = []
        self.profit = 0
        self.lost_and_found = {}
        self.empty_stores = [store.store_id for store in self.stores if not store.is_rented]

    def calculate_profit(self, daily_income):
        self.profit += daily_income

    def rent_store(self, store_id):
        for store in self.stores:
            if store.store_id == store_id:
                if not store.is_rented:
                    store.is_rented = True
                    self.rented_stores.append(store_id)
                    self.empty_stores.remove(store_id)
                    return True
                else:
                   # print(f"Store {store_id} is already rented.")
                    return False
        return False

    def return_store(self, store_id):
        for store in self.stores:
            if store.store_id == store_id:
                if store.is_rented:
                    store.is_rented = False
                    self.rented_stores.remove(store_id)
                    self.empty_stores.append(store_id)
                    return True
                else:
                    print(f"Store {store_id} is not currently rented.")
                    return False
        return False

    def add_to_lost_and_found(self, item, location):
        location = location.lower()

        valid_locations = [store.name.lower() for store in self.stores] + [f'warehouse {warehouse.warehouse_id}'.lower() for warehouse in self.warehouses]

        if location in valid_locations:
            location = next((store.name for store in self.stores if store.name.lower() == location), location)
            location = next((f'Warehouse {warehouse.warehouse_id}' for warehouse in self.warehouses if f'warehouse {warehouse.warehouse_id}'.lower() == location), location)

            if location not in self.lost_and_found:
                self.lost_and_found[location] = []

            self.lost_and_found[location].append(item)
            return True
        else:
            print(f"Invalid location '{location}' for lost and found.")
            return False

    def monthly_summary(self):
        net_earnings = self.profit - self.expenses
        return {
            "total_stores": self.total_stores,
            "empty_stores": self.empty_stores,
            "rented_stores": self.rented_stores,
            "available_warehouses":[warehouse.warehouse_id for warehouse in self.warehouses if warehouse.is_available],
            "profits": self.profit,
            "expenses": self.expenses,
            "net_earnings": net_earnings
        }

    def view_lost_and_found(self):
        return self.lost_and_found

    def view_available_stores(self):
        return [store for store in self.stores if not store.is_rented]

    def view_available_warehouses(self):
        return [warehouse for warehouse in self.warehouses if warehouse.is_available]

    def save_to_file(self, f):
        daily_income = 6000  # Adjust this value as needed
        self.calculate_profit(daily_income)
        self.rented_stores = [store.store_id for store in self.stores if store.is_rented]
        self.rent_store(5)
        self.rent_store(8)
        self.rent_store(2)
        with open(f, 'w') as file:
             file.write("Monthly Summary:\n")
             summary = self.monthly_summary()
             file.write(f"Total Stores: {summary['total_stores']}\n")
             file.write(f"Empty Stores: {', '.join(map(str, summary['empty_stores']))}\n")
             file.write(f"Rented Stores: {', '.join(map(str, self.rented_stores))}\n")  # Use the updated rented_stores list
             file.write(f"Available Warehouses: {', '.join(map(str, summary['available_warehouses']))}\n")
             file.write(f"Profits: {summary['profits']}\n")
             file.write(f"Expenses: {summary['expenses']}\n")
             file.write(f"Net Earnings: {summary['net_earnings']}\n")
             print(f"Data has been saved to {f}")


    def prompt_rent_store(self):
        while True:
            store_id_input = input("Enter the ID of the store you want to rent (0 to quit): ")

            try:
                store_id = int(store_id_input)
            except ValueError:
                print("Invalid input. Please enter a valid store ID.")
                continue

            if store_id == 0:
                break
            elif store_id not in self.empty_stores:
                print(f"Store {store_id} is not available for rent.")
            else:
                success = self.rent_store(store_id)
                if success:
                    print(f"Store {store_id} has been rented.")
                else:
                    print(f"Failed to rent Store {store_id}. It may already be rented.")

# Create the Mall object and perform operations
mall = Mall(total_stores=10, total_warehouses=10, expenses=5000)

f = "mall_data.txt"
mall.save_to_file(f)

mall.calculate_profit(6000)
mall.rent_store(2)
mall.rent_store(5)
mall.rent_store(8)

mall.add_to_lost_and_found("Lost key", "Store 2")
mall.add_to_lost_and_found("Lost wallet", "Warehouse 3")
mall.add_to_lost_and_found("Lost phone", "Store 5")

print("This is the original monthly summary:")
print(mall.monthly_summary())
def view_mall_information(mall):
    def show_lost_and_found():
        lost_and_found = mall.view_lost_and_found()
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Lost and Found Items and their locations:\n")
        for location, items in lost_and_found.items():
            result_text.insert(tk.END, f"Location: {location}\n")
            for item in items:
                result_text.insert(tk.END, f" - {item}\n")

    def show_available_stores():
        available_stores = mall.view_available_stores()
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Available Stores:\n")
        for store in available_stores:
            result_text.insert(tk.END, f"Store ID: {store.store_id}, Name: {store.name}, Rent Value: {store.rent_value}\n")

    def show_available_warehouses():
        available_warehouses = mall.view_available_warehouses()
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Available Warehouses:\n")
        for warehouse in available_warehouses:
            result_text.insert(tk.END, f"Warehouse ID: {warehouse.warehouse_id}\n")

    def exit_program():
        root.destroy()

    root = tk.Tk()
    #  root.title("Mall Information Viewer")

    label = tk.Label(root, text="Choose what you want to view:")
    label.pack()

    lost_and_found_button = tk.Button(root, text="Lost and Found Items", command=show_lost_and_found)
    available_stores_button = tk.Button(root, text="Available Stores", command=show_available_stores)
    available_warehouses_button = tk.Button(root, text="Available Warehouses", command=show_available_warehouses)
    exit_button = tk.Button(root, text="Exit", command=exit_program)


    available_stores_button.pack()
    available_warehouses_button.pack()
    lost_and_found_button.pack()
    exit_button.pack()

    result_text = tk.Text(root, height=10, width=40)
    result_text.pack()

    root.mainloop()


view_mall_information(mall)



# Prompt the user to rent a store
mall.prompt_rent_store()

# Print the updated monthly summary
print("This is the updated monthly summary:")
print(mall.monthly_summary())

