# Maintainer: Daniel Hillenbrand <codeworkx [at] bbqlinux [dot] org>

pkgname=bbqlinux-control-panel
pkgver=1.0.0
pkgrel=1
pkgdesc="BBQLinux Control Panel"
arch=('any')
url="https://github.com/bbqlinux/bbqlinux-control-panel"
license=('GPL')
depends=('bbqlinux-artwork' 'python' 'python-pyqt4' 'java-runtime-common')
replaces=('bbqlinux-java-switcher' 'bbqlinux-python-switcher')
conflicts=('bbqlinux-java-switcher' 'bbqlinux-python-switcher')

package() {
  cd "$pkgdir"

  install -Dm755 "$srcdir/usr/bin/bbqlinux-control-panel" usr/bin/bbqlinux-control-panel

  cp -R "$srcdir/usr/lib/" usr/lib
  cp -R "$srcdir/usr/share/" usr/share
}
