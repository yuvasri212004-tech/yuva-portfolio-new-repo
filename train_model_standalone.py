import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.ml.train_model import train_models

if __name__ == "__main__":
    print("Starting ML model training...")
    train_models()
    print("\nTraining complete! Model saved successfully.")
