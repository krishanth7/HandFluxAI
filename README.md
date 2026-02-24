# HandFluxAI 🖐️✨

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Latest-orange.svg)](https://mediapipe.dev/)

**HandFluxAI** is a professional-grade, real-time AI hand gesture control system. Leveraging cutting-edge computer vision and landmark detection, it allows users to control their computer interface through intuitive hand gestures captured via a standard webcam.

---

## 🚀 Features

- 🖱️ **Mouse Control**: Fluid cursor movement using your index finger.
- 👆 **Clicking**: Simple pinch gestures for left and right clicks.
- 🔊 **Volume Control**: Dynamic volume adjustment based on the distance between your thumb and index finger.
- 📜 **Scrolling**: Multi-finger gestures for seamless page scrolling.
- ⏯️ **Media Control**: Clench your fist to pause or play media content.
- ⚡ **Real-time Performance**: High FPS tracking with minimal latency.
- 🧼 **Visual Feedback**: Clean on-screen overlays showing tracking points and recognized gestures.

---

## 🛠️ Tech Stack

- **Computer Vision**: OpenCV
- **Hand Tracking**: Google MediaPipe
- **Numerical Processing**: NumPy
- **System Automation**: PyAutoGUI
- **OS Interface**: Python-based event mapping

---

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/krishanth7/HandFluxAI.git
   cd HandFluxAI
   ```

2. **Create a virtual environment (Optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🎮 Usage

Run the main script to start the gesture recognition system:

```bash
python main.py
```

### Quick Commands:
- **Index Finger Up**: Move Mouse
- **Thumb + Index Pinch**: Left Click
- **Thumb + Middle Pinch**: Right Click
- **Fist (All Down)**: Pause/Play (Spacebar)
- **Index + Middle + Ring Up**: Scroll Mode
- **'q'**: Quit the application

---

## 🗺️ Project Structure

```text
HandFluxAI/
│
├── main.py                 # Application entry point
├── requirements.txt         # Project dependencies
├── README.md               # Documentation
├── .gitignore              # Git ignore rules
├── LICENSE                 # MIT License
│
├── src/                    # Source code
│   ├── hand_tracker.py     # MediaPipe wrapper logic
│   ├── gesture_recognizer.py# Gesture interpretation logic
│   ├── action_controller.py# System action execution
│   └── utils.py            # Calculations & smoothing
│
├── assets/                 # Brand & demo assets
│   └── screenshots/        # UI Screenshots
│
└── docs/                   # Technical documentation
    └── architecture.md     # System design overview
```

---

## 📐 Architecture

HandFluxAI follows a modular pipeline:
1. **Perception**: Captures webcam frames and detects 21 hand landmarks.
2. **Recognition**: Analyzes landmark orientations to identify predefined gestures.
3. **Execution**: Maps recognized gestures to system-level PyAutoGUI commands with motion smoothing.

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

**Developed with ❤️ by [Krishanth](https://github.com/krishanth7)**
