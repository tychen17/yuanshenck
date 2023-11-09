import tkinter as tk
from tkinter import messagebox

# Constants
PRIMO_TO_PULL = 160
RECHARGE_TIERS = {
    8080: 648,
    3880: 328,
    2240: 198,
    1090: 98,
    330: 30,
    60: 6
}

# Calculate constellations
def calculate_constellations(primo, crystal, padded_pulls, existing_pulls, desired_constellations, desired_pulls):
    total_pulls_available = (primo + crystal) // PRIMO_TO_PULL + existing_pulls
    if desired_constellations:
        total_pulls_needed = desired_constellations * 160
    elif desired_pulls:
        total_pulls_needed = desired_pulls
    else:
        raise ValueError("Please enter either desired constellations or expected pulls.")
    constellations_obtained = min(total_pulls_available // 160, desired_constellations if desired_constellations else float('inf'))
    remaining_pulls = total_pulls_available - constellations_obtained * 160
    return constellations_obtained, remaining_pulls

# Calculate recharge
def calculate_recharge(remaining_pulls, desired_constellations, desired_pulls):
    pulls_needed = max(desired_constellations * 160 - remaining_pulls, 0) if desired_constellations else max(desired_pulls - remaining_pulls, 0)
    primo_needed = pulls_needed * PRIMO_TO_PULL
    recharge_plan = {}
    for amount, cost in sorted(RECHARGE_TIERS.items(), key=lambda x: -x[1]):
        count = primo_needed // amount
        if count:
            recharge_plan[cost] = count
            primo_needed -= count * amount
    if primo_needed:
        for amount, cost in sorted(RECHARGE_TIERS.items(), key=lambda x: x[1]):
            if primo_needed <= amount:
                recharge_plan[cost] = recharge_plan.get(cost, 0) + 1
                break
    return primo_needed, recharge_plan

# GUI functions
def calculate():
    try:
        primo = int(primo_entry.get())
        crystal = int(crystal_entry.get())
        padded_pulls = int(padded_pulls_entry.get())
        existing_pulls = int(existing_pulls_entry.get())
        desired_constellations = int(desired_constellations_entry.get() or 0)
        desired_pulls = int(desired_pulls_entry.get() or 0)
        if desired_constellations and desired_pulls:
            raise ValueError("Enter either desired constellations or expected pulls, not both.")
        constellations_obtained, remaining_pulls = calculate_constellations(primo, crystal, padded_pulls, existing_pulls, desired_constellations, desired_pulls)
        primo_needed, recharge_plan = calculate_recharge(remaining_pulls, desired_constellations, desired_pulls)
        result_message = f"Constellations obtained: {constellations_obtained}\n"
        result_message += f"Primogems needed for recharge: {primo_needed}\n"
        result_message += f"Recharge plan: {recharge_plan}\n"
        result_message += f"Total pulls available: {remaining_pulls + constellations_obtained * 160}\n"
        messagebox.showinfo("Wish Planning Result", result_message)
    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Setup GUI
root = tk.Tk()
root.title("Genshin Impact Wish Planning Tool")

# Input fields
labels = ["Primogems", "Crystals", "Padded Pulls", "Existing Pulls", "Desired Constellations", "Expected Pulls"]
entries = []
for i, label in enumerate(labels):
    tk.Label(root, text=label).grid(row=i, column=0)
    entry = tk.Entry(root)
    entry.grid(row=i, column=1)
    entries.append(entry)
(primo_entry, crystal_entry, padded_pulls_entry, existing_pulls_entry, desired_constellations_entry, desired_pulls_entry) = entries

# Calculate button
calculate_button = tk.Button(root, text="Calculate", command=calculate)
calculate_button.grid(row=6, columnspan=2)

# Run the main loop
root.mainloop()