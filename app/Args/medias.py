from argparse import ArgumentParser, SUPPRESS


def build_argparser():
    parser = ArgumentParser(add_help=False)
    args = parser.add_argument_group('Options')
    args.add_argument('-h', '--help', action='help', default='SUPPRESS')

    # custom command line input parameters
    args.add_argument("-output", "--output",
                      type=str, default='./output/realsense', help="where to save files.")
    args.add_argument("-folder", "--folder", type=str,
                      default='./medias/realsenseData/')
    args.add_argument("-highResModel", "--highResModel", type=str,
                      default='./medias/neptune_50k_hk.obj')
    args.add_argument("-model", "--model", type=str,
                      default='./medias/sample.obj')
    args.add_argument("-texture", "--texture", type=str,
                      default='./medias/sample.png')
    args.add_argument("-texture2", "--texture2", type=str,
                      default='./medias/chess.png')
    args.add_argument("-config", "--config", type=str,
                      default='./medias/realsenseData/config.json')
    args.add_argument("-color", "--color", type=str,
                      default='./medias/realsenseData/color.png')
    args.add_argument("-depth", "--depth", type=str,
                      default='./medias/realsenseData/depth16.png')

    # two side hand data
    args.add_argument("-color1", "--color1", type=str,
                      default='./medias/depthhull/20201029150546098733.634204003874.color.png')
    args.add_argument("-config1", "--config1", type=str,
                      default='./medias/depthhull/20201029150546098733.634204003874.config.json')
    args.add_argument("-depth1", "--depth1", type=str,
                      default='./medias/depthhull/20201029150546098733.634204003874.depth16.png')
    args.add_argument("-color2", "--color2", type=str,
                      default='./medias/depthhull/20201029150625453271.634204003874.color.png')
    args.add_argument("-config2", "--config2", type=str,
                      default='./medias/depthhull/20201029150625453271.634204003874.config.json')
    args.add_argument("-depth2", "--depth2", type=str,
                      default='./medias/depthhull/20201029150625453271.634204003874.depth16.png')



    return parser
