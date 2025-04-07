from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': []}

base = 'gui'

executables = [
    Executable('run.py', base=base, target_name = 'PAQSGui')
]

setup(name='PAQSGui',
      version = '1.0',
      description = 'GUI implementation of xpca and database management for PAQS',
      options = {'build_exe': build_options},
      executables = executables)
