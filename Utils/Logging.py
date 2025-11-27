"""
Data Logging Module
Handles CSV logging of ECU data streams
"""

import csv
import datetime
import os


class DataLogger:
    def __init__(self, speed_unit="MPH", temp_unit="F"):
        """
        Initialize the data logger
        
        Args:
            speed_unit: Unit for speed display (MPH or KPH)
            temp_unit: Unit for temperature display (F or C)
        """
        self.speed_unit = speed_unit
        self.temp_unit = temp_unit
        self.is_logging = False
        self.log_file = None
        self.csv_writer = None
        self.log_filename = None

    def start_logging(self):
        """Start logging data to CSV file"""
        if self.is_logging:
            return  # Already logging
        
        # Create logs directory if it doesn't exist
        if not os.path.exists("logs"):
            os.makedirs("logs")
        
        # Generate filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_filename = f"logs/datalog_{timestamp}.csv"
        
        # Open file and create CSV writer
        self.log_file = open(self.log_filename, 'w', newline='')
        self.csv_writer = csv.writer(self.log_file)
        
        # Write header row
        self.csv_writer.writerow([
            'Timestamp',
            'RPM',
            f'Speed ({self.speed_unit})',
            'TPS (%)',
            f'Temp (°{self.temp_unit})',
            'Timing (°)',
            'Battery (V)',
            'AAC (%)',
            'Injector (ms)'
        ])
        
        self.is_logging = True
        return self.log_filename

    def stop_logging(self):
        """Stop logging data and close file"""
        if not self.is_logging:
            return  # Not currently logging
        
        self.is_logging = False
        
        if self.log_file:
            self.log_file.close()
            self.log_file = None
            self.csv_writer = None
        
        filename = self.log_filename
        self.log_filename = None
        return filename

    def log_data(self, rpm, speed, tps, temp, timing, battery, aac, injector):
        """
        Write current data values to CSV file
        
        Args:
            rpm: Engine RPM value
            speed: Vehicle speed value
            tps: Throttle position sensor percentage
            temp: Engine temperature
            timing: Ignition timing degrees
            battery: Battery voltage
            aac: AAC valve percentage
            injector: Injector pulse width in ms
        """
        if not self.is_logging or not self.csv_writer:
            return
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        self.csv_writer.writerow([
            timestamp,
            rpm,
            speed,
            tps,
            temp,
            timing,
            battery,
            aac,
            injector
        ])

    def __del__(self):
        """Ensure file is closed when object is destroyed"""
        if self.is_logging:
            self.stop_logging()
