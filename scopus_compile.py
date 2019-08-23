import re
import sublime_plugin

from sublime import Region
from sublime import Selection


class CompileScopusQueryCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        selection = self.view.sel()
        new_selection = Selection(12)

        # splitting lines over line breaks
        for region in selection:
            text = self.view.substr(region)
            # adding a virtual line break before the region
            # because we take the regions between line breaks
            line_break_positions = [-1]
            for i in range(len(text)):
                if text[i] == '\n':
                    line_break_positions.append[i]

                # If region doesn't end on a line break,
                # adding a virtual line break after the
                # last character (same reason as before)
                if text[-1] != '\n':
                    line_break_positions.append(len(text) + 1)

            # isolating all the regions between line breaks
            for i in range(len(line_break_positions) - 1):
                new_selection.add(Region(
                    region.a + line_break_positions[i] + 1,
                    region.a + line_break_positions[i + 1]))

        # overwriting old selection
        selection = new_selection
        new_selection = Selection(13)

        # unselecting comments
        for region in selection:
            text = self.view.substr(region)
            comment_start = text.find('%')
            if comment_start != -1:
                new_selection.add(Region(
                    region.a,
                    region.a + comment_start))
            else:
                new_selection.add(region)

        # overwriting old selection
        selection = new_selection

        # starting the compilation process
        line_ref_pattern = re.compile(r"#[0-9]+")
        for region in selection:
            text = self.view.substr(region)
            current_line_number = self.view.rowcol(region.a)[0]
            # getting each occurence of the form "#12"
            # which references a line in the file
            reference = line_ref_pattern.search(text)
            while reference is not None:
                # getting the referenced line
                target_line_number = int(
                    text[reference.start():reference.end()]) - 1

                if target_line_number == current_line_number:
                    raise RecursionError(
                        "Self-referencing query would have caused infinite recursion.")

                target_line_start = self.view.text_point(target_line_number,
                                                         0)
                target_line_end = self.view.text_point(
                    target_line_number + 1, 0) - 1

                # replacing the reference with its target
                text = (text[:reference.start()] +
                        self.view.substr(Region(target_line_start,
                                                target_line_end)) +
                        text[reference.end():])
                reference = line_ref_pattern.search(text)
            print(text)
            self.view.replace(edit, region, text)

        # caret_pos = selection[-1].b
