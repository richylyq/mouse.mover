import tkinter as tk
from tkinter import ttk
import pyautogui
import time
import threading

# Safety feature: Move mouse to any corner to abort
pyautogui.FAILSAFE = True

class MouseMoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse Jiggler")
        self.root.geometry("300x200")
        self.root.resizable(False, False)
        
        # State variable
        self.is_running = False
        self.mover_thread = None
        self.nudge_strength = tk.IntVar(value=10) # Default strength: 10 pixels

        # Style Configuration
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 11), padding=10)
        
        # Status Label
        self.status_label = tk.Label(root, text="Status: Stopped", fg="red", font=("Arial", 12, "bold"))
        self.status_label.pack(pady=20)

        # Slider Label
        self.slider_label = tk.Label(root, text="Nudge Strength: 10 px", font=("Arial", 10))
        self.slider_label.pack()

        # Slider (Scale) - Range from 1 to 50 pixels
        self.strength_slider = ttk.Scale(
            root, 
            from_=1, 
            to=50, 
            orient="horizontal", 
            variable=self.nudge_strength,
            command=self.update_slider_label
        )
        self.strength_slider.pack(fill="x", padx=40, pady=5)

        # Start/Stop Button
        self.action_button = ttk.Button(root, text="Start", command=self.toggle_mover)
        self.action_button.pack(pady=10)

    def update_slider_label(self, value):
        # Dynamically updates the text above the slider as you drag it
        self.slider_label.config(text=f"Nudge Strength: {int(float(value))} px")

    def toggle_mover(self):
        if not self.is_running:
            # Start the background loop
            self.is_running = True
            self.status_label.config(text="Status: Active", fg="green")
            self.action_button.config(text="Stop")
            
            # Run the loop in a separate thread so the GUI doesn't freeze
            self.mover_thread = threading.Thread(target=self.mover_loop, daemon=True)
            self.mover_thread.start()
        else:
            # Stop the loop
            self.stop_mover()

    def stop_mover(self):
        self.is_running = False
        self.status_label.config(text="Status: Stopped", fg="red")
        self.action_button.config(text="Start")

    def mover_loop(self):
        while self.is_running:
            try:
                # Grab the current strength from the slider dynamically
                current_pixel_distance = self.nudge_strength.get()
                
                # Move relative to current position based on slider value
                pyautogui.moveRel(current_pixel_distance, current_pixel_distance, duration=0.8)
                pyautogui.moveRel(-1, -1, duration=0.9)

                # Check every second if the user hit 'Stop' instead of sleeping for 60s straight
                for _ in range(60):
                    if not self.is_running:
                        break
                    time.sleep(1)
                    
            except pyautogui.FailSafeException:
                # If user slams mouse to a corner, safely turn off the app
                self.root.after(0, self.stop_mover)
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = MouseMoverApp(root)
    root.mainloop()