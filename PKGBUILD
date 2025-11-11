# Maintainer: Your Name <youremail@example.com>
pkgname=ntfy-notify-send-bridge
pkgver=0.1.0
pkgrel=1
pkgdesc="Bridge messages from ntfy to notify-send using a systemd user service."
arch=('any')
url="https://github.com/yourusername/ntfy-notify-send-bridge" # TODO: Update with your actual repository URL
license=('MIT') # TODO: Confirm your license
depends=('python' 'python-requests' 'python-pyyaml' 'python-aiohttp' 'libnotify')
source=(
    "${pkgname}.py"
    "${pkgname}.service"
    "client.yml"
)
sha256sums=(
    '540ee08b9bd7bcc8b9b2a68184c8516522558492978aff486997994a0ddb0065'
    'e36714a16816141c461d39614b19dfa5bb4bd242d21d0793f4b700baee5168fb'
    '1edb61769ad62ce184df6797912724ae8e460953f5929cf4da00a23cb45e64b5'
)

package() {
    # Remove Restart and RestartSec from the service file, as the Python script handles retries internally.
    sed -i '/^Restart=/d' "${srcdir}/${pkgname}.service"
    sed -i '/^RestartSec=/d' "${srcdir}/${pkgname}.service"

    sed -i 's/^StandardOutput=journal/StandardOutput=file:\/tmp\/ntfy-bridge.log/' "${srcdir}/${pkgname}.service"
    sed -i 's/^StandardError=journal/StandardError=file:\/tmp\/ntfy-bridge.log/' "${srcdir}/${pkgname}.service"

    install -D -m 755 "${srcdir}/${pkgname}.py" "${pkgdir}/usr/bin/${pkgname}.py"
    install -D -m 644 "${srcdir}/${pkgname}.service" "${pkgdir}/usr/lib/systemd/user/${pkgname}.service"
    install -D -m 644 "${srcdir}/client.yml" "${pkgdir}/usr/share/examples/${pkgname}/client.yml.example"
}

pre_install() {
    echo "Stopping and disabling existing ${pkgname}.service (if any)..."
    systemctl --user stop ${pkgname}.service || true
    systemctl --user disable ${pkgname}.service || true
}

post_install() {
    echo "\n-----------------------------------------------------------------------"
    echo "ntfy-notify-send-bridge has been installed."
    echo "Automatically enabling and starting ${pkgname}.service..."
    systemctl --user daemon-reload
    systemctl --user enable ${pkgname}.service
    systemctl --user start ${pkgname}.service
    echo "\nTo get started:"
    echo "1. Edit ~/.config/ntfy/client.yml with your ntfy subscriptions."
    echo "   (An example config will be automatically copied there on first run if it doesn't exist.)"
    echo "   The example config is located at /usr/share/examples/${pkgname}/client.yml.example"
    echo "2. Check its status and logs:"
    echo "   systemctl --user status ${pkgname}.service"
    echo "   journalctl --user -u ${pkgname}.service -f"
    echo "-----------------------------------------------------------------------\n"
}
