# Face Detector Plus

"A comprehensive Python package that integrates multiple face detection algorithms, offering flexible and efficient solutions for various face recognition applications."

**Key features:**

- Easy to understand and setup
- Easy to manage
- Requires very less or no tuning for any resolution image
- No need to download models, they're automatically maintained
- Uses ultralight face detection models that is very fast on CPU alone
- Get very good speed and accuracy on CPU alone
- All detectors share same parameters and methods, makes it easier to switch and go

**Detectors:**

- Hog detector
- CNN detector
- Caffemodel detector
- UltraLight 320 detector
- UltraLight 640 detector


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install [face-detector-plus](https://pypi.org/project/face-detector-plus/) with the following command:

```bash
pip install face-detector-plus
```

If you would like to get the latest master or branch from github, you could also:

```bash
pip install git+https://github.com/huseyindas/face-detector-plus
```

Or even select a specific revision _(branch/tag/commit)_:

```bash
pip install git+https://github.com/huseyindas/face-detector-plus@master
```

Similarly, for tag specify [tag](https://github.com/huseyindas/face-detector-plus/tags) with `@v0.x.x`. For example to download tag v0.1.0 from Git use:

```bash
pip install git+https://github.com/huseyindas/face-detector-plus@v0.1.0
```

## Quick usage

Like said setup and usage is very simple and easy.

- Import the detector you want,
- Initialize it,
- Get predicts

**_Example_**

```python
from face_detector_plus import Ultralight320Detector
from face_detector_plus.utils import annotate_image

detector = Ultralight320Detector()

image = cv2.imread("image.png")

faces = detector.detect_faces(image)
image = annotate_image(image, faces, width=3)

cv2.imshow("view", image)
cv2.waitKey(100000)
```

### CaffeModel Detector

Caffemodel is very light weight model that uses less resources to perform detections that is created by caffe (Convolutional Architecture for Fast Feature Embedding).

```python
import cv2
from face_detector_plus import CaffemodelDetector
from face_detector_plus.utils import annotate_image

vid = cv2.VideoCapture(0)
detector = CaffemodelDetector()

while True:
    rect, frame = vid.read()
    if not rect:
        break

    bbox = detector.detect_faces(frame)
    frame = annotate_image(frame, bbox)

    cv2.imshow("Caffe Model Detection", frame)

    cv2.waitKey(1)
```

**Configurable options for CaffeModel detector**.

Syntax: `CaffemodelDetector(**options)`

| Options         | Description                                                                                                                                                                                              |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `convert_color` | Takes OpenCV COLOR codes to convert the images. Defaults to cv2.COLOR_BGR2RGB                                                                                                                            |
| `confidence`    | Confidence score is used to refrain from making predictions when it is not above a sufficient threshold. Defaults to 0.5                                                                                 |
| `scale`         | Scales the image for faster output (No need to set this manually, scale will be determined automatically if no value is given)                                                                           |
| `mean`          | Scalar with mean values which are subtracted from channels. Values are intended to be in (mean-R, mean-G, mean-B) order if image has BGR ordering and swapRB is true. Defaults to (104.0, 177.0, 123.0). |
| `scalefactor`   | Multiplier for images values. Defaults to 1.0.                                                                                                                                                           |
| `crop`          | Flag which indicates whether image will be cropped after resize or not. Defaults to False.                                                                                                               |
| `swapRB`        | Flag which indicates that swap first and last channels in 3-channel image is necessary. Defaults to False.                                                                                               |
| `transpose`     | Transpose image. Defaults to False.                                                                                                                                                                      |
| `resize`        | Spatial size for output image. Default is (300, 300)                                                                                                                                                     |

**Useful methods for this detector:**

- **`detect_faces(image)`**

  This method will return coordinates for all the detected faces of the given image

  | Options | Description                 |
  | ------- | --------------------------- |
  | `image` | image in numpy array format |

- **`detect_faces_keypoints(image, get_all=false)`**

  This method will return coordinates for all the detected faces along with their facial keypoints of the given image. Keypoints are detected using dlib's new shape_predictor_68_face_landmarks_GTX.dat` model.

  _Note: Generating keypoints might take more time if compared with `detect_faces` method_

  | Options   | Description                                                               |
  | --------- | ------------------------------------------------------------------------- |
  | `image`   | Image in numpy array format                                               |
  | `get_all` | Weather to get all facial keypoints or the main (chin, nose, eyes, mouth) |

### CNN Detector

CNN (Convolutional Neural Network) might not be a light weight model but it is good at detecting faces from all angles. This detector is a hight level wrapper around `dlib::cnn_face_detection_model_v1` that is fine tuned to improve overall performance and accuracy.

```python
import cv2
from face_detector_plus import CNNDetector
from face_detector_plus.utils import annotate_image

vid = cv2.VideoCapture(0)
detector = CNNDetector()

while True:
    rect, frame = vid.read()
    if not rect:
        break

    bbox = detector.detect_faces(frame)
    frame = annotate_image(frame, bbox)

    cv2.imshow("CNN Detection", frame)

    cv2.waitKey(1)
```

**Configurable options for CNNDetector detector.**

Syntax: `CNNDetector(**options)`

| Options                       | Description                                                                                                                    |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `convert_color`               | Takes OpenCV COLOR codes to convert the images. Defaults to cv2.COLOR_BGR2RGB                                                  |
| `number_of_times_to_upsample` | Up samples the image number_of_times_to_upsample before running the basic detector. By default is 1.                           |
| `confidence`                  | Confidence score is used to refrain from making predictions when it is not above a sufficient threshold. Defaults to 0.5       |
| `scale`                       | Scales the image for faster output (No need to set this manually, scale will be determined automatically if no value is given) |

- **`detect_faces(image)`**

  This method will return coordinates for all the detected faces of the given image

  | Options | Description                 |
  | ------- | --------------------------- |
  | `image` | image in numpy array format |

- **`detect_faces_keypoints(image, get_all=false)`**

  This method will return coordinates for all the detected faces along with their facial keypoints of the given image. Keypoints are detected using dlib's new `shape_predictor_68_face_landmarks_GTX.dat` model.

  _Note: Generating keypoints might take more time if compared with `detect_faces` method_

  | Options   | Description                                                               |
  | --------- | ------------------------------------------------------------------------- |
  | `image`   | Image in numpy array format                                               |
  | `get_all` | Weather to get all facial keypoints or the main (chin, nose, eyes, mouth) |

### Hog Detector

This detector uses Histogram of Oriented Gradients (HOG) and Linear SVM classifier for face detection. It is also combined with an image pyramid and a sliding window detection scheme. `HogDetector` is a high level client over dlib's hog face detector and is fine tuned to make it more optimized in both speed and accuracy.

If you want to detect faster with `HogDetector` and don't care about number of detections then set `number_of_times_to_upsample=1` in the options, it will detect less fasces in less time, mainly used for real time one face detection.

```python
import cv2
from face_detector_plus import HogDetector
from face_detector_plus.utils import annotate_image

vid = cv2.VideoCapture(0)
detector = HogDetector()

while True:
    rect, frame = vid.read()
    if not rect:
        break

    bbox = detector.detect_faces(frame)
    frame = annotate_image(frame, bbox)

    cv2.imshow("Hog Detection", frame)

    cv2.waitKey(1)
```

**Configurable options for HogDetector detector.**

Syntax: `HogDetector(**options)`

| Options                       | Description                                                                                                                    |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `convert_color`               | Takes OpenCV COLOR codes to convert the images. Defaults to cv2.COLOR_BGR2RGB                                                  |
| `number_of_times_to_upsample` | Up samples the image number_of_times_to_upsample before running the basic detector. By default is 2.                           |
| `confidence`                  | Confidence score is used to refrain from making predictions when it is not above a sufficient threshold. Defaults to 0.5       |
| `scale`                       | Scales the image for faster output (No need to set this manually, scale will be determined automatically if no value is given) |

- **`detect_faces(image)`**

  This method will return coordinates for all the detected faces of the given image

  | Options | Description                 |
  | ------- | --------------------------- |
  | `image` | image in numpy array format |

- **`detect_faces_keypoints(image, get_all=false)`**

  This method will return coordinates for all the detected faces along with their facial keypoints of the given image. Keypoints are detected using dlib's new `shape_predictor_68_face_landmarks_GTX.dat` model.

  _Note: Generating keypoints might take more time if compared with `detect_faces` method_

  | Options   | Description                                                               |
  | --------- | ------------------------------------------------------------------------- |
  | `image`   | Image in numpy array format                                               |
  | `get_all` | Weather to get all facial keypoints or the main (chin, nose, eyes, mouth) |

### Ultra Light Detection (320px)

Ultra Light detection model is what the name says, it a very light weight, accuracy with impressive speed which is pre-trained on 320x240 sized images and only excepts 320x240 sized images but don't worry `Ultralight320Detector` detector will do all for you.

```python
import cv2
from face_detector_plus import Ultralight320Detector
from face_detector_plus.utils import annotate_image

vid = cv2.VideoCapture(0)
detector = Ultralight320Detector()

while True:
    rect, frame = vid.read()
    if not rect:
        break

    bbox = detector.detect_faces(frame)
    frame = annotate_image(frame, bbox)

    cv2.imshow("Ultra 320 Detection", frame)

    cv2.waitKey(1)
```

**Configurable options for Ultralight320Detector detector.**

Syntax: `Ultralight320Detector(**options)`

| Options         | Description                                                                                                                    |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `convert_color` | Takes OpenCV COLOR codes to convert the images. Defaults to cv2.COLOR_BGR2RGB                                                  |
| `mean`          | Metric used to measure the performance of models doing detection tasks. Defaults to [127, 127, 127].                           |
| `confidence`    | Confidence score is used to refrain from making predictions when it is not above a sufficient threshold. Defaults to 0.5       |
| `scale`         | Scales the image for faster output (No need to set this manually, scale will be determined automatically if no value is given) |
| `cache`         | It uses same model for all the created sessions. Default is True                                                               |

- **`detect_faces(image)`**

  This method will return coordinates for all the detected faces of the given image

  | Options | Description                 |
  | ------- | --------------------------- |
  | `image` | image in numpy array format |

- **`detect_faces_keypoints(image, get_all=false)`**

  This method will return coordinates for all the detected faces along with their facial keypoints of the given image. Keypoints are detected using dlib's new `shape_predictor_68_face_landmarks_GTX.dat` model.

  _Note: Generating keypoints might take more time if compared with `detect_faces` method_

  | Options   | Description                                                               |
  | --------- | ------------------------------------------------------------------------- |
  | `image`   | Image in numpy array format                                               |
  | `get_all` | Weather to get all facial keypoints or the main (chin, nose, eyes, mouth) |

### Ultra Light Detection (640px)

Ultra Light detection model is what the name says, it a very light weight, accuracy with impressive speed which is pre-trained on 640x480 sized images and only excepts 640x480 sized images but don't worry `Ultralight640Detector` detector will do all for you.

This detector will be more accurate than 320 sized ultra light model (`Ultralight320Detector`) but might take a little more time.

```python
import cv2
from face_detector_plus import Ultralight640Detector
from face_detector_plus.utils import annotate_image

vid = cv2.VideoCapture(0)
detector = Ultralight640Detector()

while True:
    rect, frame = vid.read()
    if not rect:
        break

    bbox = detector.detect_faces(frame)
    frame = annotate_image(frame, bbox)

    cv2.imshow("Ultra 640 Detection", frame)

    cv2.waitKey(1)
```

**Configurable options for Ultralight640Detector detector.**

Syntax: `Ultralight640Detector(**options)`

| Options         | Description                                                                                                                    |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `convert_color` | Takes OpenCV COLOR codes to convert the images. Defaults to cv2.COLOR_BGR2RGB                                                  |
| `mean`          | Metric used to measure the performance of models doing detection tasks. Defaults to [127, 127, 127].                           |
| `confidence`    | Confidence score is used to refrain from making predictions when it is not above a sufficient threshold. Defaults to 0.5       |
| `scale`         | Scales the image for faster output (No need to set this manually, scale will be determined automatically if no value is given) |
| `cache`         | It uses same model for all the created sessions. Default is True                                                               |

- **`detect_faces(image)`**

  This method will return coordinates for all the detected faces of the given image

  | Options | Description                 |
  | ------- | --------------------------- |
  | `image` | image in numpy array format |

- **`detect_faces_keypoints(image, get_all=false)`**

  This method will return coordinates for all the detected faces along with their facial keypoints of the given image. Keypoints are detected using dlib's new `shape_predictor_68_face_landmarks_GTX.dat` model.

  _Note: Generating keypoints might take more time if compared with `detect_faces` method_

  | Options   | Description                                                               |
  | --------- | ------------------------------------------------------------------------- |
  | `image`   | Image in numpy array format                                               |
  | `get_all` | Weather to get all facial keypoints or the main (chin, nose, eyes, mouth) |

### Annotate Image Function

Annotates the given image with the payload returned by any of the detectors and returns a well annotated image with boxes and keypoints on the faces.

**Configurable options for annotate_image function.**

Syntax: `annotate_image(**options)`

| Options         | Description                                                                  |
| --------------- | ---------------------------------------------------------------------------- |
| `image`         | Give image for annotation in numpy.Array format                              |
| `faces`         | Payload returned by detector.detect_faces or detector.detect_faces_keypoints |
| `box_rgb`       | RGB color for rectangle to be of. Defaults to (100, 0, 255).                 |
| `keypoints_rgb` | RGB color for keypoints to be of. Defaults to (150, 0, 255).                 |
| `width`         | Width of annotations. Defaults to 2                                          |
