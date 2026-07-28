# DSAR Labs

This repository provides the student lab notebooks, synthetic datasets, and shared GitHub Codespaces environment for DSAR.

Canvas is the source for quiz availability, deadlines, and grading. The notebooks are learning environments: complete the code, run each notebook from top to bottom, and use the displayed outputs to complete the corresponding Canvas quiz. The notebooks themselves are not collected.

## Open the labs in GitHub Codespaces

1. Select **Code** on the repository page.
2. Select **Codespaces** and create a codespace on `main`.
3. Open the assigned notebook from `labs/`.
4. Complete the code challenges and run the notebook from top to bottom.
5. Check that the required tables and figures appear.
6. Complete the corresponding Canvas quiz using your notebook outputs.

Save your work in the codespace. You may download a notebook as a personal backup, but it is not uploaded for grading.

## Repository structure

- `labs/`: student notebooks.
- `data/`: four independent synthetic dataset groups.
- `docs/`: links to documentation used by the labs.
- `assets/`: shared student-facing assets when needed.
- `.devcontainer/`: the shared Codespaces environment.

The files in `data/labs_01_03/` are used by Labs 1–3. Later dataset groups contain distinct synthetic samples. Do not link participant records across dataset groups.

## Troubleshooting

If a notebook cannot find a file, confirm that the notebook remains in `labs/` and that the expected CSV remains in its assigned folder under `data/`. If an import fails, restart the notebook kernel; if needed, rebuild the Codespace container.
