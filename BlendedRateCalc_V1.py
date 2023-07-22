#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 15:22:28 2023

@author: justinhulet
"""

class Role:
    def __init__(self, name, rate_per_hour):
        self.name = name
        self.rate_per_hour = rate_per_hour


class ResourceTracker:
    def __init__(self):
        self.roles = {}  # Dictionary to store Role objects and their quantities
        self.next_role_number = 1

    def add_role(self, role, quantity):
        if role.name in self.roles:
            self.roles[role.name]['quantity'] += quantity
        else:
            self.roles[role.name] = {
                'role': role,
                'quantity': quantity,
            }

    def calculate_blended_rate(self):
        total_billable_rate = 0.0
        total_quantity = 0

        for role_data in self.roles.values():
            role = role_data['role']
            quantity = role_data['quantity']
            total_billable_rate += role.rate_per_hour * quantity
            total_quantity += quantity

        if total_quantity == 0:
            return 0.0

        return total_billable_rate / total_quantity

    def add_new_role(self, name, rate_per_hour):
        role = Role(name, rate_per_hour)
        self.roles[name] = {'role': role, 'quantity': 0}
        print(f"{name} with rate ${rate_per_hour:.2f} per hour added as Role {self.next_role_number}")
        self.next_role_number += 1


def print_available_roles(roles):
    print("Available roles:")
    for index, role in enumerate(roles, start=1):
        print(f"{index}. {role['name']} (${role['rate_per_hour']:.2f} per hour)")


def main():
    available_roles = [
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

    resource_tracker = ResourceTracker()

    while True:
        print_available_roles(available_roles)
        print(f"{len(available_roles) + 1}. Add a new role")
        print(f"{len(available_roles) + 2}. Quit")

        choice = int(input(f"Enter the number of the role (1-{len(available_roles) + 2}) you want to add or "
                           f"{len(available_roles) + 2} to quit: "))

        if choice == len(available_roles) + 2:
            break
        elif choice == len(available_roles) + 1:
            name = input("Enter the name of the new role: ")
            rate_per_hour = float(input("Enter the billable rate per hour for the new role: "))
            resource_tracker.add_new_role(name, rate_per_hour)
            available_roles.append({"name": name, "rate_per_hour": rate_per_hour})
        elif choice in range(1, len(available_roles) + 1):
            role_data = available_roles[choice - 1]
            role = Role(role_data['name'], role_data['rate_per_hour'])
            quantity = int(input(f"Enter the quantity for {role_data['name']}: "))
            resource_tracker.add_role(role, quantity)

            add_another = input("Do you want to add another role? (yes/no): ").lower()
            if add_another != "yes":
                break
        else:
            print("Invalid choice. Please try again.")
            continue

    blended_rate = resource_tracker.calculate_blended_rate()
    print(f"Blended billable rate: ${blended_rate:.2f} per hour")

    restart = input("Do you want to reset and start over? (yes/no): ").lower()
    if restart == "yes":
        main()
    else:
        print("Program ended.")


if __name__ == "__main__":
    main()