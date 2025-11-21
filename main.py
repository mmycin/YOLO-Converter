# app.py
import streamlit as st
import json
import os
import shutil
from pathlib import Path
import zipfile

# Config
st.set_page_config(page_title="YOLO Exporter + ZIP", layout="centered")
st.title("YOLO Model Exporter")
st.markdown("Upload `.pt` → Choose format → Download as **ZIP** → Server auto-cleans")

# Load formats.json
JSON_FILE = "formats.json"


def load_formats():
    if not os.path.exists(JSON_FILE):
        st.error(f"'{JSON_FILE}' not found in app directory!")
        st.stop()
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        raw = json.load(f)
        data = raw[0]["data"] if isinstance(raw, list) and "data" in raw[0] else raw
        mapping = {list(item.keys())[0]: list(item.values())[0] for item in data}
        return mapping


formats = load_formats()
if not formats:
    st.stop()

# UI
uploaded_file = st.file_uploader("Upload YOLO model (.pt)", type=["pt"])

if uploaded_file:
    # Save uploaded .pt temporarily
    temp_model_path = "temp_uploaded_model.pt"
    with open(temp_model_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Uploaded: **{uploaded_file.name}**")

    # Format selector
    selected_name = st.selectbox("Select export format", options=sorted(formats.keys()))
    export_format = formats[selected_name]

    if st.button("Export & Create ZIP", type="primary"):
        with st.spinner(f"Exporting to {selected_name} ({export_format})..."):
            try:
                from ultralytics import YOLO

                # Load and export
                model = YOLO(temp_model_path)
                exported_path = model.export(format=export_format, imgsz=640)

                # Convert Path object to string
                exported_path = str(exported_path)

                # Create ZIP
                zip_filename = f"{Path(uploaded_file.name).stem}_{export_format}.zip"
                with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
                    if os.path.isfile(exported_path):
                        zipf.write(
                            exported_path, arcname=os.path.basename(exported_path)
                        )
                    else:
                        # It's a directory (e.g. saved_model/, openvino_model/)
                        for root, dirs, files in os.walk(exported_path):
                            for file in files:
                                full_path = os.path.join(root, file)
                                arcname = os.path.relpath(
                                    full_path, start=os.path.dirname(exported_path)
                                )
                                zipf.write(full_path, arcname)

                # Success + Download
                st.success(f"Exported & zipped successfully!")
                with open(zip_filename, "rb") as f:
                    st.download_button(
                        label="Download ZIP",
                        data=f,
                        file_name=zip_filename,
                        mime="application/zip",
                        type="primary",
                    )

                st.balloons()

            except Exception as e:
                st.error(f"Export failed: {e}")
            finally:
                # AUTO CLEANUP — Remove everything
                files_to_remove = [temp_model_path, exported_path, zip_filename]
                for path in files_to_remove:
                    try:
                        if os.path.isfile(path):
                            os.remove(path)
                        elif os.path.isdir(path):
                            shutil.rmtree(path)
                    except:
                        pass  # Silent cleanup

                st.info("All temporary files deleted from server")

else:
    st.info("Upload a `.pt` model to get started")

st.markdown("---")
st.caption("Secure • Auto-clean • Made for Bangladesh & Beyond")
