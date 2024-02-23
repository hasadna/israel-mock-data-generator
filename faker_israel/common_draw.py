import os
import json
import time
import signal
import socket
import tempfile
import functools
import subprocess
from textwrap import dedent
from contextlib import contextmanager

from PIL import Image, ImageDraw, ImageFont
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


@contextmanager
def start_python_http_server(path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        port = s.getsockname()[1]
    server = subprocess.Popen(
        ['python', '-m', 'http.server', str(port)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        cwd=path
    )
    try:
        yield functools.partial(wait_for_server_start, port)
    finally:
        server.send_signal(signal.SIGINT)
        server.wait()


def save_render_html(path, template_name, page, http_server_port, context, width, height, output_scale=0.5, y=0):
    with tempfile.TemporaryDirectory() as tmpdir:
        page_output_path = os.path.join(tmpdir, 'page.png')
        page.set_viewport_size({'width': width, 'height': height})
        page.goto(f"http://localhost:{http_server_port}/israel-mock-data-generator/faker_israel/{template_name}.html")
        if y:
            page.evaluate(f"window.scrollTo(0, {y})")
        for key, value in context.items():
            value = str(value).replace("'", "\\'")
            page.evaluate(f"document.getElementById('{key}').innerText = '{value}'")
        page.screenshot(path=page_output_path)
        # resize the image to the desired size
        image = Image.open(page_output_path)
        image = image.resize((int(width*output_scale), int(height*output_scale)))
        image.save(path)
