import customtkinter as ctk
import threading
import webbrowser
import requests
from tkinter import messagebox


# ===== MODIFICATION START: backend API connection settings =====
BACKEND_URL = "http://127.0.0.1:8000"
# ===== MODIFICATION END: backend API connection settings =====


# ===== MODIFICATION START: backend API call =====
def handle_chat(user_text: str):
    """
    Send the user's message to the backend API and return the JSON result.
    """
    response = requests.post(
        f"{BACKEND_URL}/recommend",
        json={"message": user_text},
        timeout=15
    )
    response.raise_for_status()
    return response.json()
# ===== MODIFICATION END: backend API call =====


class MusicTherapyUI:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("MoodTune")
        self.root.geometry("1180x760")
        self.root.minsize(980, 680)

        # ===== VISUAL MODIFICATION START: improved readable palette =====
        self.window_fg = "#18181b"
        self.card_fg = "#232329"
        self.bot_bubble_fg = "#31313a"
        self.user_bubble_fg = "#4f46e5"
        self.system_bubble_fg = "#475569"
        self.secondary_text = "#cbd5e1"
        self.info_card_fg = "#202028"
        self.subcard_fg = "#2a2a33"
        self.track_button_fg = "#3b3b46"
        self.track_button_hover = "#52525f"
        # ===== VISUAL MODIFICATION END: improved readable palette =====

        self.root.configure(fg_color=self.window_fg)

        self.build_ui()

    def build_ui(self):
        # ===== LAYOUT MODIFICATION START: make middle row the main focus =====
        # Give the chat area and session panel more room.
        self.root.grid_columnconfigure(0, weight=4)
        self.root.grid_columnconfigure(1, weight=2)
        self.root.grid_rowconfigure(0, weight=0)   # header
        self.root.grid_rowconfigure(1, weight=1)   # main middle area
        self.root.grid_rowconfigure(2, weight=0)   # input area
        # ===== LAYOUT MODIFICATION END: make middle row the main focus =====

        self.header = ctk.CTkFrame(self.root, corner_radius=18, fg_color=self.card_fg)
        self.header.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="ew")
        self.header.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self.header,
            text="🎵 MoodTune",
            font=ctk.CTkFont(size=30, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=22, pady=(18, 4), sticky="w")

        self.subtitle_label = ctk.CTkLabel(
            self.header,
            text="Share your mood. Find music that fits.",
            font=ctk.CTkFont(size=15),
            text_color=self.secondary_text
        )
        self.subtitle_label.grid(row=1, column=0, padx=22, pady=(0, 6), sticky="w")

        self.status_label = ctk.CTkLabel(
            self.header,
            text="Status: Ready to listen",
            font=ctk.CTkFont(size=12),
            text_color="#a1a1aa"
        )
        self.status_label.grid(row=2, column=0, padx=22, pady=(0, 18), sticky="w")

        # ===== LAYOUT MODIFICATION START: larger, more central chat area =====
        # ===== HORIZONTAL SCROLL MODIFICATION START =====
        # Create a container frame for the chat area
        self.chat_container = ctk.CTkFrame(
            self.root,
            corner_radius=18,
            fg_color=self.card_fg
        )

        self.chat_container.grid(
            row=1,
            column=0,
            padx=(20, 10),
            pady=10,
            sticky="nsew"
        )

        self.chat_container.grid_rowconfigure(0, weight=1)
        self.chat_container.grid_columnconfigure(0, weight=1)

        # Create canvas
        self.chat_canvas = ctk.CTkCanvas(
            self.chat_container,
            bg=self.card_fg,
            highlightthickness=0
        )

        # Vertical scrollbar
        self.chat_scroll_y = ctk.CTkScrollbar(
            self.chat_container,
            orientation="vertical",
            command=self.chat_canvas.yview
        )

        # Horizontal scrollbar
        self.chat_scroll_x = ctk.CTkScrollbar(
            self.chat_container,
            orientation="horizontal",
            command=self.chat_canvas.xview
        )

        self.chat_canvas.configure(
            yscrollcommand=self.chat_scroll_y.set,
            xscrollcommand=self.chat_scroll_x.set
        )

        self.chat_scroll_y.grid(row=0, column=1, sticky="ns")
        self.chat_scroll_x.grid(row=1, column=0, sticky="ew")

        self.chat_canvas.grid(row=0, column=0, sticky="nsew")

        # Frame inside the canvas (this replaces the old chat_frame)
        self.chat_frame = ctk.CTkFrame(
            self.chat_canvas,
            fg_color=self.card_fg
        )

        self.chat_frame.grid_columnconfigure(0, weight=1)

        # Create window inside canvas
        self.chat_window = self.chat_canvas.create_window(
            (0, 0),
            window=self.chat_frame,
            anchor="nw"
        )

        # Update scroll region when content changes
        def update_scroll_region(event):
            self.chat_canvas.configure(
                scrollregion=self.chat_canvas.bbox("all")
            )

        self.chat_frame.bind("<Configure>", update_scroll_region)
        # ===== LAYOUT MODIFICATION END: larger, more central chat area =====

        self.add_message(
            "MoodTune",
            "Hi! I’m here to help you process your feelings through music.\n\n"
            "Tell me how you’re feeling, and I’ll suggest tracks that match your mood.",
            is_user=False,
            bubble_type="bot"
        )

        # ===== LAYOUT MODIFICATION START: make Current Session panel scrollable =====
        self.side_panel = ctk.CTkScrollableFrame(
            self.root,
            corner_radius=18,
            fg_color=self.info_card_fg
        )
        self.side_panel.grid(row=1, column=1, padx=(10, 20), pady=10, sticky="nsew")
        self.side_panel.grid_columnconfigure(0, weight=1)
        # ===== LAYOUT MODIFICATION END: make Current Session panel scrollable =====

        # ===== VISUAL MODIFICATION START: stronger Current Session section =====
        self.session_title = ctk.CTkLabel(
            self.side_panel,
            text="Current Session",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.session_title.grid(row=0, column=0, padx=18, pady=(18, 12), sticky="w")
        # ===== VISUAL MODIFICATION END: stronger Current Session section =====

        # ===== VISUAL MODIFICATION START: nicer session summary card =====
        self.mood_card = ctk.CTkFrame(
            self.side_panel,
            corner_radius=16,
            fg_color=self.subcard_fg
        )
        self.mood_card.grid(row=1, column=0, padx=18, pady=8, sticky="ew")

        self.mood_label = ctk.CTkLabel(
            self.mood_card,
            text="Mood: Not analyzed yet",
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.mood_label.grid(row=0, column=0, padx=16, pady=(14, 6), sticky="w")

        self.song_label = ctk.CTkLabel(
            self.mood_card,
            text="Top song: None yet",
            font=ctk.CTkFont(size=13),
            text_color=self.secondary_text,
            justify="left",
            wraplength=280
        )
        self.song_label.grid(row=1, column=0, padx=16, pady=(0, 14), sticky="w")
        # ===== VISUAL MODIFICATION END: nicer session summary card =====

        # ===== VISUAL MODIFICATION START: session stats / details card =====
        self.details_card = ctk.CTkFrame(
            self.side_panel,
            corner_radius=16,
            fg_color=self.subcard_fg
        )
        self.details_card.grid(row=2, column=0, padx=18, pady=8, sticky="ew")

        self.details_title = ctk.CTkLabel(
            self.details_card,
            text="Session Details",
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.details_title.grid(row=0, column=0, padx=16, pady=(14, 8), sticky="w")

        self.details_text = ctk.CTkLabel(
            self.details_card,
            text="No recommendations yet.\nYour most recent mood and top track will appear here.",
            justify="left",
            wraplength=280,
            text_color=self.secondary_text,
            font=ctk.CTkFont(size=13)
        )
        self.details_text.grid(row=1, column=0, padx=16, pady=(0, 14), sticky="w")
        # ===== VISUAL MODIFICATION END: session stats / details card =====

        # ===== VISUAL MODIFICATION START: simplified helpful info card =====
        self.instructions_card = ctk.CTkFrame(
            self.side_panel,
            corner_radius=16,
            fg_color=self.subcard_fg
        )
        self.instructions_card.grid(row=3, column=0, padx=18, pady=8, sticky="ew")

        self.instructions_title = ctk.CTkLabel(
            self.instructions_card,
            text="How it works",
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.instructions_title.grid(row=0, column=0, padx=16, pady=(14, 8), sticky="w")

        self.instructions_text = ctk.CTkLabel(
            self.instructions_card,
            text="1. Share how you feel\n2. MoodTune analyzes your mood\n3. Click any suggested track to open it in Spotify",
            justify="left",
            wraplength=280,
            text_color=self.secondary_text,
            font=ctk.CTkFont(size=13)
        )
        self.instructions_text.grid(row=1, column=0, padx=16, pady=(0, 14), sticky="w")
        # ===== VISUAL MODIFICATION END: simplified helpful info card =====

        # ===== LAYOUT MODIFICATION START: smaller bottom input area =====
        self.bottom_frame = ctk.CTkFrame(self.root, corner_radius=18, fg_color=self.card_fg)
        self.bottom_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(1, weight=0)

        self.input_label = ctk.CTkLabel(
            self.bottom_frame,
            text="How are you feeling?",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.input_label.grid(row=0, column=0, padx=16, pady=(12, 0), sticky="w")

        # Smaller textbox so it doesn't crowd the middle area
        self.input_box = ctk.CTkTextbox(
            self.bottom_frame,
            height=70,
            corner_radius=14,
            fg_color="#2b2b34"
        )
        self.input_box.grid(row=1, column=0, columnspan=2, padx=16, pady=(8, 10), sticky="ew")
        # ===== LAYOUT MODIFICATION END: smaller bottom input area =====

        self.send_button = ctk.CTkButton(
            self.bottom_frame,
            text="Find My Music",
            width=155,
            height=42,
            corner_radius=16,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#4f46e5",
            hover_color="#4338ca",
            command=self.send_message
        )
        self.send_button.grid(row=2, column=1, padx=16, pady=(0, 14), sticky="e")

    def mood_colors(self, mood_summary: str):
        return {
            "window": "#18181b",
            "card": "#232329",
            "bot": "#31313a",
            "user": "#4f46e5",
            "system": "#475569",
            "info": "#202028"
        }

    def apply_mood_theme(self, mood_summary: str):
        colors = self.mood_colors(mood_summary)

        self.window_fg = colors["window"]
        self.card_fg = colors["card"]
        self.bot_bubble_fg = colors["bot"]
        self.user_bubble_fg = colors["user"]
        self.system_bubble_fg = colors["system"]
        self.info_card_fg = colors["info"]

        self.root.configure(fg_color=self.window_fg)
        self.header.configure(fg_color=self.card_fg)
        self.chat_frame.configure(fg_color=self.card_fg)
        self.bottom_frame.configure(fg_color=self.card_fg)
        self.side_panel.configure(fg_color=self.info_card_fg)

    def add_message(self, sender: str, text: str, is_user: bool, bubble_type="bot"):
        outer = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        outer.grid(sticky="ew", padx=12, pady=12)
        outer.grid_columnconfigure(0, weight=1)

        anchor = "e" if is_user else "w"

        if bubble_type == "user":
            bubble_color = self.user_bubble_fg
        elif bubble_type == "system":
            bubble_color = self.system_bubble_fg
        else:
            bubble_color = self.bot_bubble_fg

        name_label = ctk.CTkLabel(
            outer,
            text=sender,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#d4d4d8"
        )
        name_label.grid(row=0, column=0, sticky=anchor, padx=12, pady=(0, 4))

        bubble = ctk.CTkFrame(
            outer,
            corner_radius=18,
            fg_color=bubble_color
        )
        bubble.grid(row=1, column=0, sticky=anchor, padx=12)

        message = ctk.CTkLabel(
            bubble,
            text=text,
            text_color="white",
            justify="left",
            wraplength=620,
            font=ctk.CTkFont(size=14)
        )
        message.grid(row=0, column=0, padx=18, pady=14)

    def add_track_buttons(self, tracks: list):
        """
        Create one clickable button per track.
        Clicking a button opens that track in Spotify.
        """
        if not tracks:
            return

        outer = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        outer.grid(sticky="ew", padx=12, pady=(0, 12))
        outer.grid_columnconfigure(0, weight=1)

        container = ctk.CTkFrame(
            outer,
            corner_radius=18,
            fg_color=self.bot_bubble_fg
        )
        container.grid(row=0, column=0, sticky="w", padx=12)

        tracks_label = ctk.CTkLabel(
            container,
            text="Suggested Tracks",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="white"
        )
        tracks_label.grid(row=0, column=0, padx=14, pady=(12, 8), sticky="w")

        for index, track in enumerate(tracks, start=1):
            title = track.get("title", "Unknown title")
            artist = track.get("artist", "Unknown artist")
            spotify_url = track.get("spotify_url")

            track_button = ctk.CTkButton(
                container,
                text=f"🎵  {index}. {title} — {artist}",
                width=440,
                height=42,
                anchor="w",
                corner_radius=14,
                fg_color=self.track_button_fg,
                hover_color=self.track_button_hover,
                font=ctk.CTkFont(size=13),
                command=lambda url=spotify_url: self.open_song(url)
            )
            track_button.grid(row=index, column=0, padx=14, pady=8, sticky="w")

    def open_song(self, url: str | None):
        if not url:
            messagebox.showerror("Missing URL", "No song URL was returned by the backend.")
            return
        webbrowser.open(url)

    def update_session_panel(self, mood_summary: str, song_text: str):
        self.mood_label.configure(text=f"Mood: {mood_summary}")
        self.song_label.configure(text=f"Top song: {song_text}")

        # ===== VISUAL MODIFICATION START: richer details in Current Session =====
        self.details_text.configure(
            text=(
                f"Latest mood analysis:\n{mood_summary}\n\n"
                f"Top recommendation:\n{song_text}\n\n"
                f"You can scroll this panel if more content appears."
            )
        )
        # ===== VISUAL MODIFICATION END: richer details in Current Session =====

    def set_status(self, text: str):
        self.status_label.configure(text=f"Status: {text}")

    def send_message(self):
        user_text = self.input_box.get("1.0", "end").strip()

        if not user_text:
            messagebox.showwarning("Input missing", "Please type how you feel.")
            return

        self.add_message("You", user_text, is_user=True, bubble_type="user")
        self.input_box.delete("1.0", "end")

        self.send_button.configure(state="disabled", text="Finding...")
        self.set_status("Analyzing your mood...")

        def worker():
            try:
                result = handle_chat(user_text)

                recommendation = result.get("recommendation", {})
                tracks = result.get("tracks", [])

                reply = recommendation.get("response_text", "No reply received.")
                mood_summary = recommendation.get("mood_summary", "Unknown mood")

                bot_text = f"{reply}\n\nMood summary: {mood_summary}"

                if tracks:
                    first_track = tracks[0]
                    song_title = first_track.get("title", "Unknown title")
                    song_artist = first_track.get("artist", "Unknown artist")
                    song_text = f"{song_title} — {song_artist}"
                    bot_text += f"\n\nTop recommendation: {song_text}"
                else:
                    song_text = "No song found"

                self.root.after(0, lambda: self.apply_mood_theme(mood_summary))
                self.root.after(0, lambda: self.update_session_panel(mood_summary, song_text))
                self.root.after(0, lambda: self.add_message("MoodTune", bot_text, is_user=False, bubble_type="bot"))
                self.root.after(0, lambda: self.send_button.configure(state="normal", text="Find My Music"))
                self.root.after(0, lambda: self.set_status("Ready"))

                if tracks:
                    self.root.after(0, lambda: self.add_track_buttons(tracks))
                else:
                    self.root.after(
                        0,
                        lambda: messagebox.showinfo(
                            "No tracks found",
                            "The backend returned no Spotify tracks."
                        )
                    )

            except requests.exceptions.ConnectionError:
                self.root.after(
                    0,
                    lambda: messagebox.showerror(
                        "Backend not reachable",
                        "Could not connect to the backend.\n\n"
                        "Make sure your teammate's FastAPI server is running."
                    )
                )
                self.root.after(0, lambda: self.send_button.configure(state="normal", text="Find My Music"))
                self.root.after(0, lambda: self.set_status("Backend not reachable"))

            except requests.exceptions.HTTPError as e:
                self.root.after(0, lambda: messagebox.showerror("Backend error", str(e)))
                self.root.after(0, lambda: self.send_button.configure(state="normal", text="Find My Music"))
                self.root.after(0, lambda: self.set_status("Backend error"))

            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
                self.root.after(0, lambda: self.send_button.configure(state="normal", text="Find My Music"))
                self.root.after(0, lambda: self.set_status("Something went wrong"))

        threading.Thread(target=worker, daemon=True).start()

    def run(self):
        self.root.mainloop()
