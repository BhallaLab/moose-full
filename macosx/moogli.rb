class Moogli < Formula
  desc "3d visualizer of neuronal simulation"
  homepage "http://moose.ncbs.res.in/moogli"
  url "https://github.com/BhallaLab/moogli/archive/macosx.tar.gz"
  version "0.5.0"

  depends_on "open-scene-graph"
  depends_on "python" if MacOS.version <= :snow_leopard
  depends_on "gcc"
  depends_on "sip"
  depends_on "pyqt"

  def install
    ENV['CC'] = "#{HOMEBREW_PREFIX}/bin/gcc-5"
    ENV['CXX'] = "#{HOMEBREW_PREFIX}/bin/g++-5"
    # Copy QtCore.so etc to lib of our app.
    system "python", "setup.py", "build"
    system "python", "setup.py", "install"
  end

  test do
    system "#{HOMEBREW_PREFIX}/bin/python", "-c", "import moogli"
  end
end
