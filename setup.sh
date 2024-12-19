#!/bin/bash

echo "Installing required packages..."
pip install --pre -U unified-planning
git clone https://github.com/aiplan4eu/up-fast-downward.git && pip install up-fast-downward && rm -r -f up-fast-downward
git clone https://github.com/aiplan4eu/up-tamer.git && pip install up-tamer && rm -r -f up-tamer
git clone https://github.com/aiplan4eu/up-enhsp.git && pip install up-enhsp && rm -r -f up-enhsp
git clone https://github.com/aiplan4eu/up-pyperplan.git && pip install up-pyperplan && rm -r -f up-pyperplan

echo ""
echo "Setup complete! Environment is ready to use."
echo "To activate this environment in future terminal sessions, run:"
echo "conda activate planning"