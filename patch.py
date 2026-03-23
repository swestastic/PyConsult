import sys

with open('Windows/DataStreamWindow.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if "# Frame dimensions" in line and lines[i+1].strip() == "frame_width = 200":
        skip = True
        
        # INSERT NEW __INIT__
        new_lines.append('        # Frame dimensions\n')
        new_lines.append('        frame_width = 240\n')
        new_lines.append('        frame_height = 160\n\n')
        new_lines.append('        # Value ranges used to position gauge needles\n')
        new_lines.append('        speed_max = 160 if self.speed_unit == "MPH" else 260\n')
        new_lines.append('        self.gauge_ranges = {\n')
        new_lines.append('            \'RPM\': (0, 8000),\n')
        new_lines.append('            \'Speed\': (0, speed_max),\n')
        new_lines.append('            \'TPS\': (0, 100),\n')
        new_lines.append('            \'Temp\': (-40, 250 if self.temp_unit == "F" else 120),\n')
        new_lines.append('            \'Timing\': (-10, 50),\n')
        new_lines.append('            \'Battery\': (8, 16),\n')
        new_lines.append('            \'AAC\': (0, 100),\n')
        new_lines.append('            \'Injector\': (0, 20)\n')
        new_lines.append('        }\n\n')
        new_lines.append('        self.gauge_titles = {\n')
        new_lines.append('            \'RPM\': "RPM",\n')
        new_lines.append('            \'Speed\': f"Speed ({self.speed_unit})",\n')
        new_lines.append('            \'TPS\': "TPS (%)",\n')
        new_lines.append('            \'Temp\': f"Temp (°{self.temp_unit})",\n')
        new_lines.append('            \'Timing\': "Timing (°)",\n')
        new_lines.append('            \'Battery\': "Battery (V)",\n')
        new_lines.append('            \'AAC\': "AAC (%)",\n')
        new_lines.append('            \'Injector\': "Injector (ms)"\n')
        new_lines.append('        }\n')
        new_lines.append('        self.gauge_needles = {}\n\n')
        new_lines.append('        # Create all sensor frames and labels\n')
        new_lines.append('        self._create_sensor_frames(frame_width, frame_height)\n\n')
        continue

    if skip and "# Start updating values" in line:
        skip = False
        new_lines.append(line)
        continue

    if not skip:
        new_lines.append(line)

lines = new_lines
new_lines = []
skip = False

for i, line in enumerate(lines):
    if "def _create_sensor_frames(self, frame_width, frame_height):" in line:
        skip = True
        
        # INSERT NEW METHODS
        code = """    def _create_sensor_frames(self, frame_width, frame_height):
        \"\"\"Create all sensor display frames\"\"\"
        self.RPMframe = self._create_gauge(0, 0, 'RPM', frame_width, frame_height)
        self.Speedframe = self._create_gauge(0, 1, 'Speed', frame_width, frame_height)
        self.Tempframe = self._create_gauge(0, 2, 'Temp', frame_width, frame_height)
        self.TPSframe = self._create_gauge(1, 0, 'TPS', frame_width, frame_height)
        self.Timingframe = self._create_gauge(1, 1, 'Timing', frame_width, frame_height)
        self.Batteryframe = self._create_gauge(1, 2, 'Battery', frame_width, frame_height)
        self.AACframe = self._create_gauge(2, 0, 'AAC', frame_width, frame_height)
        self.Injectorframe = self._create_gauge(2, 1, 'Injector', frame_width, frame_height)

        # Data logging button
        self.log_button = ttk.Button(self.window, text="Start Data Logging", command=self.toggle_logging, width=20)
        self.log_button.grid(row=3, column=0, columnspan=3, pady=20)

    def _create_gauge(self, row, col, sensor_key, frame_width, frame_height):
        \"\"\"Create a full semi-circular gauge with text inside.\"\"\"
        frame = tk.Frame(self.window, relief=tk.RIDGE, borderwidth=2, width=frame_width, height=frame_height)
        frame.grid_propagate(False)
        frame.grid(row=row, column=col, padx=10, pady=10)

        gauge = tk.Canvas(frame, width=frame_width, height=frame_height, highlightthickness=0, bg=frame.cget("bg"))
        gauge.pack(fill=tk.BOTH, expand=True)

        center_x = frame_width // 2
        center_y = int(frame_height * 0.70)
        radius = min(center_x, center_y) - 20

        # Dial arc from left (min) to right (max)
        gauge.create_arc(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            start=0, extent=180,
            style=tk.ARC, outline="#9f9f9f", width=4
        )

        title = self.gauge_titles.get(sensor_key, sensor_key)
        # Text slightly above center
        gauge.create_text(center_x, center_y - (radius * 0.6), text=title, font=("Arial", 11, "bold"))
        
        # Center numerical value
        val_text_id = gauge.create_text(center_x, center_y - 12, text="0", font=("Arial", 16, "bold"))

        minimum, maximum = self.gauge_ranges.get(sensor_key, (0, 100))

        # Ticks and labels
        num_ticks = 5
        for i in range(num_ticks):
            fraction = i / (num_ticks - 1)
            val = minimum + (maximum - minimum) * fraction
            
            angle_deg = 180 - (180 * fraction)
            import math
            angle_rad = math.radians(angle_deg)
            
            # Tick lines
            outer_x = center_x + radius * math.cos(angle_rad)
            outer_y = center_y - radius * math.sin(angle_rad)
            inner_x = center_x + (radius - 8) * math.cos(angle_rad)
            inner_y = center_y - (radius - 8) * math.sin(angle_rad)
            gauge.create_line(inner_x, inner_y, outer_x, outer_y, fill="#555555", width=2)
            
            # Labels
            if maximum - minimum < 25:
                label_str = f"{val:.1f}"
            else:
                label_str = f"{int(val)}"
                
            text_r = radius + 11
            text_x = center_x + text_r * math.cos(angle_rad)
            text_y = center_y - text_r * math.sin(angle_rad)
            
            # Keep labels within visible area of the canvas 
            if i == 0:
                text_x += 5
            elif i == num_ticks - 1:
                text_x -= 5
                
            gauge.create_text(text_x, text_y, text=label_str, font=("Arial", 8))

        # Needle
        needle_id = gauge.create_line(center_x, center_y, center_x - radius, center_y, fill="#c62828", width=3)
        hub_id = gauge.create_oval(center_x - 5, center_y - 5, center_x + 5, center_y + 5, fill="#444444", outline="")

        self.gauge_needles[sensor_key] = {
            'canvas': gauge,
            'val_text_id': val_text_id,
            'needle_id': needle_id,
            'center_x': center_x,
            'center_y': center_y,
            'radius': radius - 4,
            'min': minimum,
            'max': maximum
        }
        return frame

    def _update_gauge(self, sensor_key, value):
        \"\"\"Move gauge needle and update text.\"\"\"
        gauge_data = self.gauge_needles.get(sensor_key)
        if not gauge_data:
            return

        minimum = gauge_data['min']
        maximum = gauge_data['max']
        if maximum <= minimum:
            return

        gauge = gauge_data['canvas']
        val_text_id = gauge_data['val_text_id']
        
        # Formatting for display
        if maximum - minimum < 25:
            display_str = f"{value:.1f}"
        else:
            display_str = f"{int(value)}"
        gauge.itemconfig(val_text_id, text=display_str)

        clamped = max(minimum, min(maximum, value))
        normalized = (clamped - minimum) / (maximum - minimum)

        import math
        angle_deg = 180 * (1 - normalized)
        angle_rad = math.radians(angle_deg)

        center_x = gauge_data['center_x']
        center_y = gauge_data['center_y']
        radius = gauge_data['radius']
        tip_x = center_x + (radius * math.cos(angle_rad))
        tip_y = center_y - (radius * math.sin(angle_rad))

        needle_id = gauge_data['needle_id']
        gauge.coords(needle_id, center_x, center_y, tip_x, tip_y)

    def _update_values(self):
        \"\"\"Update all displayed values from the ReadStream\"\"\"
        try:
            self._update_gauge('RPM', self.R.RPM_Value)
            self._update_gauge('Speed', self.R.SPEED_Value)
            self._update_gauge('TPS', self.R.TPS_Value)
            self._update_gauge('Temp', self.R.TEMP_Value)
            self._update_gauge('Timing', self.R.TIM_Value)
            self._update_gauge('Battery', self.R.BATT_Value)
            self._update_gauge('AAC', self.R.AAC_Value)
            self._update_gauge('Injector', self.R.INJ_Value)
            
            # Log data if logging is enabled
            if self.logger.is_logging:
                self.logger.log_data(
                    self.R.RPM_Value,
                    self.R.SPEED_Value,
                    self.R.TPS_Value,
                    self.R.TEMP_Value,
                    self.R.TIM_Value,
                    self.R.BATT_Value,
                    self.R.AAC_Value,
                    self.R.INJ_Value
                )
            
            # Schedule next update
            self.window.after(100, self._update_values)
        except:
            pass  # Window may have been closed
\n"""
        new_lines.append(code)
        continue

    if skip and "def toggle_logging(self):" in line:
        skip = False
        new_lines.append(line)
        continue

    if not skip:
        new_lines.append(line)

with open('Windows/DataStreamWindow.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
