# Image Feature Extractor

## Project Overview
This project aims to provide a way to extract out key features from an image specifically:
1. Hairs and Head
2. Eyes
3. Face region below eyes
4. Whole Face
5. Torso (Lower part of body below the face)

## Prerequisites
- Ensure you have the latest version of Python installed. If not, [install Python](https://www.python.org/downloads/).

## Getting Started
1. **Clone Repository:**
   - If you are using `ssh` keys, run:
     ```bash
     git clone git@github.com:Ashu-0202/Image_Feature_Extractor.git
     ```
   - If you are using `HTTPS`, run:
     ```bash
     git clone https://github.com/Ashu-0202/Image_Feature_Extractor.git
     ```

2. **Navigate into the project workspace:**
   ```bash
   cd Image_Feature_Extractor
   ```

3. **Setup virtual environment:**
    - If you are using `Ubuntu / Linux`, run:
        ```bash
        python3 -m venv {name}
        source {name}/bin/activate
        ```
    - If you are using `Windows`, run:
        ```bash
        python -m venv {name}
        {name}\Scripts\activate
        ```

4. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5. **Run the following command to download `face-segmentation model`:**
    ```bash
    pip install git+https://github.com/wiktorlazarski/head-segmentation.git
    ```
6. **To execute the code, run:**
    ```bash
    cd extraction
    python main.py
    ```