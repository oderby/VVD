import CommonGraphDiffer as cgd
import argparse

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("cg1", help="This is the first .CGX (CommonGraph) file")
    parser.add_argument("cg2", help="This is the second .CGX (CommonGraph) file")
    parser.add_argument("ds", help="This is the output filename of a .DSX (DiffSet) file")
    return parser.parse_args()

def main():
    args = parseArgs()
    CGA = cgd.CgxToObject(args.cg1)
    CGB = cgd.CgxToObject(args.cg2)
    ds = CGA.diff(CGB)
    print ds
    cgd.DSToXML(ds, args.ds)

if __name__ == "__main__":
    main()
