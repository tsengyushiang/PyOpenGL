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
                      default='./medias/neptune_200k_org.obj')
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

    return parser
