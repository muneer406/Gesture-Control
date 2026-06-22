<div align="center">

# Gesture Control

**Control your laptop by pinching the air, plus two OpenCV face utilities.**

Hold your thumb and index finger apart and the distance between them becomes a value: screen brightness in one script, system volume in the other.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0097A7?style=flat-square&logo=google&logoColor=white)

</div>

---

## The scripts

| Script | What it does | Needs |
|---|---|---|
| `brightnessControl.py` | Pinch to set screen brightness | Webcam |
| `soundControl.py` | Pinch to set system volume | Webcam, **Windows** |
| `blurFace.py` | Live webcam feed with any detected face blurred out | Webcam |
| `extractImage.py` | Crop every face out of a photo and save each one | An input photo you supply |

---

## How the pinch works

Both control scripts run the same idea. MediaPipe Hands returns 21 landmarks per hand; only two matter here:

```
landmark 4  = thumb tip
landmark 8  = index fingertip

        distance = hypot(x2-x1, y2-y1)

   15px  |------------------------------|  220px
    min  <-- linearly mapped to range -->  max
```

`np.interp` maps that pixel distance onto the target range, so the gesture is continuous rather than a set of discrete poses:

| Script | Input range | Output range |
|---|---|---|
| `brightnessControl.py` | 15 to 220 px | 0 to 100 (percent) |
| `soundControl.py` | 15 to 220 px | volume min to max, queried from the audio endpoint |

Because the range is in raw pixels, it is implicitly tied to how far you sit from the camera. Sit closer and the same gesture reads larger. A distance normalised against hand width would fix that.

---

## Running them

```bash
pip install opencv-python mediapipe numpy screen-brightness-control
pip install pycaw comtypes          # soundControl.py only, Windows only
```

```bash
python brightnessControl.py    # q to quit
python soundControl.py         # q to quit
python blurFace.py             # q to quit
python extractImage.py         # prompts for a filename
```

**`soundControl.py` is Windows only.** It drives the volume through `pycaw`, which wraps the Windows Core Audio API. The brightness script is cross platform.

---

## Using `extractImage.py`

It reads from a `Family photos/` folder and writes crops into `Extracted Photos/`:

```bash
mkdir "Family photos"
cp yourphoto.jpg "Family photos/"
python extractImage.py
# Picture path: yourphoto        (no extension, it appends .jpg)
```

Both folders are gitignored. **Supply your own images and keep them out of version control**, especially if they contain people who have not agreed to be published.

---

## Known rough edges

- The cascade is loaded as `'haarcascade\harrcascade_frontalface_default.xml'` with a backslash, so `extractImage.py` only resolves on Windows. The filename also carries a typo (`harr`, not `haar`) that matches the file on disk.
- `extractImage.py` chdirs into the output folder and then writes to a path that includes that folder again, so the write target is not quite what it looks like.
- Detection is Haar cascade, not a modern detector. Fast, but it wants frontal, reasonably lit faces.

---

<sub>An early computer vision exercise. Archived, not maintained.</sub>
