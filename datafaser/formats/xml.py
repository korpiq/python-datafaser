import xml.etree.ElementTree as ET


def read(stream):
    stream_content = ''.join(stream.read())
    root_element = ET.fromstring(stream_content)
    return element_to_structure(root_element)


def write(data, stream):
    root_element = structure_to_element(data)
    #root_element = ET.Element('Foo', attrib={'key':'value'})
    #root_element.text = '\nbody text\n'
    xml_string = ET.tostring(root_element, encoding='unicode')
    stream.write(xml_string)
    stream.write('\n')


def element_to_structure(element):
    if isinstance(element, ET.Element):
        content = []
        if element.text:
            content.append(element.text)
        for subelement in element:
            content.append(element_to_structure(subelement))
            if subelement.tail:
                content.append(subelement.tail)
        return {
            element.tag: {
                'attributes': element.attrib,
                'content': content
            }
        }
    else:
        return element


def structure_to_element(data_dict):
    builder = ET.TreeBuilder()
    build_xml(data_dict, builder)
    return builder.close()


def build_xml(data_dict, builder):
    tag_name = list(data_dict.keys())[0]
    tag = data_dict[tag_name]
    builder.start(tag_name, tag['attributes'])

    for item in tag['content']:
        if isinstance(item, dict):
            structure_to_element(item, builder)
        else:
            builder.data(item)

    builder.end(tag_name)

