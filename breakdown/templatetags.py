""" 
Breakdown.py - 2011 Concentric Sky

Lightweight jinja2 template prototyping server with support for
some custom template tags

Copyright 2011 Concentric Sky, Inc. 

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import breakdown
from breakdown.settings import STATIC_URL
import jinja2
import markupsafe
import os
import random


__all__ = ['image', 'greeking']

Markup = markupsafe.Markup
min_func = min
max_func = max
env = jinja2.Environment()


def image(cache_path, width, height):
    """ Generate a custom-sized sample image """
    # Create unique path
    size = (width, height)
    filename = '%sx%s.png' % (width, height)
    path = os.path.join(cache_path, filename)

    # Check if image has already been created
    if not os.path.exists(path):
        # Generate new image
        sample = breakdown.pkg_path('img/sample.png')
        if not os.path.exists(sample):
            return Markup(u'<img/>')
        else:
            try:
                # Try scaling the image using PIL
                import Image
                source = Image.open(sample)
                scaled = source.resize(size, Image.BICUBIC)
                scaled.save(path)
            except ImportError:
                # If we couldnt find PIL, just copy the image
                inf = open(sample, 'rb')
                outf = open(path, 'wb')
                outf.write(inf.read())

    return Markup(u'<img src="%s%s">' % (STATIC_URL, filename))


def greeking(mode=None, min=50, max=100):
    """ Generate a block of various HTML text """
    # Get a blob of lipsum
    minimum = max_func(min, 6*4)
    maximum = max_func(max, minimum+1)
    blob = env.globals['lipsum'](html=False, n=1, min=minimum, max=maximum).split(' ')

    # Wrap text in HTML elements at random points
    wrappers = [
        ('<strong>', '</strong>'),
        ('<em>', '</em>'),
        ('<code>', '</code>'),
        ('<a href="#">', '</a>'),
    ]
    random.shuffle(wrappers)
    thresh = 5
    pointers = random.sample(xrange(len(blob)/thresh), len(wrappers))
    for i, ptr in enumerate(pointers):
        ptr = ptr * thresh
        length = random.randint(2, thresh)
        blob[ptr] = wrappers[i][0] + blob[ptr]
        blob[ptr+length] = wrappers[i][1] + blob[ptr+length]

    html = '<p>' + ' '.join(blob) + '</p>'

    # Generate random lists
    lists = []
    for type in ('ul', 'ol'):
        items = []
        for i in range(random.randint(3, 4)):
            items.append('<li>%s</li>' % env.globals['lipsum'](html=False, n=1, min=5, max=10))
        lists.append(items)

    html += """
    <ul>
        %s
    </ul>

    <ol>
        %s
    </ol>
    """ % ('\n'.join(lists[0]), '\n'.join(lists[1]))

    return Markup(unicode(html))
