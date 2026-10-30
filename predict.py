#!/usr/bin/env python3
"""
HydroFlow Plant Disease Classification Engine
Model: EfficientNetB0 (13 classes)
Saved format: Keras 3.13.2 (.keras)
Supported crops: Lettuce & Basil
"""
import os
import sys
import json

from scripts.predict_leaf import predict_image, CLASS_DESCRIPTIONS, load_class_names

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python predict.py <path_to_leaf_image>")
        print("Example: python predict.py test_leaf.jpg")
        sys.exit(1)

    image_path = sys.argv[1]
    res = predict_image(image_path)
    print(json.dumps(res, indent=2))
