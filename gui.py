import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip  

# import file dari twofish_encryption
from twofish_encryption import gen_keys, encrypt_message, decrypt_message, text2num

class TwofishGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Twofish Encryption")
        self.root.geometry("700x600")
        
        # Inisialisasi kunci enkripsi dan parameter
        self.key = 'VkYp3s6v9y$B&E(H+MbQeThWmZq4t7w!'
        self.N = 128
        self.rounds = 16
        self.show_key = False  
        
        [self.K, self.S] = gen_keys(self.key, self.N, self.rounds)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Bingkai kunci
        key_frame = ttk.LabelFrame(self.root, text="Encryption Key", padding="10")
        key_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(key_frame, text="Key:").pack(side="left")
        self.key_entry = ttk.Entry(key_frame, width=50, show="*")
        self.key_entry.pack(side="left", padx=5)
        self.key_entry.insert(0, self.key)
        
        # Tombol Tampilkan/Sembunyikan Kunci
        self.show_key_btn = ttk.Button(key_frame, text="Show Key", command=self.toggle_key_visibility)
        self.show_key_btn.pack(side="left", padx=5)
        
        ttk.Button(key_frame, text="Update Key", command=self.update_key).pack(side="left", padx=5)
        
        # Bingkai Info Kunci
        self.key_info_frame = ttk.LabelFrame(self.root, text="Key Information", padding="10")
        self.key_info_frame.pack(fill="x", padx=10, pady=5)
        
        # Label informasi utama
        key_info_text = f"Key Length: {self.N} bits\nRounds: {self.rounds}"
        self.key_info_label = ttk.Label(self.key_info_frame, text=key_info_text)
        self.key_info_label.pack(fill="x")
        
        # Input Frame
        input_frame = ttk.LabelFrame(self.root, text="Input", padding="10")
        input_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.input_text = tk.Text(input_frame, height=6)
        self.input_text.pack(fill="both", expand=True)
        
        # Buttons Frame
        buttons_frame = ttk.Frame(self.root, padding="10")
        buttons_frame.pack(fill="x", padx=10)
        
        ttk.Button(buttons_frame, text="Encrypt", command=self.encrypt).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Decrypt", command=self.decrypt).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Clear", command=self.clear).pack(side="left", padx=5)
        
        # Output Frame
        output_frame = ttk.LabelFrame(self.root, text="Output", padding="10")
        output_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.output_text = tk.Text(output_frame, height=6)
        self.output_text.pack(fill="both", expand=True)
        
        # Copy Button Frame
        copy_frame = ttk.Frame(self.root, padding="10")
        copy_frame.pack(fill="x", padx=10)
        
        ttk.Button(copy_frame, text="Copy Output", command=self.copy_output).pack(side="left", padx=5)
    
    def toggle_key_visibility(self):
        self.show_key = not self.show_key
        if self.show_key:
            self.key_entry.config(show="")
            self.show_key_btn.config(text="Hide Key")
        else:
            self.key_entry.config(show="*")
            self.show_key_btn.config(text="Show Key")
    
    def update_key(self):
        new_key = self.key_entry.get()
        if new_key:
            try:
                [self.K, self.S] = gen_keys(new_key, self.N, self.rounds)
                self.key = new_key
                # Update key information display
                key_info_text = f"Key Length: {self.N} bits\nRounds: {self.rounds}"
                self.key_info_label.config(text=key_info_text)
                messagebox.showinfo("Success", "Key updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update key: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Please enter a key")
    
    def encrypt(self):
        try:
            text = self.input_text.get("1.0", "end-1c")
            if not text:
                messagebox.showwarning("Warning", "Please enter text to encrypt")
                return
                
            [num_C, cipher_text] = encrypt_message(text, self.S, self.K, self.rounds)
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", cipher_text)
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {str(e)}")
    
    def decrypt(self):
        try:
            text = self.input_text.get("1.0", "end-1c")
            if not text:
                messagebox.showwarning("Warning", "Please enter text to decrypt")
                return
                
            message_num = text2num(text)
            plain_text = decrypt_message(message_num, self.S, self.K, self.rounds)
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", plain_text)
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {str(e)}")
    
    def clear(self):
        self.input_text.delete("1.0", "end")
        self.output_text.delete("1.0", "end")
    
    def copy_output(self):
        output = self.output_text.get("1.0", "end-1c")
        if output:
            pyperclip.copy(output)
            messagebox.showinfo("Success", "Output copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No output to copy")

if __name__ == "__main__":
    root = tk.Tk()
    app = TwofishGUI(root)
    root.mainloop()