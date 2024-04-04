import pathlib
import re
import sys

def getDependencies(file):
    ret = set()
    with open(file) as f:
        name = file.parent.parent.name + '/' + file.parent.name
        s = f.read()
        pattern = re.compile("^[RB]?(DEPEND=\")(.*?)(\")", re.MULTILINE | re.DOTALL)
        depends = re.findall(pattern, s)
        for depend in depends:
            if not depend:
                continue
            packages = re.findall("([a-zA-z0-9\-]+\/[a-zA-Z0-9\-\+]+)(\-[-0-9\.]*)?", depend[1])
            for package in packages:
                if (name == package[0]):
                    continue
                if (package[0][len(package[0]) - 1] == '-'):
                    ret.add(package[0][:len(package[0]) - 1])
                elif (package[0][len(package[0]) - 2] == '-'):
                    ret.add(package[0][:len(package[0]) - 2])
                elif (package[0][len(package[0]) - 3] == '-'):
                    ret.add(package[0][:len(package[0]) - 3])
                else:
                    ret.add(package[0])
    return list(ret)


def main():
    packages = set()
    dependencies = dict()
    for item in pathlib.Path("./gentoo").rglob("*.ebuild"):
        name = item.parent.parent.name + '/' + item.parent.name
        if (name in packages):
            continue
        packages.add(name)

        dependencies[name] = getDependencies(item)

    dependency_counts = {}
    for package in packages:
        dependency_counts[package] = 0

    stack = list(packages)
    while len(stack) > 0 and len(stack) < 1000000000:
        package = stack.pop()
        if package in dependencies:
            for i in dependencies[package]:
                if i in dependencies:
                    dependency_counts[i] += 1

    view = [(v,k) for k,v in dependency_counts.items()]
    view.sort(reverse=True)
    for v,k in view:
        print("%s : %d" % (k,v))



main()
