# **KUKA KRL Python Generator**
A Python class for generating **KUKA KRL** programs dynamically. This project allows users to automate the creation of **KRL (.src) files** for KUKA robots, including **motion commands, tool/base definitions, speed settings, and digital/analog I/O control**.

---

## **📌 Features**
✔ **Generate structured KRL programs dynamically**  
✔ **Define tools, bases, and speed parameters**  
✔ **Create PTP (point-to-point) and LIN (linear) motions**  
✔ **Set digital and analog outputs**  
✔ **Wait for digital inputs or time delays**  
✔ **Add comments and print statements (TPWrite)**  
✔ **Follows KUKA best practices for proper declaration order**  

---

# **KUKA KRL Python Generator - Functions & License**

## **🛠️ Functions**
| Function | Description |
|----------|------------|
| `set_tool(tool_no, mass, cog)` | Defines a tool |
| `set_base(base_no, pos, orient)` | Defines a base |
| `set_speed(speed, acceleration)` | Sets motion speed |
| `set_start_parameters(base, tool, speed, acc, pos)` | Sets the start position |
| `set_linear_speed(speed, advance)` | Sets LIN motion speed |
| `add_move_ptp(x, y, z, a, b, c)` | Adds a PTP move |
| `add_linear_move(x, y, z, a, b, c)` | Adds a LIN move |
| `set_digital_output(output_no, value)` | Turns digital output ON/OFF |
| `set_analog_output(output_no, value)` | Sets an analog output |
| `wait_for_digital_input(input_no, value)` | Waits for a digital input |
| `wait_time(time_sec)` | Adds a time delay |
| `add_comment(msg)` | Adds a comment in the KRL file |
| `add_print_statement(msg)` | Displays a message on the teach pendant |
| `set_end_position(pos)` | Sets the end position |
| `end_program()` | Ends the KRL program |
| `save_program(filename)` | Saves the KRL program |

---

## **📜 License**
GPL
