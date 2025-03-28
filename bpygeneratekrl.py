import bpy

def export_KRL():
    # Import KRL module from Blender Text Editor
    kuka_krl = bpy.data.texts["kuka_krl_python.py"].as_module()

    obj = bpy.context.object
    if not obj:
        print("No object selected.")
        return

    # Get object name for the filename
    filename = f"{obj.name}.src"

    # Get custom properties from the scene
    scene = bpy.data.scenes['Scene']
    base_num = scene.sna_basen
    tool_num = scene.sna_tooln
    speed = scene.sna_speed
    lin_speed = scene.sna_lspeed
    acc = scene.sna_acc
    advance = scene.sna_advance

    # Define home position (A1 - A6, E1 - E4)
    home_position = (5, -90, 100, 5, -10, -5)  # A1 - A6, E1 - E4

    # Create KRL program
    krl_program = kuka_krl.KRL(program_name=obj.name)
    krl_program.set_start_parameters(base_num, tool_num, speed, acc, lin_speed, advance)
    krl_program.set_linear_speed(lin_speed)

    # **Move to Home Position using PTP**
    krl_program.add_move_ptp(*home_position, joint=True)

    # Get world matrix (to transform local to global)
    world_matrix = obj.matrix_world
    scale = obj.scale

    # Evaluate the object to get mesh data
    depsgraph = bpy.context.evaluated_depsgraph_get()
    eval_obj = obj.evaluated_get(depsgraph)

    # Retrieve position data (apply transformation and scale)
    positions = []
    if "position" in eval_obj.data.attributes:
        for pos in eval_obj.data.attributes["position"].data:
            local_pos = pos.vector  # Local coordinates
            global_pos = world_matrix @ local_pos  # Convert to global space

            # Apply object scale and convert to mm
            x, y, z = global_pos.x * scale.x * 1000, global_pos.y * scale.y * 1000, global_pos.z * scale.z * 1000  
            positions.append((x, y, z))
    else:
        print("No position attribute found.")
        return

    if not positions:
        print("No valid positions found.")
        return

    # Retrieve optional attributes and verify data presence
    extrudes = eval_obj.data.attributes.get("E_SPEED", None)
    enables = eval_obj.data.attributes.get("E_ENABLE", None)
    lin_speeds = eval_obj.data.attributes.get("L_SPEED", None)
    fan_speeds = eval_obj.data.attributes.get("F_SPEED", None)  # Add F_SPEED attribute

    extrudes = extrudes.data if extrudes else [None] * len(positions)
    enables = enables.data if enables else [None] * len(positions)
    lin_speeds = lin_speeds.data if lin_speeds else [None] * len(positions)
    fan_speeds = fan_speeds.data if fan_speeds else [None] * len(positions)  # Add fan speeds data

    # **Move to First Position using PTP**
    first_position = positions.pop(0)
    krl_program.add_move_ptp(*first_position)

    prev_extrude = None
    prev_enable = None
    prev_speed = None
    prev_fan_speed = None  # Add previous fan speed tracking
    extrude_value = None
    enable_state = None
    speed_value = None
    fan_speed_value = None  # Add fan speed value variable

    # **Move through all points using LIN**
    for i, pos in enumerate(positions):
        extrude_value = extrudes[i+1].value if (extrudes[i+1] and hasattr(extrudes[i+1], 'value')) else None
        enable_state = bool(enables[i+1].value) if (enables[i+1] and hasattr(enables[i+1], 'value')) else False  # Default to False
        speed_value = lin_speeds[i+1].value if (lin_speeds[i+1] and hasattr(lin_speeds[i+1], 'value')) else None
        fan_speed_value = fan_speeds[i+1].value if (fan_speeds[i+1] and hasattr(fan_speeds[i+1], 'value')) else None  # Get fan speed value
        
        if speed_value is not None and speed_value != prev_speed:
            krl_program.set_linear_speed(speed_value)
            prev_speed = speed_value
            print(f"Linear speed changed to {speed_value}")
            
        if extrude_value is not None and extrude_value != prev_extrude:
            krl_program.change_variable('E_SPEED', extrude_value)  # Properly assigned extrude_value
            prev_extrude = extrude_value  # Store new value
            print("speed changed")

        # Check if E_ENABLE has changed before updating
        if enable_state is not None and enable_state != prev_enable:
            krl_program.change_variable('E_ENABLE', enable_state)  # Properly assigned enable_state
            prev_enable = enable_state  # Store new value
            print("state changed")

        # Check if F_SPEED has changed before updating
        if fan_speed_value is not None and fan_speed_value != prev_fan_speed:
            krl_program.change_variable('F_SPEED', fan_speed_value)  # Update fan speed
            prev_fan_speed = fan_speed_value  # Store new value
            print("fan speed changed")
            
        # Move in a straight line
        print(i)
        krl_program.add_linear_move(*pos)

    krl_program.add_move_ptp(*home_position,joint=True)

    # Finalize and save the KRL program
    krl_program.end_program()
    
    # Save as a Blender text block
    if filename in bpy.data.texts:
        bpy.data.texts[filename].clear()
    else:
        bpy.data.texts.new(filename)
    
    bpy.data.texts[filename].write(krl_program.program)
    print(f"KRL program saved as '{filename}' in Blender text editor.")

export_KRL()