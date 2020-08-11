from argparse import ArgumentParser, SUPPRESS

def build_argparser():
   parser = ArgumentParser(add_help=False)
   args = parser.add_argument_group('Options')   
   args.add_argument('-h', '--help', action='help',default='SUPPRESS') 

   # custom command line input parameters       
   args.add_argument("-model", "--model", type=str,default='./medias/sample.obj')
   args.add_argument("-texture", "--texture", type=str,default='./medias/sample.png')

   return parser