import customtkinter as ctk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageTk, ImageOps, ImageEnhance, ImageFilter

# Initialize the application
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk() 
root.iconbitmap("logo.ico")

class ImageFilterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Image Filter Application")
        self.geometry("1400x800")  # Adjust the window size for better layout

        # Set application logo
        self.set_app_logo()

        # Initialize variables
        self.image = None
        self.filtered_image = None
        self.filtered_images = []  # To hold processed images
        self.image_index = -1  # Keeps track of the current image index

        # UI Setup
        self.create_widgets()

    def set_app_logo(self):
        try:
            logo_image = Image.open("RNS_Filter_logo.jpg")  # Load the ICO logo image
            self.iconphoto(False, ImageTk.PhotoImage(logo_image))  # Set as window icon
        except Exception as e:
            print(f"Error setting logo: {e}")


    def create_widgets(self):
        # Main Frame with background color
        self.main_frame = ctk.CTkFrame(self, width=1400, height=800, corner_radius=20, fg_color="#201F1F")
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Top Menu Bar
        self.menu_bar = ctk.CTkFrame(self.main_frame, width=1400, height=50, corner_radius=15, fg_color="#201F1F")
        self.menu_bar.pack(side="top", fill="x", pady=10)

        # Menu Button
        self.menu_button = ctk.CTkButton(self.menu_bar, text="☰ Menu", width=100, command=self.toggle_sidebar, font=("Arial", 16), fg_color="#867C7F", hover_color="#D4CFD1")
        self.menu_button.pack(side="left", padx=20, pady=10)

        # Sidebar for filters and tools
        self.sidebar = ctk.CTkFrame(self.main_frame, width=250, height=800, corner_radius=15, fg_color="#867C7F")
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        self.sidebar.pack_forget()  # Hide the sidebar initially

        # Sidebar Title (no background color)
        self.sidebar_title = ctk.CTkLabel(self.sidebar, text="Filters & Tools", font=("Arial", 18, "bold"), text_color="white")
        self.sidebar_title.pack(pady=20)

        # Filters Section (no background color)
        ctk.CTkLabel(self.sidebar, text="Filters", font=("Arial", 14), text_color="white").pack(pady=10)

        # Buttons for filters (larger buttons for better visibility)
        self.bw_button = ctk.CTkButton(self.sidebar, text="Black & White", width=220, height=40, command=self.apply_bw_filter, font=("Arial", 12), fg_color="#020B03", hover_color="#8D918E")
        self.bw_button.pack(pady=8)

        self.tint_button = ctk.CTkButton(self.sidebar, text="Apply Color Tint", width=220, height=40, command=self.apply_color_tint, font=("Arial", 12), fg_color="#020B03", hover_color="#8D918E")
        self.tint_button.pack(pady=8)

        self.brightness_button = ctk.CTkButton(self.sidebar, text="Adjust Brightness", width=220, height=40, command=self.adjust_brightness, font=("Arial", 12), fg_color="#020B03", hover_color="#8D918E")
        self.brightness_button.pack(pady=8)

        self.invert_button = ctk.CTkButton(self.sidebar, text="Invert Colors", width=220, height=40, command=self.apply_invert_filter, font=("Arial", 12), fg_color="#020B03", hover_color="#8D918E")
        self.invert_button.pack(pady=8)

        self.sharpen_button = ctk.CTkButton(self.sidebar, text="Sharpen Image", width=220, height=40, command=self.sharpen_image, font=("Arial", 12), fg_color="#020B03", hover_color="#8D918E")
        self.sharpen_button.pack(pady=8)

        # Background Removal Section (no background color)
        ctk.CTkLabel(self.sidebar, text="Background Removal", font=("Arial", 14), text_color="white").pack(pady=20)
        self.remove_bg_button = ctk.CTkButton(self.sidebar, text="Remove Background", width=220, height=40, command=self.remove_background, font=("Arial", 12), fg_color="#020B03", hover_color="#8D918E")
        self.remove_bg_button.pack(pady=8)

        # Right Frame for Image Display
        self.image_frame = ctk.CTkFrame(self.main_frame, width=1150, height=800)
        self.image_frame.pack(side="right", fill="both", expand=True)

        # Labels for displaying images (no background color)
        self.original_label = ctk.CTkLabel(self.image_frame, text="Original Image", width=500, height=400, corner_radius=10, fg_color="#ffffff", text_color="black")
        self.original_label.pack(side="left", padx=10, pady=10)
        self.filtered_label = ctk.CTkLabel(self.image_frame, text="Filtered Image", width=500, height=400, corner_radius=10, fg_color="#ffffff", text_color="black")
        self.filtered_label.pack(side="right", padx=10, pady=10)

        # Control buttons (Save, Load)
        self.control_buttons_frame = ctk.CTkFrame(self.main_frame, fg_color="#030101")
        self.control_buttons_frame.pack(side="bottom", pady=20)

        self.load_button = ctk.CTkButton(self.control_buttons_frame, text="Load Image", width=150, height=40, command=self.load_image, font=("Arial", 12), fg_color="#020B03", hover_color="#8D918E")
        self.load_button.pack(side="left", padx=10)

        # Navigation buttons (Previous and Next)
        self.nav_buttons_frame = ctk.CTkFrame(self.image_frame, fg_color="#020B03")
        self.nav_buttons_frame.pack(side="top", pady=10)

        self.previous_button = ctk.CTkButton(self.nav_buttons_frame, text="Previous", width=120, height=40, command=self.show_previous_image, font=("Arial", 12), fg_color="#020B03", hover_color="#8D918E")
        self.previous_button.pack(side="left", padx=10)

        self.next_button = ctk.CTkButton(self.nav_buttons_frame, text="Next", width=120, height=40, command=self.show_next_image, font=("Arial", 12), fg_color="#020B03", hover_color="#8D918E")
        self.next_button.pack(side="left", padx=10)

        # Save Button below the filtered image
        self.save_button_frame = ctk.CTkFrame(self.image_frame, fg_color="#020B03")
        self.save_button_frame.pack(side="bottom", pady=10)

        self.save_button = ctk.CTkButton(self.save_button_frame, text="Save Image", width=150, height=40, command=self.save_image, font=("Arial", 12), fg_color="#020B03", hover_color="#8D918E")
        self.save_button.pack()

    def toggle_sidebar(self):
        """Toggle the sidebar visibility with sliding animation"""
        if self.sidebar.winfo_ismapped():
            self.sidebar.pack_forget()  # Hide the sidebar
        else:
            self.sidebar.pack(side="left", fill="y", padx=0, pady=0)  # Show it

    def load_image(self):
        """Load an image file and display it"""
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if file_path:
            self.image = Image.open(file_path)
            self.filtered_image = self.image.copy()
            self.filtered_images = [self.image.copy()]  # Start the list of filtered images
            self.image_index = 0  # Set the index to the first image
            self.display_images()
            self.update_buttons_state()

    def display_images(self):
        """Display both original and filtered images"""
        if self.image and self.filtered_image:
            original_img = self.image.resize((500, 400), Image.Resampling.LANCZOS)
            filtered_img = self.filtered_image.resize((500, 400), Image.Resampling.LANCZOS)

            original_img_tk = ImageTk.PhotoImage(original_img)
            filtered_img_tk = ImageTk.PhotoImage(filtered_img)

            self.original_label.configure(image=original_img_tk, text="")
            self.original_label.image = original_img_tk

            self.filtered_label.configure(image=filtered_img_tk, text="")
            self.filtered_label.image = filtered_img_tk

    def apply_bw_filter(self):
        """Convert the image to black and white"""
        if self.image:
            self.filtered_image = ImageOps.grayscale(self.filtered_image)
            self.filtered_images.append(self.filtered_image)
            self.image_index += 1
            self.display_images()
            self.update_buttons_state()

    def apply_color_tint(self):
        """Apply a color tint to the image"""
        if self.image:
            color = colorchooser.askcolor(title="Choose Tint Color")
            if color[0]:
                red, green, blue = map(int, color[0])
                tint_image = ImageOps.colorize(ImageOps.grayscale(self.filtered_image), black="black", white=f"#{red:02x}{green:02x}{blue:02x}")
                self.filtered_image = tint_image
                self.filtered_images.append(self.filtered_image)
                self.image_index += 1
                self.display_images()
                self.update_buttons_state()

    def adjust_brightness(self):
        """Adjust the brightness of the image"""
        if self.image:
            enhancer = ImageEnhance.Brightness(self.filtered_image)
            self.filtered_image = enhancer.enhance(1.5)  # Brightness factor
            self.filtered_images.append(self.filtered_image)
            self.image_index += 1
            self.display_images()
            self.update_buttons_state()

    def apply_invert_filter(self):
        """Invert the colors of the image"""
        if self.image:
            self.filtered_image = ImageOps.invert(self.filtered_image.convert("RGB"))
            self.filtered_images.append(self.filtered_image)
            self.image_index += 1
            self.display_images()
            self.update_buttons_state()

    def sharpen_image(self):
        """Apply sharpen filter to the image"""
        if self.image:
            self.filtered_image = self.filtered_image.filter(ImageFilter.SHARPEN)
            self.filtered_images.append(self.filtered_image)
            self.image_index += 1
            self.display_images()
            self.update_buttons_state()

    def remove_background(self):
        """Remove background (simulated by detecting white or near-white pixels)"""
        if self.image:
            self.filtered_image = self.image.convert("RGBA")
            data = self.filtered_image.getdata()
            new_data = []
            for item in data:
                if item[0] in range(200, 256):
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)
            self.filtered_image.putdata(new_data)
            self.filtered_images.append(self.filtered_image)
            self.image_index += 1
            self.display_images()
            self.update_buttons_state()

    def save_image(self):
        """Save the filtered image"""
        if self.filtered_image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
            if save_path:
                self.filtered_image.save(save_path)

    def show_previous_image(self):
        """Display the previous image in the filtered images list"""
        if self.image_index > 0:
            self.image_index -= 1
            self.filtered_image = self.filtered_images[self.image_index]
            self.display_images()
            self.update_buttons_state()

    def show_next_image(self):
        """Display the next image in the filtered images list"""
        if self.image_index < len(self.filtered_images) - 1:
            self.image_index += 1
            self.filtered_image = self.filtered_images[self.image_index]
            self.display_images()
            self.update_buttons_state()

    def update_buttons_state(self):
        """Enable/Disable Previous and Next buttons based on the image index"""
        if self.image_index == 0:
            self.previous_button.configure(state="disabled")
        else:
            self.previous_button.configure(state="normal")
        
        if self.image_index == len(self.filtered_images) - 1:
            self.next_button.configure(state="disabled")
        else:
            self.next_button.configure(state="normal")


# Run the application
if __name__ == "__main__":
    app = ImageFilterApp()
    app.mainloop()
