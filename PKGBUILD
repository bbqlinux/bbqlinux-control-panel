# Maintainer: Daniel Hillenbrand <codeworkx [at] bbqlinux [dot] org>

pkgname=bbqlinux-control-panel
pkgver=1.1.0
pkgrel=1
pkgdesc="BBQLinux Control Panel"
arch=('any')
url="https://github.com/bbqlinux/bbqlinux-control-panel"
license=('GPL')
depends=('bbqlinux-artwork' 'python' 'python-pyqt5' 'python-dbus' 'java-runtime-common')
replaces=('bbqlinux-java-switcher' 'bbqlinux-python-switcher')
conflicts=('bbqlinux-java-switcher' 'bbqlinux-python-switcher')

package() {
  cd "$pkgdir"

  install -Dm755 "$srcdir/usr/bin/bbqlinux-control-panel" usr/bin/bbqlinux-control-panel
  install -Dm755 "$srcdir/usr/bin/bbqlinux-control-panel-service" usr/bin/bbqlinux-control-panel-service

  cp -R "$srcdir/etc/" etc
  cp -R "$srcdir/usr/lib/" usr/lib
  cp -R "$srcdir/usr/share/" usr/share
}
