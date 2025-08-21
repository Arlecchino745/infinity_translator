"""
Debug wrapper for Infinity Translator
This script wraps the main application to catch and log any exceptions
"""

import sys
import traceback
import os
import time

def create_error_log(error_info):
    """Create an error log file with the exception details"""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    log_file = os.path.join(log_dir, f"error-{timestamp}.log")
    
    with open(log_file, "w") as f:
        f.write("Infinity Translator Error Log\n")
        f.write("===========================\n\n")
        f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Python Version: {sys.version}\n")
        f.write(f"Platform: {sys.platform}\n\n")
        f.write("Error Details:\n")
        f.write("-------------\n")
        f.write(error_info)
        
    return log_file

def main():
    """Main entry point that wraps the application and catches exceptions"""
    try:
        # Import the main module
        print("Starting Infinity Translator...")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Python executable: {sys.executable}")
        print(f"Python path: {sys.path}")
        
        # Check if we're running in a PyInstaller bundle
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            print(f"Running in PyInstaller bundle. MEIPASS: {sys._MEIPASS}")
            # Add the PyInstaller bundle directory to the path
            bundle_dir = sys._MEIPASS
            sys.path.insert(0, bundle_dir)
            
            # List files in the bundle directory
            print("\nFiles in PyInstaller bundle:")
            for root, dirs, files in os.walk(bundle_dir):
                rel_path = os.path.relpath(root, bundle_dir)
                if rel_path == ".":
                    rel_path = ""
                for file in files:
                    print(f"  {os.path.join(rel_path, file)}")
        
        # Check for critical files
        critical_files = [
            "templates/index.html",
            "static/favicon.ico",
            "config/settings.json",
            ".env.example"
        ]
        
        print("\nChecking for critical files:")
        for file in critical_files:
            if os.path.exists(file):
                print(f"  ✓ {file} found")
            else:
                print(f"  ✗ {file} NOT found")
        
        # Import and run the main application
        print("\nImporting web_app module...")
        import web_app
        
        print("Starting web server...")
        web_app.start_web_server()
        
    except Exception as e:
        error_info = f"Exception: {str(e)}\n\n"
        error_info += "Traceback:\n"
        error_info += traceback.format_exc()
        
        log_file = create_error_log(error_info)
        
        print("\n" + "="*60)
        print("ERROR: Infinity Translator encountered an error and could not start.")
        print(f"Error details have been saved to: {log_file}")
        print("="*60)
        print("\nError information:")
        print(error_info)
        print("\nPress Enter to exit...")
        input()
        
        sys.exit(1)

if __name__ == "__main__":
    main()