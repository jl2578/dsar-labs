# DSAR Labs

This repository contains the student notebooks and synthetic data for the DSAR course labs.

## Start a lab in GitHub Codespaces

1. Select **Code** and then **Codespaces**.
2. Create or open a codespace for this repository.
3. Open the assigned notebook in the `labs/` folder.
4. Select the Python kernel installed for the codespace.
5. Run the notebook from top to bottom and complete each **Your Turn** section.
6. Use the displayed outputs to complete the corresponding Canvas reflection.

Save your work in the codespace. You may download a notebook as a personal backup. Grading occurs only through Canvas reflections.

## Repository folders

- `labs/`: student lab notebooks
- `data/`: synthetic datasets used by the notebooks
- `docs/`: supporting course documentation
- `assets/`: supporting images and other files

The four folders under `data/` contain distinct synthetic samples for different groups of labs. Participant IDs are meaningful only within a dataset group. Do not link records across groups.

## Troubleshooting

If a notebook cannot find a data file, confirm that you opened the notebook from `labs/` and that the repository folder structure has not changed. Then restart the kernel and run the notebook from the first cell.

If Lab 5 reports that `scipy` is missing in an existing Codespace, run `python -m pip install -r requirements.txt` in the Codespace terminal, then restart the notebook kernel. You can also rebuild the Codespace container to rerun its dependency setup.
