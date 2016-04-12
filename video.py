from __future__ import unicode_literals
from docutils import nodes
from docutils.parsers.rst import directives, Directive


class Video(Directive):
    """ Embed direct video in posts

    Based on the YouTube video plugin by Kura:
    https://github.com/kura/pelican_youtube

    Usage:
    .. video:: video.m4v (or other supported by browsers)
        :width: 640
        :height: 480
        :srt: webtt file
    """
    required_arguments = 1
    optional_arguments = 3
    option_spec = {
        'width': directives.positive_int,
        'height': directives.positive_int,
        'srt': directives.path
    }

    final_argument_whitespaces = False
    has_content = False

    def run(self):
        video_src = self.arguments[0].strip()
        width = None
        height = None
        srt = None

        if 'width' in self.options:
            width = self.options['width']

        if 'height' in self.options:
            height = self.options['height']

        if 'srt' in self.options:
            srt = self.options['srt']
        else:
            srt = None

        video_block = '<video controls '
        if width is not None:
            video_block += 'width="{} "'.format(width)
        if height is not None:
            video_block += 'height="{}"'.format(height)
        video_block += '>'

        src_block = '    <source src="{}"/>'.format(video_src)
        if srt is not None:
            srt_block = '    <track kind="subtitles" srclang="en" ' \
                        'src="{}" default/>'.format(srt)

        output = [
            nodes.raw('', video_block, format='html'),
            nodes.raw('', src_block, format='html')]
        if srt is not None:
            output.append(nodes.raw('', srt_block, format='html'))
        output.append(nodes.raw('', "Your browser doesn't support "
                                "<code>video</code> directive", format='html'))
        output.append(nodes.raw('', '</video>', format='html'))

        return output


def register():
    directives.register_directive('video', Video)
