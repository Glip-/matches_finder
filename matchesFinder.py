import re
import argparse

'''
to do:
1) standard input if no files are specified, or the file name '-' is given
'''

color = '\033[{0}m'
colorGreenStr = color.format(32)
colorRedStr = color.format(31)
resetStr = color.format(0)


class outputPrinter:
    def __init__(self, match):
        self.match = match

    def normalPrint(self, filename, output):
        print("\n\nThere are matches in file '" + str(filename) + "':\n")
        for t in output:
            print(t)

    def colorPrint(self, filename, output):
        print("\n\nThere are matches in file '" + str(filename) + "':\n")
        for t in output:
            self.coloredText = ''
            lastMatch = 0

            for m in self.match.finditer(t):
                start, end = m.span()
                self.coloredText += t[lastMatch: start]
                self.coloredText += colorGreenStr
                self.coloredText += t[start: end]
                self.coloredText += resetStr
                lastMatch = end
            self.coloredText += t[lastMatch:]
            print(self.coloredText)

    def underscorePrint(self, filename, output):
        print("\n\nThere are matches in file '" + str(filename) + "':\n")
        for t in output:
            self.underscoreText = ''
            lastMatch = 0

            for m in self.match.finditer(t):
                start, end = m.span()
                self.underscoreText += " " * (start - lastMatch)
                self.underscoreText += "^" * (end - start)
                lastMatch = end
                self.underscoreText += " " * lastMatch
            print(t)
            print(self.underscoreText)

    def machinePrint(self, filename, output):
        for t in output:
            lineNumber = t.split()[0]
            self.outputText = ''
            foundMatches = 0

            for m in self.match.finditer(t):
                if foundMatches == 1:
                    self.outputText += "\n"
                start, end = m.span()
                self.outputText += ":".join([filename, str(lineNumber), str(start), str(t[start: end])])
                foundMatches = 1
            print(self.outputText)


class matchesFinder:
    def __init__(self, args):

        self.listOfFiles = args.filenames.split(",")
        self.match = re.compile(args.regexp)
        self.op = outputPrinter(self.match)
        self.printStyle = 0
        if args.color:
            self.printStyle = 1
        elif args.underscore:
            self.printStyle = 2
        elif args.machine:
            self.printStyle = 3

        for filename in self.listOfFiles:
            self.output = self.find(filename)

            if self.output:
                if self.printStyle == 1:
                    self.op.colorPrint(filename, self.output)
                elif self.printStyle == 2:
                    self.op.underscorePrint(filename, self.output)
                elif self.printStyle == 3:
                    self.op.machinePrint(filename, self.output)
                else:
                    self.op.normalPrint(filename, self.output)
            elif self.output == None:
                print("\n\nCan not open file " + colorRedStr + str(filename) + resetStr)
            else:
                print("\n\nNo Matches in file " + str(filename))

    def find(self, filename):
        output = []
        try:
            with open(filename) as f:
                i = 0
                for line in f:
                    i += 1
                    if self.match.search(line):
                        output.append(str(i) + "      " + line.rstrip())
            return output
        except:
            return None


def parse_arguments():
    parser = argparse.ArgumentParser(description='Matches Finder')
    parser.add_argument("-r", "--regexp",
                          help=colorRedStr + 'Required' + resetStr + ', enter regexp in double quotes ""',
                          type=str, required=True)
    parser.add_argument("-f", "--filenames", help=colorRedStr + "Required" + resetStr + ", enter the comma separated list of filenames",
                          type=str, required=True)

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--color",
                          help="Optional, Highlight matching text with " + colorGreenStr + "color" + resetStr, action='store_true')
    group.add_argument("-u", "--underscore",
                          help="Optional, Print '^' under the matching text", action='store_true')
    group.add_argument("-m", "--machine",
                          help="Optional, Generate machine readable output", action='store_true')

    return parser


def main():
    parser = parse_arguments()
    args = parser.parse_args()

    matchesFinder(args)


if __name__ == "__main__":
    main()