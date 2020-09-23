# RealsesneApp Capture Data format

- ${time}.${realsense_serial_num}.depth16.png : 16bit depth image
- ${time}.${realsense_serial_num}.color.png : rgb color image
- ${time}.${realsense_serial_num}.config.json : camera Info

```json
{
    "realsense_serial_num": "932122061885",
    "time": "20200923_193537_135",
    "depth_fx": 1382.960205078125,
    "depth_fy": 1379.7989501953125,
    "depth_cx": 957.801025390625,
    "depth_cy": 531.53662109375,
    "depth_scale": 0.0010000000474974513,
    "depth_width": 1920,
    "depth_height": 1080,
    "rgb_fx": 1382.960205078125,
    "rgb_fy": 1379.7989501953125,
    "rgb_cx": 957.801025390625,
    "rgb_cy": 531.53662109375,
    "rgb_width": 1920,
    "rgb_height": 1080,
    "calibrateMat": [
        [
            1.0,
            0.0,
            0.0,
            0.0
        ],
        [
            0.0,
            1.0,
            0.0,
            0.0
        ],
        [
            0.0,
            0.0,
            1.0,
            0.0
        ],
        [
            0.0,
            0.0,
            0.0,
            1.0
        ]
    ],
    "positiveBoundaryCorner": [
        1.0,
        1.0,
        1.0
    ],
    "negativeBoundaryCorner": [
        -1.0,
        -1.0,
        -1.0
    ]
}
```