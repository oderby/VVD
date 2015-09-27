import CommonGraphDiffer as cgd
import argparse

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("cg", help="This is the first .CGX (CommonGraph) file")
    parser.add_argument("ds", help="This is a .DSX (DiffSet) file")
    parser.add_argument("cgout", help="This is the output filename of the .CGX (CommonGraph) file")
    return parser.parse_args()

def main():
    args = parseArgs()
    CGA = cgd.CgxToObject(args.cg)
    ds =  cgd.XMLToDS(args.ds)
    CGout = CGA.applyDiff(ds)
    cgd.CGToXML(CGout, args.cgout)

if __name__ == "__main__":
    main()
