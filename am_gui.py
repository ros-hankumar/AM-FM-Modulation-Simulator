import os
import sys
import subprocess

def main():
    print("==========================================================")
    print("      Analog Communication Modulation Simulator Launcher  ")
    print("==========================================================")
    print("Starting Streamlit server on app.py...")
    print("Press Ctrl+C in this terminal to terminate the server.")
    print("----------------------------------------------------------")
    
    # Get directory of current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(current_dir, "app.py")
    
    try:
        # Run streamlit command
        subprocess.run(["streamlit", "run", app_path], check=True)
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    except Exception as e:
        print(f"\nError launching Streamlit: {e}")
        print("Please ensure Streamlit is installed by running: pip install streamlit")

if __name__ == "__main__":
    main()
