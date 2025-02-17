import google.generativeai as genai
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk, ImageDraw
import os

class SplashScreen:
    def __init__(self):
        self.splash = tk.Tk()
        self.splash.title("Welcome to VibhavGPT")
        self.splash.configure(bg='#1E1E1E')
        
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(script_dir, "icon.png")
            icon = tk.PhotoImage(file=icon_path)
            self.splash.iconphoto(False, icon)
        except Exception as e:
            print(f"Could not load window icon: {e}")
        
        window_width = 400
        window_height = 300
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.splash.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        # Create logo frame
        logo_frame = tk.Frame(self.splash, bg='#1E1E1E')
        logo_frame.pack(pady=20)
        
        # Fancy logo
        logo_text = "VibhavGPT"
        logo_label = tk.Label(logo_frame, 
                            text=logo_text,
                            font=('Arial Black', 28, 'bold'),
                            fg='#00ff00',
                            bg='#1E1E1E')
        logo_label.pack()
        
        # Decorative underline
        underline = tk.Frame(logo_frame, bg='#00ff00', height=3, width=250)
        underline.pack(pady=5)
        
        # Tagline
        tagline = tk.Label(logo_frame,
                          text="Your Intelligent Assistant",
                          font=('Arial', 14),
                          fg='white',
                          bg='#1E1E1E')
        tagline.pack(pady=10)
        
        # Use button
        self.use_button = tk.Button(self.splash,
                                  text="Use VibhavGPT",
                                  command=self.launch_main_app,
                                  bg='#4CAF50',
                                  fg='white',
                                  font=('Arial', 12, 'bold'),
                                  padx=20,
                                  pady=10)
        self.use_button.pack(pady=20)
        
    def launch_main_app(self):
        self.splash.destroy()
        root = tk.Tk()
        app = VibhavGPT(root)
        root.mainloop()

class VibhavGPT:
    """A class that implements a chat interface using Google's Gemini Pro model"""
    
    def __init__(self, root):
        self.window = root
        self.window.title("VibhavGPT")
        self.window.configure(bg='#1E1E1E')
        
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(script_dir, "icon.png")
            icon = tk.PhotoImage(file=icon_path)
            self.window.iconphoto(True, icon)
        except Exception as e:
            print(f"Could not load window icon: {e}")
        
        self.window.minsize(800, 800)
        
        self.api_key = "YOUR_GEMINI_API_KEY"#Go to Google AI Studio (https://makersuite.google.com/app/apikey) 
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Create animation frame with specific size
        self.animation_frame = tk.Frame(self.window, bg='#1E1E1E', width=150, height=150)
        self.animation_frame.pack(side=tk.TOP, anchor='ne', padx=20, pady=10)
        
        # Load running animation
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            self.running_man_frames = self.load_animation(os.path.join(script_dir, "running_man.gif"))
            
            self.animation_label = tk.Label(self.animation_frame, bg='#1E1E1E')
            self.animation_label.place(relx=1.0, rely=0.0, anchor='ne')
            self.animation_label.configure(bg='#1E1E1E')
            
            # Add "Running..." text below the animation
            self.running_text = tk.Label(self.animation_frame, 
                                       text="Running...", 
                                       bg='#1E1E1E', 
                                       fg='white',
                                       font=('Comic Sans MS', 10))
            self.running_text.place(relx=1.0, rely=1.0, anchor='se')
            
            self.animate_running_man(0)
            
        except Exception as e:
            print(f"Could not load animation: {e}")
        
        # Create main frame for chat
        self.main_frame = tk.Frame(self.window, bg='#1E1E1E')
        self.main_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        self.label = tk.Label(self.main_frame, text="Welcome to Vibhav-GPT!", bg='#1E1E1E', fg='#FFFFFF', 
                             font=('Comic Sans MS', 14))
        self.label.pack(anchor='w')

        self.chat_history = scrolledtext.ScrolledText(self.main_frame, state='disabled', width=70, height=20,
                                                     bg='#2D2D2D', fg='#FFFFFF', font=('Comic Sans MS', 12))
        self.chat_history.pack(anchor='w', fill=tk.BOTH, expand=True, pady=5)

        self.entry_label = tk.Label(self.main_frame, text="Enter your prompt:", bg='#1E1E1E', fg='#FFFFFF',
                                   font=('Comic Sans MS', 12))
        self.entry_label.pack(anchor='w')

        self.user_input = tk.Entry(self.main_frame, width=70, bg='#2D2D2D', fg='#FFFFFF', 
                                  insertbackground='#FFFFFF', font=('Comic Sans MS', 12))
        self.user_input.pack(anchor='w', fill=tk.X, pady=(5, 10))
        self.user_input.bind('<Return>', self.process_input)

        self.send_button = tk.Button(self.main_frame, text="Send", command=self.process_input,
                                   bg='#4CAF50', fg='white', activebackground='#45a049', 
                                   activeforeground='white', font=('Comic Sans MS', 12),
                                   padx=20, pady=5)
        self.send_button.pack(anchor='w', pady=(0, 10))

    def load_animation(self, image_path):
        frames = []
        image = Image.open(image_path)
        
        try:
            while True:
                frame = image.copy()
                frame = frame.resize((80, 50), Image.Resampling.LANCZOS)
                if frame.mode != 'RGBA':
                    frame = frame.convert('RGBA')
                
                data = frame.getdata()
                newData = []
                for item in data:
                    if item[3] > 100 and sum(item[0:3]) < 500:
                        newData.append((255, 255, 255, 255))
                    else:
                        newData.append((0, 0, 0, 0))
                frame.putdata(newData)
                
                frames.append(ImageTk.PhotoImage(frame))
                image.seek(len(frames))
        except EOFError:
            pass
        
        return frames

    def animate_running_man(self, frame_index):
        if hasattr(self, 'running_man_frames') and self.running_man_frames:
            self.animation_label.configure(image=self.running_man_frames[frame_index])
            next_frame = (frame_index + 1) % len(self.running_man_frames)
            self.window.after(100, self.animate_running_man, next_frame)

    def process_input(self, event=None):
        user_query = self.user_input.get()
        if not user_query:
            return
            
        self.display_message(f"You: {user_query}")
        
        # Update text to "Thinking..."
        self.running_text.config(text="Thinking...")
        self.window.update()
        
        response = self.get_response(user_query)
        
        # Change text back to "Running..."
        self.running_text.config(text="Running...")
        
        self.display_message(f"Vibhav-GPT: {response}")
        self.user_input.delete(0, tk.END)

    def display_message(self, message):
        self.chat_history.config(state='normal')
        self.chat_history.configure(wrap=tk.WORD)
        self.chat_history.insert(tk.END, message + '\n\n')
        self.chat_history.config(state='disabled')
        self.chat_history.see(tk.END)

    def get_response(self, query):
        try:
            response = self.model.generate_content(query)
            return response.text
        except Exception as e:
            return f"An error occurred: {str(e)}"

def create_icon():
    img = Image.new('RGBA', (48, 48), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    
    draw.line([(8, 8), (8, 40)], fill=(0, 0, 0, 255), width=3)
    draw.line([(40, 8), (40, 40)], fill=(0, 0, 0, 255), width=3)
    points = [(16, 12), (24, 36), (32, 12)]
    draw.line(points, fill=(0, 0, 0, 255), width=3)
    
    img.save('icon.png')

create_icon()

if __name__ == "__main__":
    splash = SplashScreen()
    splash.splash.mainloop()
