# Prerequisite

- [CMake](https://cmake.org/download/)
- [Visual Studio](https://visualstudio.microsoft.com/zh-hant/https://visualstudio.microsoft.com/zh-hant/)(使用 C++ 的桌面開發 )

# Quick Start

- 環境安裝 :  
    
    - `cd /dependencies`
    - use anaconda : `conda env create -f environment.yaml`
    - `conda activate PyOpenGL`
    - `pip install PyOpenGL_accelerate-3.1.5-cp38-cp38-win_amd64.whl`
        
        - 若已安裝需先移除`pip uninstall PyOpenGL_accelerate`
        - 解決`AttributeError: module 'numpy' has no attribute 'float128'`錯誤
        - 解決`Unable to load numpy_formathandler accelerator from OpenGL_accelerate`錯誤
        - 不同版本(`cp38`表示python3.8)可到[此處下載](https://www.lfd.uci.edu/~gohlke/pythonlibs/)

- 執行指令 :

    - 使用範例 : `python app/app.py` 
    - 顯示自己的model : `python app/app.py -model ./medias/box.obj`

# PyOpenGL API 

- [Document](http://pyopengl.sourceforge.net/documentation/manual-3.0)
- [Simple Tutorial](https://cg-dev.ltas.ulg.ac.be/svn/cadxfem/tomoprocess_deprecated/src/OpenMesh-3.3/Documentation/a00036.html#python_propman)
- [Sample Code](https://python.hotexamples.com/examples/OpenGL/GL/glColorPointer/python-gl-glcolorpointer-method-examples.html)
- [glut mouse event](https://www.itread01.com/content/1541378106.html)

# Develop

- 輸出環境 `conda env export > enviroment.yml`