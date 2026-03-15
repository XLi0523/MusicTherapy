import customtkinter as ctk
import threading
import webbrowser
import requests
from tkinter import messagebox


# ===== MODIFICATION START: backend API connection settings =====
# This is the URL of your teammate's FastAPI backend.
# Change the port if your teammate runs it on a different one.
BACKEND_URL = "http://127.0.0.1:8000"
# ===== MODIFICATION END: backend API connection settings =====


# ===== MODIFICATION START: replace fake handle_chat with real API call =====
def handle_chat(user_text: str):
    """
    Send the user's message to the backend API and return the JSON result.
    The backend returns a dictionary like:
    {
        "mood_input": {...},
        "recommendation": {...},
        "tracks": [...]
    }
    """
    response = requests.post(
        f"{BACKEND_URL}/recommend",
        json={"message": user_text},
        timeout=15
    )

    # If the backend returns an error status, raise an exception
    response.raise_for_status()

    # Convert the backend JSON response into a Python dictionary
    return response.json()
# ===== MODIFICATION END: replace fake handle_chat with real API call =====


class MusicTherapyUI:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()

        # ===== MODIFICATION START: stronger branding and window size =====
        self.root.title("MoodTune")
        self.root.geometry("1100x720")
        self.root.minsize(900, 650)
        # ===== MODIFICATION END: stronger branding and window size =====

        # ===== MODIFICATION START: neutral dark palette for readability =====
        self.window_fg = "#18181b"
        self.card_fg = "#232329"
        self.bot_bubble_fg = "#2f2f36"
        self.user_bubble_fg = "#4f46e5"
        self.system_bubble_fg = "#334155"
        self.secondary_text = "#cbd5e1"
        self.info_card_fg = "#202028"
        # ===== MODIFICATION END: neutral dark palette for readability =====

        self.root.configure(fg_color=self.window_fg)

        self.build_ui()

    def build_ui(self):
        # ===== MODIFICATION START: two-column layout =====
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        # ===== MODIFICATION END: two-column layout =====

        # ===== MODIFICATION START: improved header =====
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
            text="Talk about how you feel and get music that meets you there.",
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
        # ===== MODIFICATION END: improved header =====

        # ===== MODIFICATION START: styled chat area =====
        self.chat_frame = ctk.CTkScrollableFrame(
            self.root,
            corner_radius=18,
            fg_color=self.card_fg
        )
        self.chat_frame.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="nsew")
        self.chat_frame.grid_columnconfigure(0, weight=1)
        # ===== MODIFICATION END: styled chat area =====

        # ===== MODIFICATION START: welcome state =====
        self.add_message(
            "MoodTune",
            "Hi! I’m here to help you process your feelings through music.\n\n"
            "Tell me how you’re feeling, and I’ll suggest tracks that matches your mood.",
            is_user=False,
            bubble_type="bot"
        )
        # ===== MODIFICATION END: welcome state =====

        # ===== MODIFICATION START: side panel =====
        self.side_panel = ctk.CTkFrame(self.root, corner_radius=18, fg_color=self.info_card_fg)
        self.side_panel.grid(row=1, column=1, padx=(10, 20), pady=10, sticky="nsew")
        self.side_panel.grid_columnconfigure(0, weight=1)

        self.session_title = ctk.CTkLabel(
            self.side_panel,
            text="Current Session",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.session_title.grid(row=0, column=0, padx=18, pady=(18, 10), sticky="w")

        self.mood_card = ctk.CTkFrame(self.side_panel, corner_radius=14, fg_color="#2a2a33")
        self.mood_card.grid(row=1, column=0, padx=18, pady=8, sticky="ew")

        self.mood_label = ctk.CTkLabel(
            self.mood_card,
            text="Mood: Not analyzed yet",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.mood_label.grid(row=0, column=0, padx=14, pady=(12, 4), sticky="w")

        self.song_label = ctk.CTkLabel(
            self.mood_card,
            text="Song: None yet",
            font=ctk.CTkFont(size=13),
            text_color=self.secondary_text,
            justify="left",
            wraplength=240
        )
        self.song_label.grid(row=1, column=0, padx=14, pady=(0, 12), sticky="w")

        self.instructions_card = ctk.CTkFrame(self.side_panel, corner_radius=14, fg_color="#2a2a33")
        self.instructions_card.grid(row=2, column=0, padx=18, pady=8, sticky="ew")

        self.instructions_title = ctk.CTkLabel(
            self.instructions_card,
            text="How it works",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.instructions_title.grid(row=0, column=0, padx=14, pady=(12, 6), sticky="w")

        self.instructions_text = ctk.CTkLabel(
            self.instructions_card,
            text="1. Share how you feel\n2. MoodTune analyzes your mood\n3. A matching Spotify song opens",
            justify="left",
            wraplength=240,
            text_color=self.secondary_text,
            font=ctk.CTkFont(size=13)
        )
        self.instructions_text.grid(row=1, column=0, padx=14, pady=(0, 12), sticky="w")
        # ===== MODIFICATION END: side panel =====

        # ===== MODIFICATION START: improved bottom input area =====
        self.bottom_frame = ctk.CTkFrame(self.root, corner_radius=18, fg_color=self.card_fg)
        self.bottom_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(1, weight=0)

        self.input_label = ctk.CTkLabel(
            self.bottom_frame,
            text="How are you feeling right now?",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.input_label.grid(row=0, column=0, padx=16, pady=(14, 0), sticky="w")

        self.input_box = ctk.CTkTextbox(
            self.bottom_frame,
            height=95,
            corner_radius=14,
            fg_color="#2b2b34"
        )
        self.input_box.grid(row=1, column=0, columnspan=2, padx=16, pady=(8, 12), sticky="ew")
        # ===== MODIFICATION END: improved bottom input area =====

        # ===== MODIFICATION START: better send button =====
        self.send_button = ctk.CTkButton(
            self.bottom_frame,
            text="Find My Music",
            width=155,
            height=44,
            corner_radius=16,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#4f46e5",
            hover_color="#4338ca",
            command=self.send_message
        )
        self.send_button.grid(row=2, column=1, padx=16, pady=(0, 16), sticky="e")
        # ===== MODIFICATION END: better send button =====

    # ===== MODIFICATION START: simpler neutral mood colors =====
    # Since you said the previous shifting colors were hard to read,
    # this returns one calm readable palette for all moods.
    def mood_colors(self, mood_summary: str):
        return {
            "window": "#18181b",
            "card": "#232329",
            "bot": "#2f2f36",
            "user": "#4f46e5",
            "system": "#334155",
            "info": "#202028"
        }
    # ===== MODIFICATION END: simpler neutral mood colors =====

    # ===== MODIFICATION START: apply colors to the main widgets =====
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
    # ===== MODIFICATION END: apply colors to the main widgets =====

    # ===== MODIFICATION START: styled message bubbles =====
    def add_message(self, sender: str, text: str, is_user: bool, bubble_type="bot"):
        outer = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        outer.grid(sticky="ew", padx=12, pady=10)
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
        message.grid(row=0, column=0, padx=16, pady=12)
    # ===== MODIFICATION END: styled message bubbles =====
    # ===== NEW MODIFICATION START: add clickable buttons for returned tracks =====
    def add_track_buttons(self, tracks: list):
        """
        Create one clickable button per track.
        Clicking a button opens that track in Spotify.
        """
        if not tracks:
            return

        outer = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        outer.grid(sticky="ew", padx=12, pady=(0, 10))
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
                text=f"{index}. {title} — {artist}",
                width=440,
                anchor="w",
                corner_radius=12,
                fg_color="#3b3b46",
                hover_color="#4b4b58",
                command=lambda url=spotify_url: self.open_song(url)
            )
            track_button.grid(row=index, column=0, padx=14, pady=6, sticky="w")
    # ===== NEW MODIFICATION END: add clickable buttons for returned tracks =====

    def open_song(self, url: str | None):
        if not url:
            messagebox.showerror("Missing URL", "No song URL was returned by the backend.")
            return
        webbrowser.open(url)

    # ===== MODIFICATION START: helper to update side session info =====
    def update_session_panel(self, mood_summary: str, song_text: str):
        self.mood_label.configure(text=f"Mood: {mood_summary}")
        self.song_label.configure(text=f"Song: {song_text}")
    # ===== MODIFICATION END: helper to update side session info =====

    # ===== MODIFICATION START: helper to update status label =====
    def set_status(self, text: str):
        self.status_label.configure(text=f"Status: {text}")
    # ===== MODIFICATION END: helper to update status label =====

    def send_message(self):
        user_text = self.input_box.get("1.0", "end").strip()

        if not user_text:
            messagebox.showwarning("Input missing", "Please type how you feel.")
            return

        # ===== MODIFICATION START: styled user message =====
        self.add_message("You", user_text, is_user=True, bubble_type="user")
        # ===== MODIFICATION END: styled user message =====

        self.input_box.delete("1.0", "end")

        # ===== MODIFICATION START: better loading feedback =====
        self.send_button.configure(state="disabled", text="Finding...")
        self.set_status("Analyzing your mood...")
        # ===== MODIFICATION END: better loading feedback =====

        def worker():
            try:
                # ===== MODIFICATION START: call real backend API =====
                result = handle_chat(user_text)
                # result is a dictionary because FastAPI returned JSON
                # ===== MODIFICATION END: call real backend API =====

                # ===== MODIFICATION START: read backend JSON structure =====
                recommendation = result.get("recommendation", {})
                tracks = result.get("tracks", [])

                reply = recommendation.get("response_text", "No reply received.")
                mood_summary = recommendation.get("mood_summary", "Unknown mood")
                # ===== MODIFICATION END: read backend JSON structure =====

                bot_text = f"{reply}\n\nMood summary: {mood_summary}"

                if tracks:
                    first_track = tracks[0]
                    song_title = first_track.get("title", "Unknown title")
                    song_artist = first_track.get("artist", "Unknown artist")
                    song_text = f"{song_title} — {song_artist}"
                    bot_text += f"\n\nRecommended song: {song_text}"
                else:
                    song_text = "No song found"

                # ===== MODIFICATION START: update UI after backend response =====
                self.root.after(0, lambda: self.apply_mood_theme(mood_summary))
                self.root.after(0, lambda: self.update_session_panel(mood_summary, song_text))
                self.root.after(0, lambda: self.add_message("MoodTune", bot_text, is_user=False, bubble_type="bot"))
                self.root.after(0, lambda: self.send_button.configure(state="normal", text="Find My Music"))
                self.root.after(0, lambda: self.set_status("Ready"))
                # ===== MODIFICATION END: update UI after backend response =====

                # ===== NEW MODIFICATION START: show track buttons instead of auto-opening one song =====
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
                # ===== NEW MODIFICATION END: show track buttons instead of auto-opening one song =====

            except requests.exceptions.ConnectionError:
                # ===== MODIFICATION START: backend not running error =====
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
                # ===== MODIFICATION END: backend not running error =====

            except requests.exceptions.HTTPError as e:
                # ===== MODIFICATION START: backend returned HTTP error =====
                self.root.after(0, lambda: messagebox.showerror("Backend error", str(e)))
                self.root.after(0, lambda: self.send_button.configure(state="normal", text="Find My Music"))
                self.root.after(0, lambda: self.set_status("Backend error"))
                # ===== MODIFICATION END: backend returned HTTP error =====

            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
                self.root.after(0, lambda: self.send_button.configure(state="normal", text="Find My Music"))
                self.root.after(0, lambda: self.set_status("Something went wrong"))

        threading.Thread(target=worker, daemon=True).start()

    def run(self):
        self.root.mainloop()
