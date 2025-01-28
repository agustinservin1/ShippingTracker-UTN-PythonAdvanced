import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
from src.utils.logging.log_server import LogServer
from datetime import datetime

class LogServerGUI:
    def __init__(self):
        self.server = None
        self.server_thread = None
        self.log_position = 0

        self.window = tk.Tk()
        self.window.title("Log Server Controller")
        self.window.geometry("800x500")

        control_frame = ttk.Frame(self.window)
        control_frame.pack(pady=10, fill=tk.X)

        self.start_button = ttk.Button(
            control_frame, 
            text="▶ Start Server", 
            command=self.start_server
        )
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(
            control_frame, 
            text="⏹ Stop Server", 
            command=self.stop_server, 
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.log_area = scrolledtext.ScrolledText(
            self.window, 
            wrap=tk.WORD,
            state='disabled',  
            font=("Consolas", 10)  
        )
        self.log_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.status_label = ttk.Label(
            self.window, 
            text="Status: Stopped", 
            foreground="red",
            font=("Arial", 10, "bold")
        )
        self.status_label.pack(side=tk.BOTTOM, pady=5)

    def start_server(self):
        """Starts the server and begins monitoring the logs."""
        if not self.server:
            self.server = LogServer()
            self.server_thread = threading.Thread(
                target=self._run_server, 
                daemon=True
            )
            self.server_thread.start()

            self._update_ui("running")
            self._log_message("INFO - Server started on {}:{}".format(
                self.server.host, 
                self.server.port
            ))
            self._update_logs()

    def _run_server(self):
        """Handles the server execution in a separate thread."""
        try:
            self.server.start()
        except Exception as e:
            self._log_message(f"ERROR - {str(e)}")
        finally:
            self.stop_server()

    def stop_server(self):
        """Stops the server and cleans up resources."""
        if self.server:
            self.server.stop()
            self._log_message("INFO - Server stopped")
            self._update_ui("stopped")
            self.server = None

    def _update_ui(self, state: str):
        """Updates the UI based on the server's state."""
        if state == "running":
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_label.config(text="Status: Running", foreground="green")
        else:
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.status_label.config(text="Status: Stopped", foreground="red")

    def _log_message(self, message: str):
        """Adds a message to the log area."""
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
        self.log_area.config(state='disabled')
        self.log_area.see(tk.END)

    def _update_logs(self):
        """Reads and displays new logs from the log file."""
        if self.server and self.server.running:
            try:
                with open(self.server.log_file, "r") as log_file:
                    log_file.seek(self.log_position)
                    new_logs = log_file.read()

                    if new_logs:
                        self._log_message(new_logs)
                        self.log_position = log_file.tell()
            except FileNotFoundError:
                self._log_message("ERROR - Log file not found")
            except Exception as e:
                self._log_message(f"ERROR - Failed to load logs: {str(e)}")

            self.window.after(2000, self._update_logs)

    def run(self):
        """Starts the application."""
        self.window.mainloop()

if __name__ == "__main__":
    gui = LogServerGUI()
    gui.run()
