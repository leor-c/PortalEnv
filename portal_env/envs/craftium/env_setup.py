from pathlib import Path
import os
import subprocess


APT_PKGS_DEFAULT = [
    "g++", "make", "libc6-dev", "cmake", "libpng-dev", "libjpeg-dev",
    "libgl1-mesa-dev", "libsqlite3-dev", "libogg-dev", "libvorbis-dev",
    "libopenal-dev", "libcurl4-gnutls-dev", "libfreetype6-dev", "zlib1g-dev",
    "libgmp-dev", "libjsoncpp-dev", "libzstd-dev", "libluajit-5.1-dev",
    "gettext", "libsdl2-dev", "libpython3-dev", 
    "git", "pkg-config", "ca-certificates",
    "xvfb",
    "libxml2"
]
#sudo apt install 



def main():
    # Assume this script runs by the appropriate micromamba env.
    # cache_path = Path(user_cache_dir("portal-env"))

    apt_cmd = []
    apt_update_cmd = []
    if os.geteuid() != 0:
        apt_cmd.append('sudo')
        apt_update_cmd.append('sudo')
    apt_update_cmd += ['apt-get', 'update']
    subprocess.run(apt_update_cmd, check=True)
    apt_cmd += ["apt-get", "install", "-y", "--no-install-recommends", "--fix-missing", "--fix-broken", *APT_PKGS_DEFAULT]
    subprocess.run(apt_cmd, check=True)

    subprocess.run(['pip install uv'], check=True)

    craftium_clone_path = Path('.')
    clone_cmd = ['git', 'clone', '--recurse-submodules', 'https://github.com/mikelma/craftium.git']
    subprocess.run(clone_cmd, check=True, cwd=craftium_clone_path)

    subprocess.run(['uv pip', 'install', '--upgrade', 'pip'], check=True)
    subprocess.run(['uv pip', 'install', '--upgrade', 'setuptools'], check=True)
    subprocess.run(['uv pip', 'install', '.'], check=True, cwd=craftium_clone_path / 'craftium') # portal loguru gymnasium


if __name__ == '__main__':
    main()
