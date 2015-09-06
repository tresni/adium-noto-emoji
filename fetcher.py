import urllib
import json
import os
from lxml import etree as ET
from wand.image import Image
import sys

base_url = 'https://github.com/googlei18n/noto-emoji/raw/master/svg/emoji_u{0}.svg'
data = urllib.urlopen('https://github.com/Ranks/emojione/raw/master/emoji.json').read()
emo_json = json.loads(data)

root = 'Noto.AdiumEmoticonSet'

if not os.path.exists(root):
    os.mkdir(root)

if not os.path.isdir(root):
    print "{0} is not a directory...".format(root)
    sys.exit(1)

#if not os.path.isfile(root + img):
plist = ET.Element('plist', {'version': '1.0'})
d = ET.SubElement(plist, 'dict')
ET.SubElement(d, 'key').text = 'AdiumSetVersion'
ET.SubElement(d, 'real').text = '1.0'
ET.SubElement(d, 'key').text = 'Emoticons'
emoticons = ET.SubElement(d, 'dict')

def AddElement(name, emoticon):
    ET.SubElement(emoticons, 'key').text = "{0}.png".format(name)
    emoji = ET.SubElement(emoticons, 'dict')
    ET.SubElement(emoji, 'key').text = 'Name'
    ET.SubElement(emoji, 'string').text = emoticon['name']
    ET.SubElement(emoji, 'key').text = 'Equivalents'
    sub = ET.SubElement(emoji, 'array')
    ET.SubElement(sub, 'string').text = emoticon['shortname']
    for alias in emoticon['aliases']:
        ET.SubElement(sub, 'string').text = alias

for key in emo_json:
    img_path = '{0}/{1}.png'.format(root, key)
    if not os.path.isfile(img_path):
        # Grab SVG turn into 16x16 PNG...
        uni = emo_json[key]['unicode'].lower().replace('-', '_')
        img_url = base_url.format(uni)
        stream = urllib.urlopen(img_url)
        if stream.getcode() != 200:
            stream.close()
            continue
        try:
            with Image(file=stream, format="svg") as img:
                img.resize(18, 18)
                with img.convert('png') as converted:
                    converted.save(filename=img_path)
        except Exception as e:
            print e
        finally:
            stream.close()
        #urllib.urlretrieve(base_url.format('assets/png/{0}.png'.format(emo_json[key]['unicode'])), img_path)

    AddElement(key, emo_json[key])

with open("{0}/Emoticons.plist".format(root), 'w') as fp:
    fp.write(ET.tostring(plist, encoding="UTF-8", xml_declaration=True, pretty_print=True, doctype='<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">'))
