# YOLO Model Export Converter + Auto-ZIP Downloader  
**A complete, secure, and automated tool to convert Ultralytics YOLO `.pt` models to any supported format and download as ZIP**

---

### Project Structure
```
.
├── format_crawler/                  ← Scrapy project that crawls export formats
│   ├── format_crawler/
│   │   └── spiders/yoloformat_spider.py
│   ├── scrapy.cfg
│   └── yolo_format_mapping.json     ← Raw output from crawler (optional)
├── formats.json                     ← Clean final format mapping (used by app)
├── main.py                          ← Streamlit web app (the converter)
├── pyproject.toml                   ← Dependencies (managed with uv)
└── uv.lock
```

---

### Part 1 – The Format Scraper (format_crawler)

This Scrapy spider automatically fetches the **latest export format list** from the official Ultralytics documentation:

https://docs.ultralytics.com/modes/export/

It extracts:
- Human-readable format name → command-line format argument  
  Example: `{"TorchScript": "torchscript"}`, `{"TensorRT": "engine"}`

#### Run the scraper (whenever Ultralytics adds new formats)
```bash
cd format_crawler
scrapy crawl yoloformat_spider
```

After running, copy the generated list from `yolo_format_mapping.json` into the root `formats.json` (or just overwrite it).

> **Why scrape?**  
> Ultralytics frequently adds new export formats (RKNN, IMX500, ExecuTorch, etc.).  
> This keeps your app **100% up-to-date** without manual editing.

---

### Part 2 – The Streamlit Converter App (main.py)

A beautiful, secure web app that lets anyone:

1. Upload a `.pt` YOLO model  
2. Choose any officially supported export format  
3. Convert it instantly using `model.export()`  
4. Download the result as a **ZIP**  
5. **All files are automatically deleted** from the server after download

#### Features
- Zero leftover files (perfect for public deployment)
- Supports folders (e.g., SavedModel, OpenVINO) and single files
- Auto-ZIP creation
- Clean UI with balloons on success
- Works on Streamlit Community Cloud, Railway, Render, VPS, etc.

#### How to run locally

```bash
# Install dependencies (uses uv – super fast)
uv sync

# Run the app
streamlit run main.py
```

Open your browser at: http://localhost:8501

#### Deploy online (free)

1. Push this repo to GitHub
2. Go to https://share.streamlit.io
3. Connect your repo → Deploy!

No server management needed.

---

### How to Use (User Guide)

1. **Open the app** → https://your-app.streamlit.app
2. Click **"Upload YOLO model (.pt)"** → select your `best.pt`, `yolo11n.pt`, etc.
3. Choose desired export format from the dropdown:
   - TorchScript
   - ONNX
   - TensorRT
   - OpenVINO
   - CoreML
   - TensorFlow Lite
   - Edge TPU
   - RKNN, IMX500, ExecuTorch, etc.
4. Click **"Export & Create ZIP"**
5. Wait a few seconds → Success!
6. Click **"Download ZIP"**
7. Done! Your converted model is now on your computer.

**All temporary files are deleted from the server immediately.**

---

### Supported Export Formats (as of Nov 2025)

| Format           | Argument       |
|------------------|----------------|
| TorchScript      | `torchscript`  |
| ONNX             | `onnx`         |
| OpenVINO         | `openvino`     |
| TensorRT         | `engine`       |
| CoreML           | `coreml`       |
| TF SavedModel    | `saved_model`  |
| TF Lite          | `tflite`       |
| Edge TPU         | `edgetpu`      |
| TF.js            | `tfjs`         |
| PaddlePaddle     | `paddle`       |
| NCNN             | `ncnn`         |
| RKNN             | `rknn`         |
| ExecuTorch       | `executorch`   |
| + many more...

Always up-to-date thanks to the scraper!

---

### Security & Privacy

- No model is ever stored permanently
- Everything is deleted right after download
- Safe for public deployment
- Ideal for sharing with clients, students, or teammates

