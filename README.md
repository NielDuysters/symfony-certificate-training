![symfony-training-logo](https://github.com/user-attachments/assets/19b941f5-7e8b-42a9-984b-0028f8fda69a)
# Symfony Certificate Training - Python UI
I found the following Github repository ([certification symfony](https://github.com/efficience-it/certification-symfony)) containing questions to prepare for the Symfony certificate exam in Yaml-format. This Python script provides a user-friendly interface to practice the quiz.

## Screenshots
Topic selection
<img width="1259" alt="symfony-quiz-tool-2" src="https://github.com/user-attachments/assets/608e3857-7025-4f71-9248-6e6dcdc60217" />

Q & A + Results
<img width="1265" alt="symfony-quiz-tool-1" src="https://github.com/user-attachments/assets/940e56ac-8dd7-443e-b4c6-25e44b805c99" />



## Technical specifications
- Python 3.13.0

## Installation
Prerequisites:
- Python 3
- *nix/Unix system

```
# Clone repository
git clone https://github.com/NielDuysters/symfony-certificate-training.git

# Clone certification-symfony repository
git clone https://github.com/efficience-it/certification-symfony.git

# Copy data directory from certification-symfony to our directory
cp -R certification-symfony/data symfony-certificate-training/data

cd symfony-certificate-training

# Create virtual env
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip3 install pyyaml
pip3 install prettytable

# Run app
python3 main.py
```

## Usage
```
python3 main.py
```

## TODO
- Implement feedback: https://codereview.stackexchange.com/questions/294718/quiz-interface-based-on-yaml-files-python
