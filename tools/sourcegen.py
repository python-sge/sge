#!/usr/bin/env python

# SGE Source Generator
# Copyright (C) 2013 Julian Marchant <onpon4@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

TEMPLATE = """
#!/usr/bin/env python

# {name}
{license}

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

{modules}

import sge

{constants}

{globalvars}


{classes}


{functions}


if __name__ == '__main__':
    main()
""".strip()

MAIN_FUNCTION_TEMPLATE = """
# Create Game object
{game_object}

# Load sprites
{sprites}

# Load backgrounds
{backgrounds}

# Load fonts
{fonts}

# Load sounds
{sounds}

# Load music
{music}

# Create objects
{objects}

# Create views
{views}

# Create rooms
{rooms}

sge.game.start()
""".strip()


class ClassDefinition(object):

    """Class definition class.

    This class is used for class definition objects used for creating
    source files.

    """

    def __init__(self, class_name, parent="object", indentation=0,
                 class_attributes={}, methods=(), class_methods=(),
                 static_methods=()):
        self.class_name = class_name
        self.parent = parent
        self.indentation = indentation
        self.class_attributes = class_attributes
        self.methods = methods
        self.class_methods = class_methods
        self.static_methods = static_methods

    @property
    def code_text(self):
        header_indent = ' ' * self.indentation
        code_indent = ' ' * (self.indentation + 4)

        for method in self.methods + self.class_methods + self.static_methods:
            method.indentation = self.indentation + 4

        header_text = "{0}class {1}({2}):".format(header_indent,
                                                  self.class_name, self.parent)

        attribute_texts = []
        for a in self.class_attributes:
            text = "{0}{1} = {2}".format(code_indent, a,
                                         self.class_attributes[a])
        attribute_text = '\n'.join(attribute_texts)

        all_texts = [header_text, attribute_text]

        for method in self.methods:
            all_texts.append(method.code_text)

        for method in self.class_methods:
            text = '{0}@classmethod\n{1}'.format(code_indent, method.code_text)
            all_texts.append(text)

        for method in self.static_methods:
            text = '{0}@staticmethod\n{1}'.format(code_indent,
                                                  method.code_text)
            all_texts.append(text)

        return '\n\n'.join(all_texts)


class FunctionDefinition(object):

    """Class definition class.

    This class is used for function definition objects used for creating
    source files.  It is also used for methods.

    """

    def __init__(self, name, args=(), indentation=0, code="pass"):
        self.name = name
        self.args = args
        self.indentation = indentation
        self.code = code

    @property
    def code_text(self):
        code_lines = self.code.splitlines()
        new_code_lines = []
        header_indent = ' ' * self.indentation
        code_indent = ' ' * (self.indentation + 4)
        for line in code_lines:
            if line.strip():
                new_code_lines.append(code_indent + line)
            else:
                new_code_lines.append('')
        code_text = '\n'.join(new_code_lines)

        args_text = ', '.join(self.args)

        return '{0}{1}({2}):\n{3}'.format(header_indent, self.name, args_text,
                                          code_text)


class ObjectDefinition(object):

    """Object definition class.

    This class is used for object definition objects used for defining
    objects to be created.

    """

    def __init__(self, classname, assignto=None, args=(), kwargs={}):
        self.classname = classname
        self.assignto = assignto
        self.args = args
        self.kwargs = kwargs

    @property
    def code_text(self):
        if self.assignto is not None:
            assign_text = '{0} = '.format(self.assignto)
        else:
            assign_text = ''

        kwargslist = []
        for i in self.kwargs:
            kwargslist.append('{0}={1}'.format(i, self.kwargs[i]))
        return "{0}{1}({2})".format(assign_text, self.classname,
                                    ', '.join(self.args + tuple(kwargslist)))


def create_source_file(name, license_header='', modules=(), constants={},
                       globalvars={}, classes=(), functions=(),
                       game_object=ObjectDefinition('sge.Game'), sprites=(),
                       backgrounds=(), fonts=(), sounds=(), music=(),
                       objects=(), views=(), rooms=()):
    license_lines = license_header.splitlines()
    commented_license_lines = []
    for line in license_lines:
        commented_license_lines.append('# ' + line)
    license_header_text = '\n'.join(commented_license_lines)

    modules_lines = []
    for module in modules:
        modules_lines.append('import {0}'.format(module))
    modules_text = '\n'.join(modules_lines)

    constants_lines = []
    for c in constants:
        constants_lines.append('{0} = {1}'.format(c, constants[c]))
    constants_text = '\n'.join(constants_lines)

    globalvars_lines = []
    for v in globalvars:
        globalvars_lines.append('{0} = {1}'.format(v, globalvars[v]))
    globalvars_text = '\n'.join(globalvars_lines)

    classes_strings = []
    for cls in classes:
        classes_strings.append(cls.code_text)
    classes_text = '\n\n\n'.join(classes_strings)

    functions_strings = []
    for function in functions:
        functions_strings.append(function.code_text)

    game_object_text = game_object.code_text

    sprites_lines = []
    for sprite in sprites:
        sprites_lines.append(sprite.code_text)
    sprites_text = '\n'.join(sprites_lines)

    backgrounds_lines = []
    for background in backgrounds:
        backgrounds_lines.append(background.code_text)
    backgrounds_text = '\n'.join(backgrounds_lines)

    fonts_lines = []
    for font in fonts:
        fonts_lines.append(font.code_text)
    fonts_text = '\n'.join(fonts_lines)

    sounds_lines = []
    for sound in sounds:
        sounds_lines.append(sound.code_text)
    sounds_text = '\n'.join(sounds_lines)

    music_lines = []
    for piece in music:
        music_lines.append(piece.code_text)
    music_text = '\n'.join(music_lines)

    objects_lines = []
    for obj in objects:
        objects_lines.append(obj.code_text)
    objects_text = '\n'.join(objects_lines)

    views_lines = []
    for view in views:
        views_lines.append(view.code_text)
    views_text = '\n'.join(views_lines)

    rooms_lines = []
    for room in rooms:
        rooms_lines.append(room.code_text)
    rooms_text = '\n'.join(rooms_lines)

    main_function_text = MAIN_FUNCTION_TEMPLATE.format(
        game_object=game_object_text, sprites=sprites_text,
        backgrounds=backgrounds_text, fonts=fonts_text, sounds=sounds_text,
        music=music_text, objects=objects_text, views=views_text,
        rooms=rooms_text)
    main_function = FunctionDefinition('main', code=main_function_text)

    functions_strings.append(main_function.code_text)
    functions_text = '\n\n\n'.join(functions_strings)

    return TEMPLATE.format(
        name=name, license=license_header, modules=modules_text,
        constants=constants_text, globalvars=globalvars_text,
        classes=classes_text, functions=functions_text)


if __name__ == '__main__':
    print(create_source_file('Dummy Game'))
