import re
import sublime_plugin

from sublime import Region


class CompileScopusQueryCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        # compiling ahead of time regex for recognizing query references
        self.line_ref_pattern = re.compile(r"#[0-9]+")

        selection = self.view.sel()
        new_selection = []

        # splitting lines over line breaks
        for region in selection:
            region = self.fix_empty_region(region)
            new_selection.extend(self.split_line_breaks(region))

        # overwriting old selection
        selection.clear()
        selection.add_all(new_selection)
        new_selection = []

        # unselecting comments
        for region in selection:
            region = self.fix_empty_region(region)
            new_selection.append(self.remove_comments(region))

        # overwriting old selection
        selection.clear()
        selection.add_all(new_selection)

        # starting the compilation process
        for region in selection:
            region = self.fix_empty_region(region)
            self.view.replace(edit, region, self.compile_query(region))

    def compile_query(self, region):
        text = self.view.substr(region)
        current_line_number = self.view.rowcol(region.begin())[0]
        # getting each occurence of the form "#12"
        # which references a line in the file
        reference = self.line_ref_pattern.search(text)
        while reference is not None:
            # getting the referenced line
            target_line_number = int(
                text[reference.start() + 1:reference.end()]) - 1

            if target_line_number == current_line_number:
                raise RecursionError(
                    "Self-referencing query would have\
                 caused infinite recursion.")

            target_line_start = self.view.text_point(target_line_number, 0)
            target_line_end = self.view.text_point(
                target_line_number + 1, 0) - 1

            # replacing the reference with its target
            text = (text[:reference.start()] + '(' +
                    self.view.substr(
                        self.remove_comments(
                            Region(target_line_start,
                                   target_line_end))) +
                    ')' + text[reference.end():])
            reference = self.line_ref_pattern.search(text)
        return text

    def fix_empty_region(self, region):
        if region.a != region.b:
            return region
        else:
            caret_pos = self.view.rowcol(region.a)
            return Region(
                self.view.text_point(caret_pos[0], 0),
                self.view.text_point(caret_pos[0] + 1, 0) - 1)

    def remove_comments(self, region):
        text = self.view.substr(region)
        comment_start = text.find('%')
        if comment_start != -1:
            return Region(region.begin(), region.begin() + comment_start)
        else:
            return region

    def split_line_breaks(self, region):
        text = self.view.substr(region)
        # adding a virtual line break before the region
        # because we take the regions between line breaks
        line_break_positions = [-1]
        for i in range(len(text)):
            if text[i] == '\n':
                line_break_positions.append(i)

            # If region doesn't end on a line break,
            # adding a virtual line break after the
            # last character (same reason as before)
        if text[-1] != '\n':
            line_break_positions.append(len(text) + 1)

        new_regions = []
        # isolating all the regions between line breaks
        for i in range(len(line_break_positions) - 1):
            new_regions.append(Region(
                region.begin() + line_break_positions[i] + 1,
                region.begin() + line_break_positions[i + 1]))

        return new_regions
