import re
import sublime_plugin

from sublime import Region


class CompileScopusQueryCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        print("running")
        selection = self.view.sel()
        new_selection = []

        # splitting lines over line breaks
        print("splitting lines over line breaks")
        for region in selection:
            text = self.view.substr(region)
            print(text)
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

            print("line_break_positions: ", [self.view.rowcol(i) for i in line_break_positions])
            # isolating all the regions between line breaks
            for i in range(len(line_break_positions) - 1):
                print(self.view.rowcol(region.a + line_break_positions[i] + 1),
                      self.view.rowcol(region.a + line_break_positions[i + 1]))
                new_selection.append(Region(
                    region.a + line_break_positions[i] + 1,
                    region.a + line_break_positions[i + 1]))

        # overwriting old selection
        selection.clear()
        selection.add_all(new_selection)
        new_selection = []

        # unselecting comments
        print("unselecting comments")
        for region in selection:
            new_selection.append(self.remove_comments(region))

        # overwriting old selection
        selection.clear()
        selection.add_all(new_selection)

        # starting the compilation process
        print("compiling")
        line_ref_pattern = re.compile(r"#[0-9]+")
        for region in selection:
            text = self.view.substr(region)
            print("before: ", text)
            current_line_number = self.view.rowcol(region.a)[0]
            # getting each occurence of the form "#12"
            # which references a line in the file
            reference = line_ref_pattern.search(text)
            while reference is not None:
                # getting the referenced line
                target_line_number = int(
                    text[reference.start() + 1:reference.end()]) - 1

                if target_line_number == current_line_number:
                    raise RecursionError(
                        "Self-referencing query would have caused infinite recursion.")

                target_line_start = self.view.text_point(target_line_number,
                                                         0)
                target_line_end = self.view.text_point(
                    target_line_number + 1, 0) - 1

                # replacing the reference with its target
                text = (text[:reference.start()] + '(' +
                        self.view.substr(Region(target_line_start,
                                                target_line_end)) +
                        ')' + text[reference.end():])
                reference = line_ref_pattern.search(text)
            print("after: ", text)
            self.view.replace(edit, region, text)

        # caret_pos = selection[-1].b

    def remove_comments(self, region):
        text = self.view.substr(region)
        print(text)
        comment_start = text.find('%')
        if comment_start != -1:
            return Region(region.a, region.a + comment_start)
        else:
            return region
