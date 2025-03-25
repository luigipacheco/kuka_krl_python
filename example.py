from kuka_krl_python import KRL

name = "example"
krl = KRL(name)

# Define Home Position 
home_position = (5, -90, 100, 5, -10, -5)  # A1 - A6, E1 - E4

# Set Start Position (default linear speed: 0.05 m/s, advance: 3)
krl.set_start_parameters(1, 1, 15, 100, 0.05 , 3)

# Define digital output number
output_no = 5  

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
krl.set_digital_output(output_no, True)  # Turn ON before first movement
krl.add_move_ptp(*first_pos)

# Adjust linear speed dynamically (without modifying advance)
krl.set_linear_speed(0.1)   # Increase speed

# Add remaining points as LIN
for idx, pos in enumerate(positions):
    if idx == 1:
        krl.set_linear_speed(0.03)  # Slow down
    elif idx == 3:
        krl.set_linear_speed(0.08)  # Speed up

    krl.add_linear_move(*pos)

# Turn OFF Digital Output AFTER all motions before returning home
krl.set_digital_output(output_no, False)

# **Return to Home Position (Start Position)**
krl.add_move_ptp(*home_position)

# End and Save Program
krl.end_program()
krl.save_program(name + ".src")

print("KRL program with optimized home return logic generated successfully!")