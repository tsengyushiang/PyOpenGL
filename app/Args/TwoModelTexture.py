from argparse import ArgumentParser, SUPPRESS

def build_argparser():
    parser = ArgumentParser(add_help=False)
    args = parser.add_argument_group('Options')
    args.add_argument('-h', '--help', action='help', default='SUPPRESS')

    # custom command line input parameters
    args.add_argument("-modelFront", "--modelFront", type=str,
                      default='./medias/front.obj')
    args.add_argument("-modelBack", "--modelBack", type=str,
                      default='./medias/back.obj')
    args.add_argument("-textureFront", "--textureFront", type=str,
                      default='./medias/front.png')
    args.add_argument("-textureBack", "--textureBack", type=str,
                      default='./medias/back.png')

    return parser
