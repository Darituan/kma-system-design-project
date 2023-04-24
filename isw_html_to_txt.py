from pyquery import PyQuery
import re
import os

def main():
    directory = 'isw_reports'
    directory_to_write = 'isw_reports_txt'


    def write_to_file(name, data):
        name = name.replace('.html', '.txt')
        f = open(f'{directory_to_write}/{name}', 'w', encoding='utf-8')
        f.write(data)
        f.close()

    if not os.path.exists(directory_to_write):
        os.mkdir(directory_to_write)

    for filename in os.listdir(directory):
        future_name = filename.replace('.html', '.txt')
        if os.path.exists(os.path.join(directory_to_write, future_name)):
            continue
        f = os.path.join(directory, filename)
        with open(f, 'r', encoding='utf-8') as file:
            data = file.read()
            html = data
            pq = PyQuery(html)
            tag = pq('div.field-items')
            text = re.sub(r'\[(\d+)\]', '', tag.text())
            text = text.replace(' ', ' ')
            lines = text.split('\n')
            lines.pop(0)
            indices_to_remove = set()
            for index, line in enumerate(lines):
                if "http" in line:
                    indices_to_remove.add(index)
                if '.png' in line:
                    indices_to_remove.add(index)
                if '.jpg' in line:
                    indices_to_remove.add(index)
                if 'Click here' in line:
                    indices_to_remove.add(index)
            for index in indices_to_remove:
                lines[index] = ''
            lines = list(filter(lambda line: line != '', lines))
            lines = '\n'.join(lines)
            write_to_file(filename, lines)
