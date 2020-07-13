PyOpenGL

# Install

- `cd /dependencies`
- use anaconda : `conda env create -f environment.yaml`
- `conda activate PyOpenGL`
- `pip install PyOpenGL_accelerate-3.1.5-cp38-cp38-win_amd64.whl`
    
    - 解決`AttributeError: module 'numpy' has no attribute 'float128'`錯誤
    - 不同版本(`cp38`表示python3.8)可到[此處下載](https://www.lfd.uci.edu/~gohlke/pythonlibs/)
