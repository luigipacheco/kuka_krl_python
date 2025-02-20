from kuka_krl_python import KRL

filename = "test"
# Example Usage
krl = KRL(filename)

# Define Tool, Base, and Speed
krl.set_tool(tool_no=1)
krl.set_base(base_no=1)
krl.set_speed(speed=15)

# Set Start Position
krl.set_start_position()

# Set LIN speed
krl.set_linear_speed(speed=0.05)

# Add motions (first point is PTP)
positions = [
    (281.36, 304.25, 459.51),  # First move is PTP
    (245.07, 300.67, 459.51),
    (210.17, 290.08, 459.51),
    (178.02, 272.90, 459.51),
    (149.83, 249.76, 459.51),
]

# First movement is PTP
first_pos = positions.pop(0)
krl.add_move_ptp(*first_pos)

# Add remaining points as LIN
for pos in positions:
    krl.add_linear_move(*pos)

# Set End Position
krl.set_end_position()

# End and Save Program
krl.end_program()
krl.save_program(filename+".src")

print("KRL program generated successfully!")