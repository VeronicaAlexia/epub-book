import os
from .template import container, mimetype
from HbookerAPI import Vars


def join_path(*args):
    return '/'.join(args)


def set_epub_cache_file():
    for _name in os.listdir(join_path("HbookerAPI", 'template')):
        if not os.path.isfile(join_path("HbookerAPI", 'template', _name)):
            if not os.path.exists(Vars.config_dir + '/' + _name):
                os.makedirs(Vars.config_dir + '/' + _name)
    for _name in os.listdir(join_path("HbookerAPI", 'template', 'OEBPS')):
        if not os.path.isfile(join_path("HbookerAPI", 'template', 'OEBPS', _name)):
            if not os.path.exists(join_path(Vars.config_dir, "OEBPS", _name)):
                os.makedirs(join_path(Vars.config_dir, "OEBPS", _name))
    with open(join_path(Vars.config_dir, 'mimetype'), 'w') as f:
        f.write(mimetype)
    # print(Vars.config_dir, 'META-INF', 'container.xml')
    with open(join_path(Vars.config_dir, 'META-INF', 'container.xml'), 'w') as f:
        f.write(container)
