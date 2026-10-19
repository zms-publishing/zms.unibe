import subprocess
import sys

from Products.zms import standard

"""
Use `uv pip list` or `uv pip freeze` to get installed packages in the virtual environment.
"""
print('Monkeypatch: Products.zms.standard.get_installed_packages')
def get_installed_packages(pip_cmd='freeze'):
    pip_cmds = {
      'freeze': 'uv pip freeze',
      'list': 'uv pip list',
    }
    cmd = pip_cmds.get(pip_cmd,'freeze')
    pth = standard.getPACKAGE_HOME().rsplit('/lib/')[0] + '/bin'
    output = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            shell=True, cwd=pth, universal_newlines=True)
    stdout, stderr = output.communicate()
    stdout = "\n".join(sorted(stdout.splitlines())) if pip_cmd == 'freeze' else stdout
    packages = f'# {pth}{cmd}\n\nPython {sys.version}\n\n{stderr}\n{stdout}'
    return packages

standard.get_installed_packages = get_installed_packages
