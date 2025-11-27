"""
PyConsult - Main Application Entry Point
Desktop ECU diagnostics tool using Tkinter
"""

from Windows.LandingWindow import LandingWindow


def main():
    """Main entry point for PyConsult application"""
    config_file = 'configJSON.json'
    app = LandingWindow(config_file)
    app.run()


if __name__ == "__main__":
    main()