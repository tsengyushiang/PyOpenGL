from argparse import ArgumentParser, SUPPRESS


def build_argparser():
    parser = ArgumentParser(add_help=False)
    args = parser.add_argument_group('Options')
    args.add_argument('-h', '--help', action='help', default='SUPPRESS')

    # custom command line input parameters
    args.add_argument("-device", "--device",
                      type=int, default=-1, help="specify index of device start from 1,asign 0 to open all device,default value will not open any devices.")
    args.add_argument("-output", "--output",
                      type=str, default='./output/realsense', help="where to save files.")

    return parser
