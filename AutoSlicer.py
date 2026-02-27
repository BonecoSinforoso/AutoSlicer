import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
from scipy import ndimage

# ─── SETTINGS ──────────────────────────────────────────────
ALPHA_THRESHOLD = 32
PADDING         = 2
OUTPUT_DIR      = "sprites_output"
# ─────────────────────────────────────────────────────────

def load_mask(img: Image.Image) -> np.ndarray:
    rgba = img.convert("RGBA")
    a = np.array(rgba.getchannel("A"))

    if a.min() < 255:
        return a > ALPHA_THRESHOLD

    r = np.array(rgba.getchannel("R"))
    g = np.array(rgba.getchannel("G"))
    b = np.array(rgba.getchannel("B"))

    bg_r, bg_g, bg_b = int(r[0, 0]), int(g[0, 0]), int(b[0, 0])

    
    dist = np.sqrt((r.astype(np.int32) - bg_r) ** 2 +
                   (g.astype(np.int32) - bg_g) ** 2 +
                   (b.astype(np.int32) - bg_b) ** 2)
    
    return dist > 30


def slice_sprites(img: Image.Image, mask: np.ndarray, padding: int = PADDING):
    labeled, n = ndimage.label(mask)
    sprites = []

    for i in range(1, n + 1):
        ys, xs = np.where(labeled == i)
        x0 = max(xs.min() - padding, 0)
        y0 = max(ys.min() - padding, 0)
        x1 = min(xs.max() + padding + 1, img.width)
        y1 = min(ys.max() + padding + 1, img.height)
        sprites.append(img.crop((x0, y0, x1, y1)))

    return sprites


def save_sprites(sprites, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    paths = []

    for i, spr in enumerate(sprites):
        path = os.path.join(out_dir, f"sprite_{i:03d}.png")
        spr.save(path)
        paths.append(path)

    return paths


# ─── GUI ─────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Auto Slicer")
        self.resizable(False, False)
        self.img_path = None
        self.img      = None
        self.sprites  = []

        self.canvas = tk.Canvas(self, width=500, height=400, bg="#1e1e1e")
        self.canvas.pack(padx=10, pady=10)

        frm = tk.Frame(self)
        frm.pack(fill="x", padx=10, pady=(0, 10))

        tk.Button(frm, text="📂 Open Image",
                  command=self.open_image, width=16).pack(side="left", padx=4)
        
        self.lbl = tk.Label(frm, text="No image loaded", fg="gray")
        self.lbl.pack(side="left", padx=8, expand=True, fill="x")
        self.btn_slice = tk.Button(frm, text="✂️ Slice!",
                                   command=self.do_slice, width=14,
                                   state="disabled", bg="#4CAF50", fg="white")
        
        self.btn_slice.pack(side="right", padx=4)

    def open_image(self):
        path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png *.jpg *.jpeg *.bmp *.gif *.webp")])

        if not path:
            return
        
        self.img_path = path
        self.img = Image.open(path)
        self.lbl.config(text=os.path.basename(path), fg="black")
        self.btn_slice.config(state="normal")
        self._preview()

    def _preview(self):
        preview = Image.new("RGBA", self.img.size, (40, 40, 40, 255))
        preview.paste(self.img.convert("RGBA"), mask=self.img.convert("RGBA").getchannel("A"))
        preview.thumbnail((500, 400))
        self._tk_img = ImageTk.PhotoImage(preview)
        self.canvas.delete("all")
        self.canvas.create_image(250, 200, image=self._tk_img)

    def do_slice(self):
        mask = load_mask(self.img)
        self.sprites = slice_sprites(self.img.convert("RGBA"), mask)

        if not self.sprites:
            messagebox.showwarning(
                "Nothing found.",
                "No sprites detected.\n\n"
                "Make sure the image is a PNG with transparent background (alpha=0)."
            )
            return

        paths = save_sprites(self.sprites, OUTPUT_DIR)

        messagebox.showinfo(
            "Success! 🎉",
            f"{len(self.sprites)} sprite(s) saved to:\n{os.path.abspath(OUTPUT_DIR)}"
        )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        img = Image.open(sys.argv[1])
        mask = load_mask(img)
        sprites = slice_sprites(img.convert("RGBA"), mask)
        paths = save_sprites(sprites, OUTPUT_DIR)
        print(f"{len(sprites)} sprites saved to \'{OUTPUT_DIR}/\'")

        for p in paths:
            print(" →", p)
    else:
        App().mainloop()
