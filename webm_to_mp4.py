import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading
import subprocess
from pathlib import Path
import sys

def show_error(exc_type, exc_value, exc_traceback):
    """Affiche les erreurs dans une boîte de dialogue"""
    import traceback
    error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print(f"ERREUR: {error_msg}")
    
    try:
        messagebox.showerror('Erreur de l\'application', error_msg)
    except:
        pass

# Rediriction
sys.excepthook = show_error

class WebmToMp4Converter:
    def __init__(self, root):
        self.root = root
        self.root.title("Convertisseur WebM vers MP4")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        self.bg_color = "#f5f5f5"
        self.accent_color = "#3498db"
        self.text_color = "#2c3e50"
        
        self.root.configure(bg=self.bg_color)
        
        print("Initialisation de l'interface...")
        
        self.setup_ui()
        self.files_to_convert = []
        self.conversion_in_progress = False
        
        print("Interface initialisée avec succès")
    
    def setup_ui(self):
        title_label = tk.Label(
            self.root, 
            text="Convertisseur WebM vers MP4", 
            font=("Helvetica", 18, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        title_label.pack(pady=20)
        
        file_frame = tk.Frame(self.root, bg=self.bg_color)
        file_frame.pack(fill="x", padx=20)
        
        self.file_label = tk.Label(
            file_frame,
            text="Aucun fichier sélectionné",
            bg=self.bg_color,
            fg=self.text_color,
            width=40,
            anchor="w"
        )
        self.file_label.pack(side="left", pady=10)
        
        select_btn = tk.Button(
            file_frame,
            text="Sélectionner fichiers",
            command=self.select_files,
            bg=self.accent_color,
            fg="white",
            bd=0,
            padx=10,
            pady=5
        )
        select_btn.pack(side="right", pady=10)
        
        dir_frame = tk.Frame(self.root, bg=self.bg_color)
        dir_frame.pack(fill="x", padx=20)
        
        self.output_dir = os.path.expanduser("~/Videos")
        
        self.dir_label = tk.Label(
            dir_frame,
            text=f"Répertoire de sortie: {self.output_dir}",
            bg=self.bg_color,
            fg=self.text_color,
            width=40,
            anchor="w"
        )
        self.dir_label.pack(side="left", pady=10)
        
        dir_btn = tk.Button(
            dir_frame,
            text="Changer répertoire",
            command=self.select_output_dir,
            bg=self.accent_color,
            fg="white",
            bd=0,
            padx=10,
            pady=5
        )
        dir_btn.pack(side="right", pady=10)
        
        # Cadre de progression
        progress_frame = tk.Frame(self.root, bg=self.bg_color)
        progress_frame.pack(fill="x", padx=20, pady=10)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            length=560
        )
        self.progress_bar.pack(pady=10)
        
        self.status_label = tk.Label(
            progress_frame,
            text="Prêt",
            bg=self.bg_color,
            fg=self.text_color
        )
        self.status_label.pack(pady=5)
        
        self.convert_btn = tk.Button(
            self.root,
            text="Convertir",
            command=self.start_conversion,
            bg=self.accent_color,
            fg="white",
            bd=0,
            padx=20,
            pady=10,
            font=("Helvetica", 12, "bold")
        )
        self.convert_btn.pack(pady=20)
        
        self.ffmpeg_status = tk.Label(
            self.root,
            text="",
            bg=self.bg_color,
            fg=self.text_color,
            font=("Helvetica", 10)
        )
        self.ffmpeg_status.pack(pady=5)
        
        self.check_ffmpeg()
    
    def check_ffmpeg(self):
        """Vérifier si FFmpeg est installé et disponible dans PATH"""
        try:
            print("Vérification de FFmpeg...")
            subprocess.run(
                ["ffmpeg", "-version"], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                check=True
            )
            self.ffmpeg_status.config(
                text="✓ FFmpeg détecté",
                fg="green"
            )
            print("FFmpeg trouvé")
            return True
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            print(f"Erreur FFmpeg: {str(e)}")
            self.ffmpeg_status.config(
                text="❌ FFmpeg non trouvé. Veuillez installer FFmpeg pour utiliser cette application.",
                fg="red"
            )
            self.convert_btn.config(state="disabled")
            return False
    
    def select_files(self):
        """Ouvrir une boîte de dialogue pour sélectionner des fichiers WebM"""
        filetypes = [("Fichiers WebM", "*.webm")]
        files = filedialog.askopenfilenames(
            title="Sélectionner des fichiers WebM",
            filetypes=filetypes
        )
        
        if files:
            self.files_to_convert = list(files)
            if len(self.files_to_convert) == 1:
                self.file_label.config(
                    text=f"1 fichier sélectionné: {os.path.basename(self.files_to_convert[0])}"
                )
            else:
                self.file_label.config(
                    text=f"{len(self.files_to_convert)} fichiers sélectionnés"
                )
    
    def select_output_dir(self):
        """Ouvrir une boîte de dialogue pour sélectionner le répertoire de sortie"""
        directory = filedialog.askdirectory(
            title="Sélectionner le répertoire de sortie",
            initialdir=self.output_dir
        )
        
        if directory:
            self.output_dir = directory
            self.dir_label.config(text=f"Répertoire de sortie: {self.output_dir}")
    
    def start_conversion(self):
        """Démarrer le processus de conversion dans un thread séparé"""
        if not self.files_to_convert:
            messagebox.showinfo("Aucun fichier", "Veuillez sélectionner des fichiers WebM à convertir.")
            return
        
        if self.conversion_in_progress:
            messagebox.showinfo("En cours", "La conversion est déjà en cours.")
            return
        
        self.convert_btn.config(state="disabled")
        self.conversion_in_progress = True
        
        conversion_thread = threading.Thread(target=self.convert_files)
        conversion_thread.daemon = True
        conversion_thread.start()
    
    def convert_files(self):
        """Convertir tous les fichiers WebM sélectionnés en MP4"""
        total_files = len(self.files_to_convert)
        
        for i, file_path in enumerate(self.files_to_convert):
            file_name = os.path.basename(file_path)
            self.update_status(f"Conversion {i+1}/{total_files}: {file_name}")
            
            progress = (i / total_files) * 100
            self.progress_var.set(progress)
            
            output_file = os.path.join(
                self.output_dir,
                f"{Path(file_name).stem}.mp4"
            )
            
            try:
                result = subprocess.run(
                    [
                        "ffmpeg",
                        "-i", file_path,
                        "-c:v", "libx264",
                        "-crf", "23",
                        "-preset", "medium",
                        "-c:a", "aac",
                        "-b:a", "128k",
                        "-y",  # ecraser file s'il existe
                        output_file
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                
                if result.returncode != 0:
                    self.update_status(f"Erreur lors de la conversion de {file_name}: {result.stderr.decode()}")
            except Exception as e:
                self.update_status(f"Erreur: {str(e)}")
        
        self.progress_var.set(100)
        self.update_status(f"Conversion terminée! {total_files} fichiers convertis.")
        self.conversion_in_progress = False
        self.convert_btn.config(state="normal")
        
        self.root.after(100, lambda: messagebox.showinfo(
            "Conversion terminée",
            f"Conversion réussie de {total_files} fichiers au format MP4."
        ))
    
    def update_status(self, message):
        """Mettre à jour l'étiquette de statut depuis n'importe quel thread"""
        self.root.after(0, lambda: self.status_label.config(text=message))


def main():
    print("Démarrage de l'application...")
    try:
        root = tk.Tk()
        app = WebmToMp4Converter(root)
        print("Lancement de la boucle principale...")
        root.mainloop()
        print("Application terminée")
        return True
    except Exception as e:
        print(f"ERREUR CRITIQUE: {str(e)}")
        return False


if __name__ == "__main__":
    success = main()
    if not success:
        print("L'application a rencontré des erreurs critiques et s'est terminée.")