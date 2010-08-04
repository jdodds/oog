#!/usr/bin/env python
"""Generate an orgmode outline for taking notes, based off the contents of a
pdf. Currently has only been tested on "Version Control With Git" by
Oreilly. Chances are that it does NOT work on other pdfs without finagling.

Hopefully this will become a fuller-fledged orgmode outline generator in the
future.
"""


def find_headings(path_to_pdf):
    """Return a list of dicts representing chapter headings in the file
    specified by path_to_pdf
    """
    def check_maker(reg, cache):
        """Generate a function for checking a line against a regex, using a
        cache
        """
        def ret(line):
            """Check to see if line has an item that has been seen before
            """
            match = reg.search(line)
            if match:
                mat = match.group(0)
                if mat not in cache:
                    cache.append(mat)
                    return False
                return True
            return False
        return ret

    import re
    chapter = re.compile(r'\(chap-([^)]+)')
    section = re.compile(r'\(sec-([^)]+)')

    seen_chapters = []
    seen_sections = []

    c_match = check_maker(chapter, seen_chapters)
    s_match = check_maker(section, seen_sections)

    def seen(line):
        """Check to see if line has a chapter or section that has been seen
        before.
        """
        return c_match(line) or s_match(line)

    data = []
    lines = []
    with open(path_to_pdf, "rb") as pdf:
        for line in pdf:
            if chapter.search(line) and section.search(line):
                lines.extend([l for l in line.split(">>")
                              if not seen(l)])
    for line in lines:
        if chapter.search(line):
            chap = chapter.search(line).group(1)
            data.append([chap, []])
        elif section.search(line):
            sec = section.search(line).group(1)
            data[-1][1].append(sec)

    return data


def generate_org_file(headings):
    """Generate an orgmode outline given associative arrays of headings.
    """
    out = []
    for chapter, sections in headings:
        out.append('* ' + chapter)
        for section in sections:
            out.append('** ' + section)
    return "\n".join(out)


if __name__ == '__main__':
    import sys
    print generate_org_file(find_headings(sys.argv[1]))
