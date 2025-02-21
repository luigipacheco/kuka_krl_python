from kuka_krl_python import KRL

name = "test"
krl = KRL(name)

# Set Start Position
krl.set_start_parameters(1, 1, 15, 100)

# Set LIN speed
krl.set_linear_speed(speed=0.05)

# Define digital output number
output_no = 2  # Change to the correct output number

# Add motions (first point is PTP)
positions = [
    (281.36, 304.25, 459.51),  # First move is PTP
    (245.07, 300.67, 459.51),
    (210.17, 290.08, 459.51),
    (178.02, 272.90, 459.51),
    (149.83, 249.76, 459.51),
]

# First movement is PTP (Activate Output BEFORE move)
first_pos = positions.pop(0)
krl.set_digital_output(output_no, 1)  # Turn ON before first move
krl.add_move_ptp(*first_pos)

# Add remaining points as LIN
for pos in positions:
    krl.add_linear_move(*pos)

# Turn OFF Digital Output AFTER all motions before end position
krl.set_digital_output(output_no, 0)

# Set End Position
krl.set_end_position()

# End and Save Program
krl.end_program()
krl.save_program(name + ".src")

print("KRL program generated successfully!")