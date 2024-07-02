import os
import json
import time
import shutil
import signal
import socket
import tempfile
import functools
import subprocess
from glob import iglob
from textwrap import dedent
from contextlib import contextmanager

import jinja2
from watchdog.observers import Observer
from PIL import Image, ImageDraw, ImageFont
from watchdog.events import FileSystemEventHandler
from playwright.sync_api import sync_playwright, Page


from .common import PRIVATE_DATA_PATH


def iterate_full_data(json_path):
    with open(os.path.join(PRIVATE_DATA_PATH, json_path), encoding='utf-8') as f:
        data = json.load(f)
        for fileitem in data:
            for annotation in fileitem['annotations']:
                for resultitem in annotation['result']:
                    yield resultitem, annotation, fileitem


def get_annotation_labels(item_filter, json_path, json_format):
    assert json_format in ['full', 'min'], f'Unknown json_format: {json_format}'
    is_full_json = json_format == 'full'
    with open(os.path.join(PRIVATE_DATA_PATH, json_path), encoding='utf-8') as f:
        data = json.load(f)
    if is_full_json:
        selected_annotation = None
        for resultitem, annotation, fileitem in iterate_full_data(json_path):
            if item_filter(resultitem):
                assert selected_annotation is None, 'Multiple matching annotations found'
                selected_annotation = annotation
        items = selected_annotation['result']
    else:
        items = [item for item in data if item_filter(item)]
        assert len(items) == 1
        items = items[0]['label']
    assert len(items) > 0
    original_width, original_height = None, None
    res = {}
    for item in items:
        if is_full_json:
            text = item.get('meta', {}).get('text', [])
            label_id = text[0] if len(text) == 1 else None
            label = {
                **item,
                **item['value']
            }
        else:
            assert len(item['rectanglelabels']) == 1
            label_id = item['rectanglelabels'][0]
            label = item
        if label_id:
            assert label_id not in res
            if not original_width:
                original_width = label['original_width']
            else:
                assert original_width == label['original_width']
            if not original_height:
                original_height = label['original_height']
            else:
                assert original_height == label['original_height']
            x = label['x'] * original_width / 100
            y = label['y'] * original_height / 100
            width = label['width'] * original_width / 100
            height = label['height'] * original_height / 100
            assert label['rotation'] == 0
            res[label_id] = {
                'x': x,
                'y': y,
                'width': width,
                'height': height,
            }
    return original_width, original_height, res


def init_draw_labels(item_filter, json_path, json_format, labels, default_label=None, mock=False):
    if not default_label:
        default_label = {}
    original_width, original_height, annotation_labels = get_annotation_labels(item_filter, json_path, json_format)
    res_labels = {}
    for label_id, label in labels.items():
        label = {**annotation_labels[label_id], **default_label, **label}
        label['font_path'] = os.path.join(PRIVATE_DATA_PATH, 'fonts', f'{label["font"]}.ttf')
        if mock:
            label['text'] = 'ללקקףףזזץץ'
        res_labels[label_id] = label
    return original_width, original_height, res_labels


def init_draw_image(output_path, source_file_name, original_width, original_height, source_image=None):
    assert output_path.endswith('.png')
    if not source_image:
        source_image = os.path.join(PRIVATE_DATA_PATH, f'{source_file_name}.png')
    image = Image.open(source_image)
    if original_width is not None:
        assert original_width == image.width
    if original_height is not None:
        assert original_height == image.height
    return ImageDraw.Draw(image), image


def get_bg_pos_rect(x, y, width, height, offset_y):
    bg_pos_rect = (x, y, x + width, y + height)
    if offset_y:
        bg_pos_rect = (bg_pos_rect[0], bg_pos_rect[1] + offset_y, bg_pos_rect[2], bg_pos_rect[3] + offset_y)
    return bg_pos_rect


def draw_bg(draw, bg_pos_rect, bg_color):
    draw.rectangle(bg_pos_rect, fill=bg_color or 'white')


def draw_border(draw, bg_pos_rect, border_color, border_width):
    border_color = border_color or "black"
    border_width = border_width or 1
    draw.rectangle(bg_pos_rect, outline=border_color, width=border_width)
    return border_width


def draw_text(draw, text, font, direction, center, x, y, width, height, x_offset, y_offset, offset_y, color, line_height):
    left, top, right, bottom = font.getbbox(text, direction=direction)
    if line_height:
        y_offset -= bottom - top - line_height
    if center:
        text_pos_xy = (
            x + (width - right + left) / 2 + (x_offset or 0),
            y + (height - bottom + top) / 2 + (y_offset or 0),
        )
    else:
        text_pos_xy = (
            x + width - right + (x_offset or 0),
            y + (y_offset or 0)
        )
    if offset_y:
        text_pos_xy = (text_pos_xy[0], text_pos_xy[1] + offset_y)
    draw.text(text_pos_xy, text, fill=color, font=font, direction=direction)
    return text_pos_xy[0], text_pos_xy[1], right - left, bottom - top


def get_html_page_template():
    return dedent(f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <style>
                @font-face {{
                    font-family: david;
                    src: url('file:///home/ori/israel-mock-data-generator-private-data/fonts/david.ttf') format('truetype');
                }}
                @font-face {{
                    font-family: Arial;
                    src: url('file:///home/ori/israel-mock-data-generator-private-data/fonts/Arial_Bold.ttf') format('truetype');
                    font-weight: bold;
                }}
                @font-face {{
                    font-family: Arial;
                    src: url('file:///home/ori/israel-mock-data-generator-private-data/fonts/Arial.ttf') format('truetype');
                }}
                * {{
                    margin: 0;
                    padding: 0;
                    border-spacing: 0;
                    background-color: transparent;
                }}
            </style>
        </head>
        <body>__BODY__</body>
        </html>
    ''').strip()


@contextmanager
def init_html_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--disable-web-security', '--allow-file-access-from-files', '--no-sandbox'
            ]
        )
        page = browser.new_page()
        yield page
        browser.close()


def draw_html(draw, image, html_page, html, **draw_kwargs):
    width, height = draw_kwargs['width'], draw_kwargs['height']
    x, y = draw_kwargs['x'], draw_kwargs['y']
    x_offset, y_offset = draw_kwargs['x_offset'] or 0, draw_kwargs['y_offset'] or 0
    direction = draw_kwargs['direction'] or 'rtl'
    font, font_size = draw_kwargs['font'], draw_kwargs['font_size']
    page: Page = html_page['page']
    template, tmpdir = html_page['template'], html_page['tmpdir']
    filepath = os.path.join(tmpdir, 'page.html')
    style = {
        'font-family': font,
        'font-size': f'{font_size}px',
        'direction': direction,
    }
    style = '; '.join([f'{k}: {v}' for k, v in style.items()])
    html = template.replace('__BODY__', dedent(f'''
        <div style="{style}">{html}</div>
    ''').strip())
    with open(filepath, 'w') as f:
        f.write(html)
    if draw_kwargs.get('html_debug_file'):
        with open(draw_kwargs['html_debug_file'], 'w') as f:
            f.write(html)
    page.set_viewport_size({'width': int(width), 'height': int(height)})
    page.goto(f"file://{filepath}")
    imagepath = os.path.join(tmpdir, 'screenshot.png')
    page.screenshot(path=imagepath)
    html_image = Image.open(imagepath)
    image.paste(html_image, (int(x) + x_offset, int(y) + y_offset))


def draw_textbox(draw, font_path=None, font_size=None, text=None,
                 color=None, direction='rtl', font=None, offset_y=None,
                 x=None, y=None, width=None, height=None,
                 x_offset=None, y_offset=None, center=None, no_bg=False,
                 border_color=None, border_width=None,
                 html=None, html_page=None,
                 line_height=None, image=None,
                 hooks=None, bg_color=None,
                 **kwargs):
    if not hooks:
        hooks = {}
    hooks = {
        'x_y_width_height': lambda x_, y_, w_, h_: (x_, y_, w_, h_),
        **hooks
    }
    x, y, width, height = hooks['x_y_width_height'](x, y, width, height)
    bg_pos_rect = get_bg_pos_rect(x, y, width, height, offset_y)
    if not no_bg:
        draw_bg(draw, bg_pos_rect, bg_color)
    if border_color or border_width:
        border_width = draw_border(draw, bg_pos_rect, border_color, border_width)
        x_offset = int(x_offset or 0) + border_width
        y_offset = int(y_offset or 0) + border_width
    color = color or (0, 0, 0)
    draw_kwargs = {
        'direction': direction,
        'color': color,
        'x_offset': x_offset,
        'y_offset': y_offset,
        'offset_y': offset_y,
        'center': center,
        'line_height': line_height,
        'x': x,
        'y': y,
        'width': width,
        'height': height,
        **kwargs
    }
    if html:
        draw_kwargs.update({
            'font': font,
            'font_path': font_path,
            'font_size': font_size,
        })
        draw_html(draw, image, html_page, html, **draw_kwargs)
    else:
        if not font or isinstance(font, str):
            font = ImageFont.truetype(font_path, font_size)
        draw_kwargs['font'] = font
        draw_text(draw, text, **draw_kwargs)
    return font


def wait_for_server_start(port):
    start_time = time.time()
    while True:
        try:
            with socket.create_connection(("localhost", port), timeout=1):
                return port
        except OSError:
            if time.time() - start_time > 10:
                raise TimeoutError("Timed out waiting for the server to start")
            time.sleep(0.1)


class JinjaTrackingFilesystemLoader(jinja2.FileSystemLoader):

    def __init__(self, *args, **kwargs):
        self.rendered_templates = set()
        super().__init__(*args, **kwargs)

    def get_source(self, environment, template):
        self.rendered_templates.add(template)
        return super().get_source(environment, template)


def render_htmls(update=False):
    html_path = os.path.join(os.path.dirname(__file__), '..', '.data', 'html')
    shutil_copy_files = []
    if not update:
        shutil.rmtree(html_path, ignore_errors=True)
    os.makedirs(os.path.join(html_path, 'fonts'), exist_ok=True)
    for ext in ['ttf', 'woff']:
        for filename in iglob(os.path.join(PRIVATE_DATA_PATH, f'fonts/*.{ext}')):
            shutil.copy(filename, os.path.join(html_path, 'fonts'))
            shutil_copy_files.append((filename, os.path.join(html_path, 'fonts')))
    os.makedirs(os.path.join(html_path, 'salaries'), exist_ok=True)
    for filename in iglob(os.path.join(PRIVATE_DATA_PATH, 'salaries/*.png')):
        shutil.copy(filename, os.path.join(html_path, 'salaries'))
        shutil_copy_files.append((filename, os.path.join(html_path, 'salaries')))
    loader = JinjaTrackingFilesystemLoader(os.path.join(os.path.dirname(__file__)))
    env = jinja2.Environment(
        loader=loader,
        autoescape=jinja2.select_autoescape()
    )
    global_context = {}
    for template in env.list_templates(filter_func=lambda f: f.endswith('.jinja.html') and not f.split('/')[-1].startswith('_')):
        context = {}
        output_filename = os.path.join(html_path, template.replace('.jinja.html', '.html'))
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
        with open(output_filename, 'w') as f:
            f.write(env.get_template(template).render({**global_context, **context}))
    return html_path, shutil_copy_files, loader.rendered_templates


@contextmanager
def start_python_http_server(watch=False, port=None):
    html_path, shutil_copy_files, rendered_templates = render_htmls()
    if not port:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            port = s.getsockname()[1]
    print(f'Starting server on port {port}')
    server = subprocess.Popen(
        ['python', '-m', 'http.server', str(port)],
        # stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        cwd=html_path
    )
    if watch:
        observer = Observer()
        handler = FileSystemEventHandler()
        handler.on_modified = lambda event: (render_htmls(update=True), print(f'Updated {event.src_path}')) if event.src_path.endswith('.html') else None
        observer.schedule(handler, PRIVATE_DATA_PATH, recursive=True)
        observer.schedule(handler, os.path.dirname(__file__), recursive=True)
        observer.start()
    try:
        yield functools.partial(wait_for_server_start, port)
    finally:
        server.send_signal(signal.SIGINT)
        server.wait()


def save_render_html(output_path, render_path, page, http_server_port, context, width, height, output_scale=0.5, y=0, pdf_output_path=None):
    with tempfile.TemporaryDirectory() as tmpdir:
        page_output_path = os.path.join(tmpdir, 'page.png')
        page.set_viewport_size({'width': width, 'height': height})
        page.goto(f"http://localhost:{http_server_port}/{render_path}")
        if y:
            page.evaluate(f"window.scrollTo(0, {y})")
        for key, value in context.items():
            if isinstance(value, int):
                value = str(value)
            elif isinstance(value, float):
                value = f'{value:.2f}'
            try:
                if isinstance(value, str):
                    inner_html = str(value).replace("'", "\\'").replace("\n", "\\n")
                    if not inner_html:
                        inner_html = '&nbsp;'
                    page.evaluate(f"document.getElementById('{key}').innerHTML = '{inner_html}'")
                elif isinstance(value, dict):
                    dict_config = {}
                    for k in list(value):
                        if k.startswith('_'):
                            dict_config[k[1:]] = value[k]
                            del value[k]
                    if 'empty_value' in dict_config:
                        empty_value = dict_config['empty_value']
                    else:
                        empty_value = '&nbsp;'
                    if value.keys() == {'divs'}:
                        # value['divs'] is a list of strings
                        # need to use page.evaluate to set the innerText of each child of the key to this value by order
                        for i, inner_html in enumerate(value['divs']):
                            inner_html = str(inner_html).replace("'", "\\'")
                            if not inner_html:
                                inner_html = empty_value
                            page.evaluate(f"document.getElementById('{key}').children[{i}].innerHTML = '{inner_html}'")
                    elif value.keys() == {'trs_td_div'} or value.keys() == {'div_trs_td_div'}:
                        for i, tr in enumerate(value.get('trs_td_div') or value.get('div_trs_td_div')):
                            for j, inner_html in enumerate(tr):
                                inner_html = str(inner_html).replace("'", "\\'")
                                if not inner_html:
                                    inner_html = empty_value
                                if value.keys() == {'trs_td_div'}:
                                    page.evaluate(f"document.getElementById('{key}').children[0].children[{i}].children[{j}].children[0].innerHTML = '{inner_html}'")
                                else:
                                    page.evaluate(f"document.getElementById('{key}').children[0].children[0].children[{i}].children[{j}].children[0].innerHTML = '{inner_html}'")
                    else:
                        raise ValueError(f'Unknown context value dict: {value}')
                else:
                    raise ValueError(f'Unknown context value type: {type(value)}')
            except Exception as e:
                raise Exception(f'Error setting context key {key} to value {value}') from e
        page.screenshot(path=page_output_path)
        image = Image.open(page_output_path)
        image = image.resize((int(width*output_scale), int(height*output_scale)))
        image.save(output_path)
        if pdf_output_path:
            assert pdf_output_path.endswith('.pdf')
            image.convert('RGB').save(pdf_output_path)
