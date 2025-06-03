# 2D to 3D Image Generation using Depth Estimation

This project converts a single 2D image into a 3D point cloud using monocular depth estimation powered by the GLPN deep learning model. The 3D scene is then visualized using Open3D.

---

## 📌 Project Overview

This Python-based system:

- Loads a single 2D image
- Applies the `GLPN (Global-Local Path Network)` model from Hugging Face to predict depth
- Converts depth + RGB into an RGBD image
- Builds a 3D point cloud using Open3D
- Visualizes or exports the point cloud

---

## ✅ Real-World Applications

### 🎮 AR/VR & Game Dev
- Quickly convert 2D concept art or objects to 3D form

### 🤖 Robotics
- Enable depth perception using just RGB cameras

### 🎨 Creative Media
- Enhance flat images with pseudo-3D visuals or effects

---

## 🔧 Why This Approach?

- **Pretrained Model**: Leverages `vinvino02/glpn-nyu` for accurate depth prediction
- **Offline**: All computations run locally
- **Flexible**: Works on any standard image format (JPG, PNG)
- **Lightweight**: Requires no GPU (optional but beneficial)

---

## 🛠️ Requirements

- Python 3.8+
- PyTorch
- Open3D
- Transformers
- Pillow
- Matplotlib

### Installation:

```bash
pip install torch torchvision transformers pillow matplotlib open3d
```

## 📽️ Demo

![Demo Output](https://github.com/Ratheesh1104/Generating-3D-Image-with-2D-Image/blob/main/Output/output_gif.gif)

---
