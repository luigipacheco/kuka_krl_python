class KRL:
    def __init__(self, program_name="rdftshirt"):
        self.program = ""
        self.program_name = program_name
        self.start_program()

    def start_program(self):
        """Initializes the KRL program with default settings"""
        self.program += (
            "&ACCESS RVP\n"
            "&REL 1\n"
            "&PARAM TEMPLATE = C:\\KRC\\Roboter\\Template\\vorgabe\n"
            "&PARAM EDITMASK = *\n"
            f"DEF {self.program_name}()\n\n"
            ";FOLD INI\n"
            ";FOLD BASISTECH INI\n"
            "GLOBAL INTERRUPT DECL 3 WHEN $STOPMESS==TRUE DO IR_STOPM()\n"
            "INTERRUPT ON 3\n"
            "BAS(#INITMOV, 0)\n"
            ";ENDFOLD (BASISTECH INI)\n"
            ";ENDFOLD (INI)\n\n"
        )

    def set_tool(self, tool_no=5, mass=0.5, cog=[0, 0, 0]):
        """Defines a tool"""
        self.program += (
            f"DECL TOOLDATA TOOL_{tool_no} = {{M {mass}, CM {{X {cog[0]}, Y {cog[1]}, Z {cog[2]}}}}}\n"
        )

    def set_base(self, base_no=3, pos=[0, 0, 0], orient=[0, 0, 0]):
        """Defines a base"""
        self.program += (
            f"DECL FRAME BASE_{base_no} = {{X {pos[0]}, Y {pos[1]}, Z {pos[2]}, A {orient[0]}, B {orient[1]}, C {orient[2]}}}\n"
        )

    def set_speed(self, speed=15, acceleration=100):
        """Sets motion speed"""
        self.program += f"DECL REAL VEL = {speed}\n"
        self.program += f"DECL REAL ACC = {acceleration}\n"

    def set_start_position(self, base=3, tool=5, speed=15, pos=None):
        """Sets the start position for the robot"""
        if pos is None:
            pos = {"A1": 5, "A2": -90, "A3": 100, "A4": 5, "A5": -10, "A6": -5, "E1": 0, "E2": 0, "E3": 0, "E4": 0}
        
        self.program += (
            f";FOLD STARTPOSITION - BASE IS {base}, TOOL IS {tool}, SPEED IS {speed}%, POSITION IS "
            f"A1 {pos['A1']}, A2 {pos['A2']}, A3 {pos['A3']}, A4 {pos['A4']}, A5 {pos['A5']}, A6 {pos['A6']}, "
            f"E1 {pos['E1']}, E2 {pos['E2']}, E3 {pos['E3']}, E4 {pos['E4']}\n"
            "$BWDSTART = FALSE\n"
            f"PDAT_ACT = {{VEL {speed}, ACC 100, APO_DIST 50}}\n"
            f"FDAT_ACT = {{TOOL_NO {tool}, BASE_NO {base}, IPO_FRAME #BASE}}\n"
            f"BAS(#PTP_PARAMS, {speed})\n"
            f"PTP {{A1 {pos['A1']}, A2 {pos['A2']}, A3 {pos['A3']}, A4 {pos['A4']}, A5 {pos['A5']}, A6 {pos['A6']}, "
            f"E1 {pos['E1']}, E2 {pos['E2']}, E3 {pos['E3']}, E4 {pos['E4']}}}\n"
            ";ENDFOLD\n\n"
        )

    def set_linear_speed(self, speed=0.05, advance=3):
        """Sets LIN motion speed"""
        self.program += (
            ";FOLD LIN SPEED IS 0.05 m/sec, INTERPOLATION SETTINGS IN FOLD\n"
            f"$VEL.CP={speed}\n"
            f"$ADVANCE={advance}\n"
            ";ENDFOLD\n"
        )

    def add_linear_move(self, x, y, z, a=0, b=90, c=0):
        """Adds a linear move"""
        self.program += f"LIN {{X {x}, Y {y}, Z {z}, A {a}, B {b}, C {c}}} C_DIS\n"
    
    def add_move_ptp(self, x, y, z, a=0, b=90, c=0):
        """Adds a PTP move"""
        self.program += f"PTP {{X {x}, Y {y}, Z {z}, A {a}, B {b}, C {c}}}\n"

    def add_wait(self, time):
        """Adds a wait instruction"""
        self.program += f"WAIT SEC {time}\n"

    def set_digital_output(self, output_no, value):
        """Sets a digital output"""
        self.program += f"$OUT[{output_no}] = {value}\n"

    def set_analog_output(self, output_no, value):
        """Sets an analog output"""
        self.program += f"$ANOUT[{output_no}] = {value}\n"

    def add_comment(self, msg):
        """Adds a comment"""
        self.program += f"; {msg}\n"

    def add_print_statement(self, msg):
        """Prints a message on the teach pendant"""
        self.program += f"TPWrite \"{msg}\"\n"

    def set_end_position(self, pos=None):
        """Sets the end position with PTP"""
        if pos is None:
            pos = {"A1": 5, "A2": -90, "A3": 100, "A4": 5, "A5": -10, "A6": -5, "E1": 0, "E2": 0, "E3": 0, "E4": 0}

        self.program += (
            f"PTP {{A1 {pos['A1']}, A2 {pos['A2']}, A3 {pos['A3']}, A4 {pos['A4']}, A5 {pos['A5']}, A6 {pos['A6']}, "
            f"E1 {pos['E1']}, E2 {pos['E2']}, E3 {pos['E3']}, E4 {pos['E4']}}} C_PTP\n"
            ";ENDFOLD\n\n"
        )

    def end_program(self):
        """Ends the KRL program"""
        self.program += "END\n"

    def save_program(self, filename="generated_module.src"):
        """Saves the KRL program to a file"""
        with open(filename, 'w') as file:
            file.write(self.program)

