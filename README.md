# Prerequisite

- [CMake](https://cmake.org/download/)
- [Visual Studio](https://visualstudio.microsoft.com/zh-hant/https://visualstudio.microsoft.com/zh-hant/)(使用 C++ 的桌面開發 )

# Anaconda install instructions

- 安裝指令

```
conda create -n Pyopengl3.7 python=3.7
conda activate Pyopengl3.7

pip install dotmap

conda install -c anaconda numpy
conda install -c conda-forge opencv

pip install pyrealsense2
pip install PyOpenGL PyOpenGL_accelerate
pip install openmesh
pip install pillow

pip install PyQt5

pip install wxPython

pip install scikit-image
pip install scipy
pip install open3d

```

- 範例程式

```
python app/wxApp.py
python app/qtApp.py
```

# GUI

- [wxPython tutorial](https://www.yiibai.com/wxpython/wxpython_gui_builder_tools.html)
- [wxFormBuilder](https://sourceforge.net/projects/wxformbuilder/)
    - 設定`name`,`code_generation = python`
    - 新增`component Palette/Forms/Frame`後可編輯物件
    - 物件`name`會是之後程式中使用的`class`,`property`可直接做更改
    - 儲存專案後按`F8`及會生成`.py`檔

- [QtDesinger](https://build-system.fman.io/qt-designer-download)

    - `pip install pyqt5-tools`
    - `pyuic5 -x untitled.ui -o untitled.py`
    - 讓 layout 依視窗大小縮放 : `Form/Layout in a Grid`
    - 固定子元件在 layout 中 50%-50%:
        
        - code

        ```
        graphicsView->setSizePolicy( QSizePolicy(QSizePolicy::Ignored, QSizePolicy::Ignored));
        raphicsView2->setSizePolicy(QSizePolicy(QSizePolicy::Ignored, QSizePolicy::Ignored));
        ```
        
        - 或在QtDesigner將layout右鍵`morph into QWidget`再從屬性欄中調整

# Tutorial 

- [Document](http://pyopengl.sourceforge.net/documentation/manual-3.0)
- [Simple Tutorial](https://cg-dev.ltas.ulg.ac.be/svn/cadxfem/tomoprocess_deprecated/src/OpenMesh-3.3/Documentation/a00036.html#python_propman)
- [Sample Code](https://python.hotexamples.com/examples/OpenGL/GL/glColorPointer/python-gl-glcolorpointer-method-examples.html)
- [glut mouse event](https://www.itread01.com/content/1541378106.html)
- [PyOpenMesh](https://www.graphics.rwth-aachen.de/media/openmesh_static/Documentations/OpenMesh-6.2-Documentation/a00036.html#python_build)

# Develop

- 輸出環境 `conda env export > enviroment.yml`
