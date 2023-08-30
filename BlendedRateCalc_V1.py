import tkinter as tk


class Role:
    def __init__(self, name, rate_per_hour):
        self.name = name
        self.rate_per_hour = rate_per_hour


class ResourceTracker:
    def __init__(self):
        self.roles = {}
        self.next_role_number = 1
        self.discount_percentage = 0  # Initialize discount percentage

    def add_role(self, role, quantity):
        if role.name in self.roles:
            self.roles[role.name]['quantity'] += quantity
        else:
            self.roles[role.name] = {
                'role': role,
                'quantity': quantity,
            }

    def calculate_blended_rate(self):
        total_billable_amount = 0.0
        total_quantity = 0

        for role_data in self.roles.values():
            role = role_data['role']
            quantity = role_data['quantity']
            rate_with_discount = role.rate_per_hour * (1 - self.discount_percentage / 100)

            total_billable_amount += rate_with_discount * quantity
            total_quantity += quantity
        if total_quantity == 0:
            return 0.0

        blended_rate = total_billable_amount / total_quantity
        return blended_rate

    def calculate_total_cost(self, num_hours):
        blended_rate = self.calculate_blended_rate()
        total_cost = num_hours * blended_rate
        return total_cost

    def add_new_role(self, name, rate_per_hour):
        role = Role(name, rate_per_hour)
        self.roles[name] = {'role': role, 'quantity': 0}
        print(f"{name} with rate ${rate_per_hour:.2f} per hour added as Role {self.next_role_number}")
        self.next_role_number += 1

    def edit_pay(self, role_name, new_rate_per_hour):
        found_role = None
        for role_key in self.roles.keys():
            if role_name.lower() == role_key.lower():
                found_role = role_key
                break

        if found_role:
            self.roles[found_role]['role'].rate_per_hour = new_rate_per_hour
            print(f"The pay for '{found_role}' has been updated to ${new_rate_per_hour:.2f} per hour.")
        else:
            print(f"Role '{role_name}' not found. Cannot edit pay.")

    def set_discount(self, discount_percentage):
        self.discount_percentage = discount_percentage
        print(f"Discount percentage set to {discount_percentage}%")


class ResourceTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Resource Tracker")
        self.resource_tracker = ResourceTracker()

        self.available_roles = [
            {"name": "Project Manager", "rate_per_hour": 95.00},
            {"name": "Senior Developer", "rate_per_hour": 125.00},
            {"name": "Junior Developer", "rate_per_hour": 95.00},
            {"name": "Process Engineer", "rate_per_hour": 105.00},
            {"name": "Functional Architect", "rate_per_hour": 115.00},
            {"name": "Technical Architect", "rate_per_hour": 125.00},
            {"name": "Senior QA Engineer", "rate_per_hour": 75.00},
            {"name": "Junior QA Engineer", "rate_per_hour": 55.00},
            {"name": "Support", "rate_per_hour": 45.00},
        ]

        self.create_widgets()

    def add_new_role(self):
        name = self.new_role_name_entry.get()
        rate_per_hour_str = self.new_role_rate_entry.get()
        try:
            rate_per_hour = float(rate_per_hour_str)
            self.resource_tracker.add_new_role(name, rate_per_hour)
            self.available_roles.append({"name": name, "rate_per_hour": rate_per_hour})
            self.update_available_roles()
        except ValueError:
            print("Invalid rate format. Please enter a valid number.")

        self.new_role_name_entry.delete(0, tk.END)
        self.new_role_rate_entry.delete(0, tk.END)

    def add_existing_role(self):
        choice = self.available_roles_listbox.curselection()
        if not choice:
            return

        index = choice[0]
        role_data = self.available_roles[index]
        role = Role(role_data['name'], role_data['rate_per_hour'])
        quantity_str = self.quantity_entry.get()
        try:
            quantity = float(quantity_str)
            self.resource_tracker.add_role(role, quantity)
            self.update_available_roles()
        except ValueError:
            print("Invalid quantity format. Please enter a valid number.")

        self.quantity_entry.delete(0, tk.END)
        self.quantity_entry.focus_set()

    def delete_role(self):
        choice = self.available_roles_listbox.curselection()
        if not choice:
            return

        index = choice[0]
        role_data = self.available_roles.pop(index)
        self.update_available_roles()
        role_name = role_data['name']

        if role_name in self.resource_tracker.roles:
            del self.resource_tracker.roles[role_name]
            self.calculate_blended_rate()

    def calculate_blended_rate(self):
        blended_rate = self.resource_tracker.calculate_blended_rate()
        self.blended_rate_label.config(text=f"Blended billable rate: ${blended_rate:.2f} per hour")

        self.people_per_role_listbox.delete(0, tk.END)  # Clear the listbox

        for role_data in self.resource_tracker.roles.values():
            role = role_data['role']
            quantity = role_data['quantity']
            self.people_per_role_listbox.insert(tk.END, f"{role.name}: {quantity}")


            self.people_per_role_listbox.Listbox(list=people_per_role_listbox)

    def calculate_total_cost(self):
        num_hours_str = self.num_hours_entry.get()
        try: 
            num_hours = float(num_hours_str)
            total_cost = self.resource_tracker.calculate_total_cost(num_hours)
            self.blended_rate_label.config(text=f"Total Cost for {num_hours} hours: ${total_cost:.2f}")
        except ValueError:
            print("Invalid number of hours format. Please enter a valid number.")

        self.num_hours_entry.delete(0, tk.END)
    def calculate_total_cost(self):
            num_weeks_str = self.num_weeks_entry.get()
            num_hours_str = self.num_hours_entry.get()
        
            try:
                num_weeks = float(num_weeks_str)
                num_hours_per_week = float(num_hours_str)
                total_hours = num_weeks * num_hours_per_week
                total_cost = self.resource_tracker.calculate_total_cost(total_hours)
                self.blended_rate_label.config(text=f"Total Cost for {total_hours} hours: ${total_cost:.2f}")
            except ValueError:
                        print("Invalid number of weeks or hours format. Please enter valid numbers.")
    def edit_pay(self):
        role_name = self.edit_pay_name_entry.get()
        new_rate_per_hour_str = self.new_rate_per_hour_entry.get()
        try:
            new_rate_per_hour = float(new_rate_per_hour_str)
            self.resource_tracker.edit_pay(role_name, new_rate_per_hour)

            # Update the rate_per_hour in available_roles list for consistency
            for role_data in self.available_roles:
                if role_data['name'].lower() == role_name.lower():
                    role_data['rate_per_hour'] = new_rate_per_hour
                    self.update_available_roles()
                    break
        except ValueError:
            print("Invalid rate format. Please enter a valid number.")

        self.edit_pay_name_entry.delete(0, tk.END)
        self.new_rate_per_hour_entry.delete(0, tk.END)

    def set_discount(self):
        discount_percentage_str = self.discount_entry.get()
        try:
            discount_percentage = float(discount_percentage_str)
            self.resource_tracker.set_discount(discount_percentage)
            self.calculate_blended_rate()
        except ValueError:
            print("Invalid discount percentage format. Please enter a valid number.")

        self.discount_entry.delete(0, tk.END)

    def update_available_roles(self):
        self.available_roles_listbox.delete(0, tk.END)
        for role in self.available_roles:
            self.available_roles_listbox.insert(tk.END, f"{role['name']} (${role['rate_per_hour']:.2f} per hour)")

    def create_widgets(self):


        #Weeks
        num_weeks_label = tk.Label(self, text="Enter the number of weeks:")
        num_weeks_label.grid(row=11, column=0, columnspan=2, padx=10, pady=6)

        self.num_weeks_entry = tk.Entry(self)
        self.num_weeks_entry.grid(row=12, column=0, columnspan=2, padx=10, pady=6)

        # Number of Hours per Week
        num_hours_label = tk.Label(self, text="Enter the number of hours per week:")
        num_hours_label.grid(row=13, column=0, columnspan=2, padx=10, pady=6)

        self.num_hours_entry = tk.Entry(self)
        self.num_hours_entry.grid(row=14, column=0, columnspan=2, padx=10, pady=6)

        calculate_total_cost_button = tk.Button(self, text="Calculate Total Cost", command=self.calculate_total_cost)
        calculate_total_cost_button.grid(row=15, column=0, columnspan=2, padx=10, pady=6)
        # Available Roles
        available_roles_label = tk.Label(self, text="Available Roles:")
        available_roles_label.grid(row=0, column=0, columnspan=2, padx=10, pady=6)

        self.available_roles_listbox = tk.Listbox(self, selectmode=tk.SINGLE, height=12, width=35)
        self.available_roles_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=6)

        for role in self.available_roles:
            self.available_roles_listbox.insert(tk.END, f"{role['name']} (${role['rate_per_hour']:.2f} per hour)")
        # Add Role
        new_role_label = tk.Label(self, text="Add a New Role:")
        new_role_label.grid(row=2, column=0, columnspan=2, padx=10, pady=6)

        new_role_name_label = tk.Label(self, text="Name:")
        new_role_name_label.grid(row=3, column=0, padx=10, pady=6, sticky=tk.E)

        self.new_role_name_entry = tk.Entry(self)
        self.new_role_name_entry.grid(row=3, column=1, padx=10, pady=6, sticky=tk.W)

        new_role_rate_label = tk.Label(self, text="Rate per hour ($):")
        new_role_rate_label.grid(row=4, column=0, padx=10, pady=6, sticky=tk.E)

        self.new_role_rate_entry = tk.Entry(self)
        self.new_role_rate_entry.grid(row=4, column=1, padx=10, pady=6, sticky=tk.W)

        add_new_role_button = tk.Button(self, text="Add New Role", command=self.add_new_role)
        add_new_role_button.grid(row=5, column=0, columnspan=2, padx=10, pady=6)

        # Add Existing Role
        quantity_label = tk.Label(self, text="Enter the quantity:")
        quantity_label.grid(row=6, column=0, columnspan=2, padx=10, pady=6)

        self.quantity_entry = tk.Entry(self)
        self.quantity_entry.grid(row=7, column=0, columnspan=2, padx=10, pady=6)

        add_existing_role_button = tk.Button(self, text="Add Role", command=self.add_existing_role)
        add_existing_role_button.grid(row=8, column=0, padx=5, pady=6)

        delete_role_button = tk.Button(self, text="Delete Role", command=self.delete_role)
        delete_role_button.grid(row=8, column=1, padx=5, pady=6)

        # Calculate Blended Rate
        blended_rate_label = tk.Label(self, text="")
        blended_rate_label.grid(row=17, column=0, columnspan=2, padx=10, pady=6)
        self.blended_rate_label = blended_rate_label

        calculate_blended_rate_button = tk.Button(self, text="Calculate Blended Rate", command=self.calculate_blended_rate)
        calculate_blended_rate_button.grid(row=16, column=0, columnspan=2, padx=10, pady=6)

        # Edit Pay
        edit_pay_label = tk.Label(self, text="Edit Pay:")
        edit_pay_label.grid(row=20, column=0, padx=10, pady=6, sticky=tk.E)

        self.edit_pay_name_entry = tk.Entry(self)
        self.edit_pay_name_entry.grid(row=20, column=1, padx=10, pady=6, sticky=tk.W)

        edit_pay_rate_label = tk.Label(self, text="New Rate per hour ($):")
        edit_pay_rate_label.grid(row=21, column=0, padx=10, pady=6, sticky=tk.E)

        self.new_rate_per_hour_entry = tk.Entry(self)
        self.new_rate_per_hour_entry.grid(row=21, column=1, padx=10, pady=6, sticky=tk.W)

        edit_pay_button = tk.Button(self, text="Edit Pay", command=self.edit_pay)
        edit_pay_button.grid(row=22, column=0, columnspan=2, padx=10, pady=6)

        # Discount
        discount_label = tk.Label(self, text="Set Discount (%):")
        discount_label.grid(row=23, column=0, padx=10, pady=6, sticky=tk.E)

        self.discount_entry = tk.Entry(self)
        self.discount_entry.grid(row=23, column=1, padx=10, pady=6, sticky=tk.W)

        set_discount_button = tk.Button(self, text="Set Discount", command=self.set_discount)
        set_discount_button.grid(row=24, column=0, columnspan=2, padx=10, pady=6)


        # People for each role
        people_per_role_label = tk.Label(self, text="People per Role:")
        people_per_role_label.grid(row=0, column=2, padx=4, pady=6, sticky=tk.E)

        self.people_per_role_listbox = tk.Listbox(self, selectmode=tk.SINGLE, height=12, width=35)
        self.people_per_role_listbox.grid(row=1, column=2, padx=8, pady=6, sticky=tk.W)

        # Restart Button
        restart_button = tk.Button(self, text="Reset and Start Over", command=self.restart)
        restart_button.grid(row=26, column=0, columnspan=2, padx=10, pady=6)


    def restart(self):
        self.resource_tracker.roles = {}
        self.resource_tracker.discount_percentage = 0  # Reset discount percentage
        self.update_available_roles()
        self.new_role_name_entry.delete(0, tk.END)
        self.new_role_rate_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.num_hours_entry.delete(0, tk.END)
        self.edit_pay_name_entry.delete(0, tk.END)
        self.new_rate_per_hour_entry.delete(0, tk.END)
        self.discount_entry.delete(0, tk.END)
        self.calculate_blended_rate()


if __name__ == "__main__":
    app = ResourceTrackerApp()
    app.mainloop()