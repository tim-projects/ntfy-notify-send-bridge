# AUR Update Guide for ntfy-notify-send-bridge-git

This guide outlines the process for submitting updates to the `ntfy-notify-send-bridge-git` package on the Arch User Repository (AUR).

**Important:** The AUR repository expects pushes to its `master` branch. Your local development happens on `dev` and `master` (which is now aligned with the AUR).

## Workflow for Submitting Updates

1.  **Make Changes on `dev` Branch:**
    Perform all your development work, bug fixes, or feature additions on your local `dev` branch.

    ```bash
    git checkout dev
    # Make your changes to files (e.g., ntfy-notify-send-bridge.py, PKGBUILD, etc.)
    ```

2.  **Update `PKGBUILD` (if necessary):**
    If your changes require modifications to dependencies, sources, or other package metadata, update the `PKGBUILD` file accordingly. Remember that `pkgver()` handles versioning for VCS packages.

3.  **Regenerate `.SRCINFO`:**
    If you modify the `PKGBUILD` file (e.g., `pkgdesc`, `depends`, `makedepends`, `provides`, `conflicts`), you **must** regenerate the `.SRCINFO` file.

    ```bash
    makepkg --printsrcinfo > .SRCINFO
    ```

4.  **Commit Your Changes:**
    Stage and commit your changes on the `dev` branch.

    ```bash
    git add .
    git commit -m "feat: Your descriptive commit message for the update"
    ```

5.  **Merge `dev` into `master`:**
    Switch to your local `master` branch and merge the `dev` branch into it. This `master` branch is what you will push to the AUR.

    ```bash
    git checkout master
    git merge dev
    ```

6.  **Push to GitHub (Optional but Recommended):**
    It's good practice to push your `master` branch to your GitHub remote first.

    ```bash
    git push origin master
    ```

7.  **Push to AUR:**
    Finally, push your local `master` branch to the AUR remote's `master` branch.

    ```bash
    git push aur master
    ```

8.  **Switch Back to `dev`:**
    After pushing to the AUR, switch back to your `dev` branch to continue development.

    ```bash
    git checkout dev
    ```

## Gitignore Strategy

To manage files tracked on different branches:

*   **`dev` branch:** The `.gitignore` on `dev` is less restrictive, allowing `.md` files (like this guide) and other development-related files to be tracked.
*   **`master` branch:** The `.gitignore` on `master` is a whitelist, ignoring everything by default and only explicitly allowing essential files for AUR submission (`PKGBUILD`, `.SRCINFO`, `README.md`, `LICENSE`, `client.yml`, `ntfy-notify-send-bridge.py`, `ntfy-notify-send-bridge.service`). This ensures only necessary files are pushed to the AUR.

## Example Scenario: Updating the Python Script

Let's say you've made changes to `ntfy-notify-send-bridge.py` and committed them on `dev`.

```bash
# On dev branch
git checkout dev
# ... edit ntfy-notify-send-bridge.py ...
git add ntfy-notify-send-bridge.py
git commit -m "fix: Improve error handling in script"

# Merge to master and push to AUR
git checkout master
git merge dev
git push origin master # Push to GitHub
git push aur master    # Push to AUR

# Back to dev
git checkout dev
```