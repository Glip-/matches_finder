import re, argparse, sys
import time

### to do:
### 1) standard input if no files are specified, or the file name '-' is given

color = '\033[{0}m'
colourStr = color.format(32)
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
            coloredText = ''
            lastMatch = 0

            for m in self.match.finditer(t):
                start, end = m.span()
                coloredText += t[lastMatch: start]
                coloredText += colourStr
                coloredText += t[start: end]
                coloredText += resetStr
                lastMatch = end
            coloredText += t[lastMatch:]
            print(coloredText)

    def underscorePrint(self, filename, output):
        print("\n\nThere are matches in file '" + str(filename) + "':\n")
        for t in output:
            underscoreText = ''
            lastMatch = 0

            for m in self.match.finditer(t):
                start, end = m.span()
                underscoreText += " " * (start - lastMatch)
                underscoreText += "^" * (end - start)
                lastMatch = end
            underscoreText += " " * (lastMatch)
            print(t)
            print(underscoreText)

    def machinePrint(self, filename, output):
        for t in output:
            lineNumber = t.split()[0]
            outputText = ''
            foundMatches = 0
            for m in self.match.finditer(t):
                if foundMatches == 1:
                    outputText += "\n"
                start, end = m.span()
                outputText += ":".join([filename, str(lineNumber), str(start), str(t[start: end])])
                foundMatches = 1
            print(outputText)


class matchesFinder:
    def __init__(self, listOfFiles, match, printStyle):
        self.listOfFiles = listOfFiles
        self.match = match
        self.op = outputPrinter(match)
        self.printStyle = printStyle

        for filename in self.listOfFiles:
            self.output = self.find(filename)

            if self.output:
                if printStyle == 1:
                    self.op.colorPrint(filename, self.output)
                elif printStyle == 2:
                    self.op.underscorePrint(filename, self.output)
                elif printStyle == 3:
                    self.op.machinePrint(filename, self.output)
                else:
                    self.op.normalPrint(filename, self.output)
            elif self.output == None:
                print("\n\nCan't open file " + colorRedStr + str(filename) + resetStr)
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
                          help="Optional, Highlight matching text with " + colourStr + "color" + resetStr, action='store_true')
    group.add_argument("-u", "--underscore",
                          help="Optional, Print '^' under the matching text", action='store_true')
    group.add_argument("-m", "--machine",
                          help="Optional, Generate machine readable output", action='store_true')

    return parser.parse_args()


def main():
    args = parse_arguments()

    filenames = args.filenames.split(",")
    match = re.compile(args.regexp)
    printStyle = 0
    if args.color:
        printStyle = 1
    elif args.underscore:
        printStyle = 2
    elif args.machine:
        printStyle = 3

    matchesFinder(filenames, match, printStyle)


if __name__ == "__main__":
    main()