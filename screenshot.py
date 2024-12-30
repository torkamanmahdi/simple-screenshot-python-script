import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageGrab, Image
import pyautogui

class ScreenshotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screenshot App")
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.rect = None
        self.canvas = None
        self.overlay = None

        # Create buttons
        full_page_button = tk.Button(root, text="Take Full Page Screenshot", command=self.on_full_page)
        full_page_button.pack(pady=10)

        custom_size_button = tk.Button(root, text="Take Custom Size Screenshot", command=self.on_custom_size)
        custom_size_button.pack(pady=10)

    def on_full_page(self):
        screenshot = pyautogui.screenshot()
        self.save_screenshot(screenshot)

    def on_custom_size(self):
        self.root.withdraw()  # Hide the main window
        self.create_overlay()

    def create_overlay(self):
        # Create a transparent overlay window
        self.overlay = tk.Toplevel(self.root)
        self.overlay.attributes("-fullscreen", True)
        self.overlay.attributes("-alpha", 0.3)  # Semi-transparent
        self.overlay.attributes("-topmost", True)
        self.canvas = tk.Canvas(self.overlay, cursor="cross", bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Bind mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

    def on_mouse_press(self, event):
        # Record the starting position of the rectangle
        self.start_x = event.x
        self.start_y = event.y

    def on_mouse_drag(self, event):
        # Draw the rectangle as the user drags the mouse
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y, outline="red", width=2
        )

    def on_mouse_release(self, event):
        # Record the ending position of the rectangle
        self.end_x = event.x
        self.end_y = event.y
        self.overlay.destroy()  # Close the overlay
        self.root.deiconify()  # Restore the main window

        # Ensure coordinates are in the correct order
        x1 = min(self.start_x, self.end_x)
        y1 = min(self.start_y, self.end_y)
        x2 = max(self.start_x, self.end_x)
        y2 = max(self.start_y, self.end_y)

        # Take the screenshot of the selected region
        screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
        self.save_screenshot(screenshot)

    def save_screenshot(self, screenshot):
        if screenshot:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
            if file_path:
                screenshot.save(file_path, "JPEG")
                messagebox.showinfo("Success", f"Screenshot saved successfully at {file_path}")
            else:
                messagebox.showwarning("Warning", "No file path selected!")
        else:
            messagebox.showerror("Error", "No screenshot taken!")

# Create the main window
root = tk.Tk()
app = ScreenshotApp(root)
root.mainloop()
