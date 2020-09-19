from argparse import ArgumentParser, SUPPRESS


def build_argparser():
    parser = ArgumentParser(add_help=False)
    args = parser.add_argument_group('Options')
    args.add_argument('-h', '--help', action='help', default='SUPPRESS')

    # custom command line input parameters
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
