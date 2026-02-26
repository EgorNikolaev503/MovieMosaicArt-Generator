
# 🎬 MosaicArt Generator — Movie Poster Mosaic

A creative tool that transforms any image into a mosaic made entirely of movie posters — where each tile is a real poster whose *average color* best matches the corresponding region of your input image.

---

## Quick Start

1. **Unpack the poster archive**
2. **Create color dictionary**
   ```bash
   python dict_creating.py
   ```
   → Generates `color_dict.json` (takes ~1–5 min for 70k posters).
3. **Prepare your input image**
   - Place your image in the root folder and rename it to `input.jpg`.
   - Recommended: do not use to big input images

4. **Generate the mosaic**
   ```bash
   python main_algorithm.py
   ```
   - Output: `mosaic_result.jpg` (very high resolution — e.g., 20k×10k for HD input).
   - By default: **allows reuse** of posters (fast, dense mosaic).
   - To disable reuse (each poster used at most once):  
     Edit `main_algorithm.py`, change `allow_repeats=False`.

5. **Preview as pixel art (optional)**
   ```bash
   python pixel_art_algorithm.py
   ```
   → Creates `pixel_art_result.jpg`: a low-res 16×9-block version showing *only colors* — great for checking composition before generating huge mosaic.

---

## 🛠️ Customization

- Want to use your own photos instead of posters ? (you need at least 20,000 photos)
  → Put them in `images/`, ensure they’re **16×9**, rerun `dict_creating.py`.

- Want smaller output?  
  → Change `block_w, block_h = 16, 9` to larger values (e.g., `32, 18`) in both algorithms — fewer, bigger tiles.
