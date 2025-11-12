This is a placeholder for current task notes.

## AUR Submission Progress Summary

**Date:** November 12, 2025

**Objective:** Prepare `ntfy-notify-send-bridge` for AUR submission and guide through the process.

**Progress:**
*   Updated `PKGBUILD` with maintainer information (Tim Jefferies <tim.jefferies@gmail.com>) and the correct GitHub repository URL.
*   Created an `MIT LICENSE` file.
*   Corrected the example configuration file path in `README.md`.
*   Generated `.SRCINFO` from the updated `PKGBUILD`.
*   Committed these changes to the `main` branch.
*   Set up `aur` as a new Git remote pointing to `ssh://aur@aur.archlinux.org/ntfy-notify-send-bridge.git`.
*   Pushed `main` and `dev` branches to GitHub remote (`origin`).

**Findings & Mitigations:**
*   **Initial `PKGBUILD` and `README.md` gaps:** Identified and filled in missing maintainer info, repository URL, and license details.
*   **Missing `LICENSE` file:** Created an `MIT LICENSE` file as required by AUR guidelines.
*   **`README.md` path inconsistency:** Corrected the path for the example `client.yml.example` in `README.md` to match the `PKGBUILD` installation location.
*   **Incorrect files in `main` branch for AUR:**
    *   Initially, `ntfy-notify-send-bridge.service` and `client.yml` were not correctly included in the AUR submission commit. This was rectified by amending the commit.
    *   `.gitignore` was initially tracked in `main`, which is not ideal for AUR. It was removed from tracking in `main` and committed.
*   **`current-task.md` management:**
    *   The `current-task.md` file was initially untracked.
    *   To keep development-related files separate from AUR submission, a `dev` branch was created.
    *   `current-task.md` was then added and committed to the `dev` branch.
    *   Encountered issues with `git checkout dev` due to an untracked `.gitignore` in the working directory on `main`. This was resolved by removing the untracked `.gitignore` before switching branches.
*   **AUR SSH Authentication Failure:**
    *   Encountered "Host key verification failed" during `git push aur main`.
    *   **Finding:** This is typically due to the public SSH key not being correctly registered on the AUR website or the SSH agent not having the private key loaded.
    *   **Mitigation (User Action Required):** User was instructed to manually verify their public SSH key on the AUR website and ensure their SSH agent is running and has the private key loaded (using `eval "$(ssh-agent -s)"` and `ssh-add ~/.ssh/id_rsa_arch_aur_contributor` in their terminal, and configuring `~/.bashrc` for persistence).

**Next Steps:**
*   User needs to confirm SSH agent and key setup.
*   Retry `git push aur main` once SSH authentication is confirmed to be working.
