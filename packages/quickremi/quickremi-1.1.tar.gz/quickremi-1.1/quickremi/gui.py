import remi.gui as tk
from datetime import datetime
import pandas as pd
import pytz
from functools import partial


class GUI:

    def __init__(self):
        self.dt = ''
        self.tm = ''
        self.text_inputs = {}

    # ------------------------------------ INITIALIZER FUNCTIONS ------------------------------------------- ]

    def create_label(self, frame, H, W, L, T, text='.', bg='white', fg='black', fw='normal', ff='calibri',
                     align='center', justify='center', display='grid', bd_style='None', bd_radius='0px',
                     position='absolute', px=False, fs=0.65, margin='0px', bd_width='0px', bd_color='black',
                     overflow='auto', ta='center', hover='', alpha=1.0, wm='horizontal-tb', lh='-1px',
                     ac='center'):

        '''
        Author Aru Raghuvanshi
        :param frame: container object
        :param H: float: 0 to 100
        :param W: float: 0 to 100
        :param L: float: 0 to 100
        :param T: float: 0 to 100
        :param text: str
        :param bg: str: label color, css colours or hex codes
        :param fg: str: text color, css colours or hex codes
        :param fw: str: font weight (bold, normal)
        :param ff: str: font family ('calibri')
        :param align: str: default 'center'
        :param ac: str: default 'center' align content one of 'center', 'flex-start', 'flex-end'
        :param justify: str: default 'center' [flex-start, flex-end, center, space-between, space-around]
        :param display: str: default 'grid' [inline, grid, block, contents, flex, inline-flex, inline-block]
        :param bd_style: str : default 'None' (solid, dotted, dashed)
        :param bd_radius: str: default '0px'
        :param position: str: default 'absolute'
        :param px: bool : default False
        :param fs: float: font-size variable width default 0.65
        :param margin: str: default '0px'
        :param bd_width: str: default '0px'
        :param bd_color: str: default 'black'
        :param overflow: str: default 'auto' - adds scrollbar in case of overflowing content
        :param ta: str: text align : default 'center' one of [left, right, center, justify, none]
        :param hover: str: hover text when mouse over the label
        :param alpha: float: alpha of the colour of the label (0 to 1)
        :param wm: str: default 'horizontal-tb' (one of 'vertical-rl', 'vertical-lr', 'horizontal-tb')
        :param lh: str: line height or spacing between lines in px (default=-1')
        :return: label widget
        '''

        lbl = tk.Label(text=text)
        lbl.variable_name = 'lbl'
        if px:
            lbl.css_height = str(f'{H}px')
            lbl.css_width = str(f'{W}px')
            lbl.css_left = str(f'{L}px')
            lbl.css_top = str(f'{T}px')
            lbl.css_font_size = str(f'{fs}px')
        else:
            lbl.css_height = str(f'{H}%')
            lbl.css_width = str(f'{W}%')
            lbl.css_left = str(f'{L}%')
            lbl.css_top = str(f'{T}%')
            lbl.css_font_size = str(f'{fs}vw')
        lbl.attributes['title'] = hover
        lbl.css_margin = margin
        # lbl.css_font_size = fs
        lbl.css_background_color = bg
        lbl.css_color = fg
        lbl.css_align_self = align
        lbl.css_align_content = ac
        lbl.css_align_items = align
        lbl.css_display = display
        lbl.css_position = position
        lbl.css_overflow = overflow
        lbl.css_justify_content = justify
        lbl.css_border_style = bd_style
        lbl.css_border_width = bd_width
        lbl.css_border_radius = bd_radius
        lbl.css_border_color = bd_color
        lbl.css_font_family = ff
        lbl.css_font_weight = fw
        lbl.css_text_align = ta
        lbl.css_opacity = alpha
        lbl.css_writing_mode = wm
        lbl.css_line_height = lh

        frame.append(lbl)
        return lbl


    def create_button(self, frame, H, W, L, T, command=None, text=' ', bg='navyblue', fg='white', fw='normal',
                      align='center', justify='space-around', fs=0.65, bd_width='0px', ff='calibri', bd_color='black',
                      display='inline', position='absolute', px=False, bd_style='none', bd_radius='0px', bidx=None,
                      overflow='auto', ta='center', hover='', alpha=1.0, wm='horizontal-tb', ac='center'):

        '''
        Author Aru Raghuvanshi
        :param frame: container object
        :param H: float: 0 to 100
        :param W: float: 0 to 100
        :param L: float: 0 to 100
        :param T: float: 0 to 100
        :param command: func: function to execute on button press
        :param text: str:
        :param bg: str: label color, css colours or hex codes
        :param fg: str: text color, css colours or hex codes
        :param fw: str: font weight (bold, normal)
        :param ff: str: font family ('calibri')
        :param ac: str: align content one of 'center', 'flex-start', 'flex-end'
        :param align: str: default 'center'
        :param justify: str: default 'center' (same as label)
        :param display: str: default 'grid'
        :param bd_style: str : default 'None' (solid, dotted, dashed)
        :param bd_radius: str: default '0px'
        :param position: str: default 'absolute'
        :param px: bool: default False
        :param fs: float: font-size variable width default 0.65
        :param margin: str: default '0px'
        :param bd_width: str: default '0px'
        :param bd_color: str: default 'black'
        :param overflow: str: default 'auto' - adds scrollbar in case of overflowing content
        :param ta: str: text align : default 'center' (same as label)
        :param hover: str: hover text when mouse over the button
        :param alpha: float: alpha of the colour of the label (0 to 1)
        :param wm: str: writing mode, default 'horizontal-tb' (one of 'vertical-rl', 'vertical-lr', 'horizontal-tb')
        :return: Button widget
        '''

        btn = tk.Button(text=text)

        if px:
            btn.variable_name = bidx
            btn.css_height = str(f'{H}px')
            btn.css_width = str(f'{W}px')
            btn.css_left = str(f'{L}px')
            btn.css_top = str(f'{T}px')
            btn.css_font_size = str(f'{fs}px')
        else:
            btn.variable_name = 'btn'
            btn.css_height = str(f'{H}%')
            btn.css_width = str(f'{W}%')
            btn.css_left = str(f'{L}%')
            btn.css_top = str(f'{T}%')
            btn.css_font_size = str(f'{fs}vw')
        btn.attributes['title'] = hover
        btn.css_background_color = bg
        btn.css_color = fg
        btn.css_align_self = align
        btn.css_align_content = ac
        btn.css_align_items = align
        btn.css_display = display
        btn.css_justify_content = align
        btn.css_position = position
        btn.css_justify_content = justify
        btn.css_border_style = bd_style
        btn.css_border_width = bd_width
        btn.css_border_radius = bd_radius
        btn.css_border_color = bd_color
        btn.css_overflow = overflow
        btn.css_font_weight = fw
        btn.css_font_family = ff
        btn.css_text_align = ta
        btn.css_opacity = alpha
        btn.css_writing_mode = wm
        btn.onclick.do(command)
        frame.append(btn)
        return btn


    def create_uploader(self, frame, H, W, L, T, filename, bg='navyblue', fg='black',
                        align='center', justify='space-around', command_succ=None, command_fail=None,
                        display='inline', position='absolute', px=False, bd_style='None', bd_radius='0px',
                        bd_color='black', bd_width='0px', fs=0.65):

        '''
         Author Aru Raghuvanshi
        :param frame: container object
        :param H: float: 0 to 100
        :param W: float: 0 to 100
        :param L: float: 0 to 100
        :param T: float: 0 to 100
        :param filename : str: path of file to be uploaded
        :param bg: str : label color, css colours or hex codes
        :param fg: str : text color, css colours or hex codes
        :param fs: float: font size
        :param align: str: default 'center'
        :param justify: str: default 'center'
        :param display: str: default 'grid'
        :param bd_style: str : default 'None' (solid, dotted, dashed)
        :param bd_radius: str: default '0px'
        :param position: str: default 'absolute'
        :param px: bool : default False
        :param bd_width: str: default '0px'
        :param bd_color: str: default 'black'
        :param command_succ: function to run on successful upload
        :param command_fail: function to run on failed upload
        :return: Uploader widget
        '''

        btn = tk.FileUploader(savepath=filename)

        if px:
            btn.variable_name = 'upl'
            btn.css_height = str(f'{H}px')
            btn.css_width = str(f'{W}px')
            btn.css_left = str(f'{L}px')
            btn.css_top = str(f'{T}px')
            btn.css_font_size = str(f'{fs}px')
        else:
            btn.variable_name = 'btn'
            btn.css_height = str(f'{H}%')
            btn.css_width = str(f'{W}%')
            btn.css_left = str(f'{L}%')
            btn.css_top = str(f'{T}%')
            btn.css_font_size = str(f'{fs}vw')
        btn.css_background_color = bg
        btn.css_color = fg
        btn.css_align_self = align
        btn.css_align_content = align
        btn.css_align_items = align
        btn.css_display = display
        btn.css_justify_content = align
        btn.css_position = position
        btn.css_justify_content = justify
        btn.css_border_style = bd_style
        btn.css_border_width = bd_width
        btn.css_border_radius = bd_radius
        btn.css_border_color = bd_color
        frame.append(btn)
        btn.onsuccess.do(command_succ)
        btn.onfailed.do(command_fail)
        return btn


    def create_container(self, frame, H, W, L, T, bg='whitesmoke', fg='black', bd_radius='0px', bd_style='None',
                         align='center', justify='space-around', overflow='auto', fs=0.7, ac='center',
                         display='space-around', position='absolute', px=False, bd_width='0px', bd_color='black'):

        '''
        Author Aru Raghuvanshi
        :param frame: container object
        :param H: float: 0 to 100
        :param W: float: 0 to 100
        :param L: float: 0 to 100
        :param T: float: 0 to 100
        :param bg: str : label color, css colours or hex codes
        :param fg: str : text color, css colours or hex codes
        :param ac: str: default 'center' align content one of 'center', 'flex-start', 'flex-end'
        :param align: str: default 'center'
        :param justify: str: default 'center'
        :param display: str: default 'grid'
        :param bd_style: str : default 'None' (solid, dotted, dashed)
        :param bd_radius: str: default '0px'
        :param position: str: default 'absolute'
        :param px: bool : default False
        :param fs: float: font-size variable width default 0.8
        :param bd_width: str: default '0px'
        :param bd_color: str: default 'black'
        :param overflow: str: default 'auto' - adds scrollbar in case of overflowing content
        :return: Container widget
        '''

        btn = tk.Container()
        if px:
            btn.variable_name = 'ctn'
            btn.css_height = str(f'{H}px')
            btn.css_width = str(f'{W}px')
            btn.css_left = str(f'{L}px')
            btn.css_top = str(f'{T}px')
            btn.css_font_size = str(f'{fs}px')
        else:
            btn.variable_name = 'btn'
            btn.css_height = str(f'{H}%')
            btn.css_width = str(f'{W}%')
            btn.css_left = str(f'{L}%')
            btn.css_top = str(f'{T}%')
            btn.css_font_size = str(f'{fs}vw')
        btn.css_border_radius = bd_radius
        btn.css_border_style = bd_style
        btn.css_border_width = bd_width
        btn.css_border_color = bd_color
        btn.css_overflow = overflow
        btn.css_background_color = bg
        btn.css_color = fg
        btn.css_align_self = align
        btn.css_align_content = ac
        btn.css_align_items = align
        btn.css_display = display
        btn.css_justify_content = align
        btn.css_position = position
        btn.css_justify_content = justify
        frame.append(btn)
        return btn


    def create_table(self, frame, lst, H, W, L, T, bg='seashell', fg='black', overflow='scroll',
                     align_self='center', ac='center', align_items='center', margin='2px',
                     justify_content='center', fs=0.65, flex_wrap='wrap', bd_color='black',
                     display='space-around', position='absolute', px=False, bd_width='3px',
                     fw='normal', ff='calibri', bd_style='None', bd_radius='0px'):

        '''
        Author Aru Raghuvanshi
        :param frame: container object
        :param H: float: 0 to 100
        :param W: float: 0 to 100
        :param L: float: 0 to 100
        :param T: float: 0 to 100
        :param bg: str : label color, css colours or hex codes
        :param fg: str : text color, css colours or hex codes
        :param ac: str: default 'center' align content one of 'center', 'flex-start', 'flex-end'
        :param fw: str : font weight (bold, normal)
        :param ff: str: font family ('calibri')
        :param display: str: default 'grid'
        :param justify_content: str 'center'
        :param align_content: str: 'center'
        :param align_self: str: 'center'
        :param flex_wrap: str: 'wrap'
        :param bd_color: str: 'black
        :param bd_width: str: '3px'
        :param position: str: default 'absolute'
        :param px: bool : default False
        :param fs: float: font-size variable width default 0.65
        :param margin: str: default '0px'
        :param overflow: str: default 'auto' - adds scrollbar in case of overflowing content
        :return: Table widget
        '''

        btn = tk.Table.new_from_list(content=lst)
        if px:
            btn.variable_name = 'tbl'
            btn.css_height = str(f'{H}px')
            btn.css_width = str(f'{W}px')
            btn.css_left = str(f'{L}px')
            btn.css_top = str(f'{T}px')
            btn.css_font_size = str(f'{fs}px')
        else:
            btn.variable_name = 'tbl'
            btn.css_height = str(f'{H}%')
            btn.css_width = str(f'{W}%')
            btn.css_left = str(f'{L}%')
            btn.css_top = str(f'{T}%')
            btn.css_font_size = str(f'{fs}vw')
        # btn.css_font_size = fs
        btn.css_background_color = bg
        btn.css_color = fg
        btn.css_align_self = align_self
        btn.css_align_content = ac
        btn.css_align_items = align_items
        btn.css_display = display
        btn.css_justify_content = justify_content
        btn.css_position = position
        btn.css_overflow = overflow
        btn.css_flex_wrap = flex_wrap
        btn.css_border_color = bd_color
        btn.css_border_width = bd_width
        btn.css_border_radius = bd_radius
        btn.css_border_style = bd_style
        btn.css_font_weight = fw
        btn.css_font_family = ff
        btn.css_margin = margin
        frame.append(btn)
        return btn

    def create_clickable_table(self, frame, lst, H, W, L, T, rowcommand=None, bg='seashell', fg='black',
                               overflow='scroll', align_self='center', ac='center', align_items='center',
                               margin='2px', justify_content='center', fs=0.65, flex_wrap='wrap', bd_color='black',
                               display='space-around', position='absolute', bd_width='3px',
                               fw='normal', ff='calibri', bd_style='None', bd_radius='0px', lh='16px'):
        '''
        Author Aru Raghuvanshi
        :param frame: container object
        :param H: float: 0 to 100
        :param W: float: 0 to 100
        :param L: float: 0 to 100
        :param T: float: 0 to 100
        :param bg: str : label color, css colours or hex codes
        :param fg: str : text color, css colours or hex codes
        :param ac: str: default 'center' align content one of 'center', 'flex-start', 'flex-end'
        :param fw: str : font weight (bold, normal)
        :param ff: str: font family ('calibri')
        :param display: str: default 'grid'
        :param justify_content: str 'center'
        :param ac: str: 'center'
        :param align_self: str: 'center'
        :param ac: str: 'center'
        :param flex_wrap: str: 'wrap'
        :param bd_color: str: 'black
        :param bd_width: str: '3px'
        :param position: str: default 'absolute'
        :param fs: float: font-size variable width default 0.65
        :param margin: str: default '0px'
        :param overflow: str: default 'auto' - adds scrollbar in case of overflowing content
        :return: Table widget
        '''

        table = tk.Table(width=f'{W}%', height=f'{H}%', margin='10px')
        table.css_left = f'{L}%'
        table.css_top = f'{T}%'

        # Create table header
        header_row = tk.TableRow(style={'font-weight': 'bold'})
        for header in lst[0]:
            header_item = tk.TableItem(str(header), style={'background-color': bg})
            header_row.append(header_item)
        table.append(header_row)

        # Create table rows
        for row_data in lst[1:]:
            row = tk.TableRow()
            for item in row_data:
                row.append(tk.TableItem(item))
            row.onclick.connect(rowcommand, row_data)
            table.append(row)

        table.css_display = display
        table.css_position = position
        table.css_margin = margin
        table.css_overflow = overflow
        table.css_font_family = ff
        table.css_font_size = f'{fs}vw'
        table.css_background_color = bg
        table.css_color = fg
        table.css_border_color = bd_color
        table.css_border_width = bd_width
        table.css_border_style = bd_style
        table.css_border_radius = bd_radius
        table.css_font_weight = fw
        table.css_align_self = align_self
        table.css_align_content = ac
        table.css_align_items = align_items
        table.css_justify_content = justify_content
        table.css_flex_wrap = flex_wrap
        table.css_line_height = lh
        frame.append(table)
        return table

    def create_editable_table(self, frame, lst, H, W, L, T, bg='seashell', fg='black', overflow='scroll',
                              align_self='center', ac='center', align_items='center', margin='2px',
                              justify_content='center', fs=0.65, flex_wrap='wrap', bd_color='black',
                              display='space-around', position='absolute', bd_width='3px',
                              fw='normal', ff='calibri', bd_style='None', bd_radius='0px',
                              rowcommand=None, editcommand=None):
        '''
        Author Aru Raghuvanshi
        :param H: float: 0 to 100
        :param W: float: 0 to 100
        :param L: float: 0 to 100
        :param T: float: 0 to 100
        :param bg: str : label color, css colours or hex codes
        :param fg: str : text color, css colours or hex codes
        :param ac: str: default 'center' align content one of 'center', 'flex-start', 'flex-end'
        :param fw: str : font weight (bold, normal)
        :param ff: str: font family ('calibri')
        :param display: str: default 'grid'
        :param justify_content: str 'center'
        :param ac: str: 'center'
        :param align_self: str: 'center'
        :param flex_wrap: str: 'wrap'
        :param bd_color: str: 'black
        :param bd_width: str: '3px'
        :param position: str: default 'absolute'
        :param fs: float: font-size variable width default 0.65
        :param margin: str: default '0px'
        :param overflow: str: default 'auto' - adds scrollbar in case of overflowing content
        :return: Table widget
        '''

        table = tk.Table(width=f'{W}%', height=f'{H}%', margin='10px')
        table.css_left = f'{L}%'
        table.css_top = f'{T}%'

        # Create table header
        header_row = tk.TableRow(style={'font-weight': 'bold'})
        for header in lst[0]:
            header_item = tk.TableItem(str(header), style={'background-color': bg})
            header_row.append(header_item)
        table.append(header_row)

        # Create table rows with editable cells
        for row_index, row_data in enumerate(lst[1:]):
            row = tk.TableRow()
            for col_index, item in enumerate(row_data):
                text_input = tk.TextInput(single_line=True, style={'width': '100%'})
                text_input.set_text(item)
                text_input.onchange.connect(partial(editcommand, row_index, col_index))
                table_item = tk.TableItem()
                table_item.append(text_input)
                row.append(table_item)
                # Store reference to the TextInput widget
                self.text_inputs[(row_index, col_index)] = text_input
            row.onclick.connect(partial(rowcommand, row_data))
            table.append(row)

        table.css_display = display
        table.css_position = position
        table.css_margin = margin
        table.css_overflow = overflow
        table.css_font_family = ff
        table.css_font_size = f'{fs}vw'
        table.css_background_color = bg
        table.css_color = fg
        table.css_border_color = bd_color
        table.css_border_width = bd_width
        table.css_border_style = bd_style
        table.css_border_radius = bd_radius
        table.css_font_weight = fw
        table.css_align_self = align_self
        table.css_align_content = ac
        table.css_align_items = align_items
        table.css_justify_content = justify_content
        table.css_flex_wrap = flex_wrap
        frame.append(table)
        return table


    def create_image(self, frame, imagepath, H, W, L, T, h=100, w=100, bg='navyblue', fg='white',
                     align='center', justify='space-around', ac='center', bd_radius='0px', bd_style='none',
                     display='inline', position='absolute', px=False, bd_color='black', bd_width='0px'):
        '''
        Author Aru Raghuvanshi
        :param frame: container object
        :param imagepath: str: path of imagefile
        :param H: float: 0 to 100
        :param W: float: 0 to 100
        :param L: float: 0 to 100
        :param T: float: 0 to 100
        :param h: float: 0 to 100 default 100 (height of the image within container)
        :param w: float: 0 to 100 default 100 (height of the image within container)
        :param bg: str : label color, css colours or hex codes
        :param fg: str : text color, css colours or hex codes
        :param ac: str: default 'center' align content one of 'center', 'flex-start', 'flex-end'
        :param display: str: default 'inline'
        :param justify: str 'space-around'
        :param align: str: 'center'
        :param position: str: default 'absolute'
        :param px: bool : default False
        :return: Image widget
        '''


        btn = tk.Image(tk.load_resource(imagepath), h=f'{h}%', w=f'{w}%')

        if px:
            btn.variable_name = 'img'
            btn.css_height = str(f'{H}px')
            btn.css_width = str(f'{W}px')
            btn.css_left = str(f'{L}px')
            btn.css_top = str(f'{T}px')
        else:
            btn.variable_name = 'btn'
            btn.css_height = str(f'{H}%')
            btn.css_width = str(f'{W}%')
            btn.css_left = str(f'{L}%')
            btn.css_top = str(f'{T}%')
        btn.css_background_color = bg
        btn.css_color = fg
        btn.css_align_self = align
        btn.css_align_content = ac
        btn.css_align_items = align
        btn.css_display = display
        btn.css_justify_content = align
        btn.css_position = position
        btn.css_justify_content = justify
        btn.css_border_radius = bd_radius
        btn.css_border_style = bd_style
        btn.css_border_color = bd_color
        btn.css_border_width = bd_width
        frame.append(btn)
        return btn


    def create_listview(self, frame, lst, H, W, L, T, command=None, bg='skyblue', fg='black',
                        align='center', justify='space-around', fs=0.65, bd_radius='0px', ac='center',
                        display='inline', position='absolute', px=False, fw='normal', ff='calibri',
                        bd_style='none', bd_color='black', bd_width='0px'):

        '''
        Author Aru Raghuvanshi

        Example Usage:

        lst = ['Tiger', 'Lion', 'Jaguar']

        lv = C.create_listview(frame, lst, 40, 50, 5, 5, command=on_selection)

        def on_selection(w, val):
            print(f'val: {lv.children[val].get_text()}')

        :param frame: container object
        :param lst: list: iterable containing items to display in listview
        :param H: float: 0 to 100
        :param W: float: 0 to 100
        :param L: float: 0 to 100
        :param T: float: 0 to 100
        :param command: function to run on select
        :param bg: str : label color, css colours or hex codes
        :param fg: str : text color, css colours or hex codes
        :param fw: str : font weight (bold, normal)
        :param ff: str: font family ('calibri')
        :param fs: float: font-size variable width default 0.65
        :param ac: str: default 'center' align content one of 'center', 'flex-start', 'flex-end'
        :param display: str: default 'inline'
        :param justify: str 'space-around'
        :param align: str: 'center'
        :param position: str: default 'absolute'
        :param px: bool : default False
        :param bd_radius: str: border radius, default '0px'
        :return: Listview widget
        '''

        btn = tk.ListView.new_from_list(items=lst)

        if px:
            btn.variable_name = 'lvw'
            btn.css_height = str(f'{H}px')
            btn.css_width = str(f'{W}px')
            btn.css_left = str(f'{L}px')
            btn.css_top = str(f'{T}px')
        else:
            btn.variable_name = 'btn'
            btn.css_height = str(f'{H}%')
            btn.css_width = str(f'{W}%')
            btn.css_left = str(f'{L}%')
            btn.css_top = str(f'{T}%')
            btn.css_font_size = str(f'{fs}vw')
        # btn.css_font_size = fs
        btn.css_background_color = bg
        btn.css_color = fg
        btn.css_align_self = align
        btn.css_align_content = ac
        btn.css_align_items = align
        btn.css_display = display
        btn.css_position = position
        btn.css_justify_content = justify
        btn.css_border_radius = bd_radius
        btn.css_border_style = bd_style
        btn.css_border_color = bd_color
        btn.css_border_width = bd_width
        btn.css_font_weight = fw
        btn.css_font_family = ff
        btn.onselection.do(command)
        frame.append(btn)
        return btn


    def create_progress(self, frame, H, W, L, T, a, b=100, bg='lightgreen', fg='pink',
                        align='center', justify='space-around',
                        display='inline', position='absolute', px=False):

        '''Author Aru Raghuvanshi
        :param frame: container object
        :param H: float: 0 to 100
        :param W: float: 0 to 100
        :param L: float: 0 to 100
        :param T: float: 0 to 100
        :param a: start position of progress bar
        :param b: float : end position of progress bar (default 100)
        :param bg: str : label color, css colours or hex codes
        :param fg: str : text color, css colours or hex codes
        :param display: str: default 'inline'
        :param justify: str 'space-around'
        :param align: str: 'center'
        :param position: str: default 'absolute'
        :param px: bool : default False
        :return: Progressbar widget'''

        btn = tk.Progress(a, b)
        if px:
            btn.variable_name = 'prg'
            btn.css_height = str(f'{H}px')
            btn.css_width = str(f'{W}px')
            btn.css_left = str(f'{L}px')
            btn.css_top = str(f'{T}px')
        else:
            btn.variable_name = 'btn'
            btn.css_height = str(f'{H}%')
            btn.css_width = str(f'{W}%')
            btn.css_left = str(f'{L}%')
            btn.css_top = str(f'{T}%')
        btn.css_background_color = bg
        btn.css_color = fg
        btn.css_align_self = align
        btn.css_align_content = align
        btn.css_align_items = align
        btn.css_display = display
        btn.css_justify_content = align
        btn.css_position = position
        btn.css_justify_content = justify
        frame.append(btn)
        return btn


    def create_dropdown(self, frame, lst, H, W, L, T, command=None, bg='navyblue', fg='black',
                        align='center', justify='space-around', fs=0.65, ac='center',
                        display='inline', position='absolute', px=False, bd_style='none', bd_radius='0px',
                        bd_color='black', bd_width='0px'):

        '''Author Aru Raghuvanshi
        :param frame: container object
        :param lst: List (members to populate in the dropdown)
        :param H: float: 0 to 100
        :param W: float: 0 to 100
        :param L: float: 0 to 100
        :param T: float: 0 to 100
        :param ac: str: default 'center' align content one of 'center', 'flex-start', 'flex-end'
        :param command: function to run on selection
        :param bg: str : label color, css colours or hex codes
        :param fg: str : text color, css colours or hex codes
        :param fs: float: font-size variable width default 0.65
        :param display: str: default 'inline'
        :param justify: str 'space-around'
        :param align: str: 'center'
        :param position: str: default 'absolute'
        :param px: bool : default False
        :return: Dropdown widget'''

        btn = tk.DropDown.new_from_list(lst)
        if px:
            btn.variable_name = 'drp'
            btn.css_height = str(f'{H}px')
            btn.css_width = str(f'{W}px')
            btn.css_left = str(f'{L}px')
            btn.css_top = str(f'{T}px')
            btn.css_font_size = str(f'{fs}px')
        else:
            btn.variable_name = 'btn'
            btn.css_height = str(f'{H}%')
            btn.css_width = str(f'{W}%')
            btn.css_left = str(f'{L}%')
            btn.css_top = str(f'{T}%')
            btn.css_font_size = str(f'{fs}vw')
        btn.css_background_color = bg
        btn.css_color = fg
        btn.css_align_self = align
        btn.css_align_content = ac
        btn.css_align_items = align
        btn.css_display = display
        btn.css_justify_content = align
        btn.css_position = position
        btn.css_justify_content = justify
        btn.css_border_style = bd_style
        btn.css_border_color = bd_color
        btn.css_border_radius = bd_radius
        btn.css_border_width = bd_width
        btn.select_by_value(lst[0])
        btn.onchange.do(command)
        frame.append(btn)
        return btn


    def create_entry(self, frame, H, W, L, T, command=None, bg='white', fg='black', fw='normal', overflow='visible',
                     align='center', justify='space-around', input_type='regular', ff='calibri',
                     ac='center', maxlen=100, write_mode='none', letter_spacing='0px', line_height='16px',
                     display='inline', position='absolute', px=False, fs=0.8, bd_radius='0px',
                     bd_style='None', bd_width='0px', bd_color='black', single_line=False):

        '''
        Author Aru Raghuvanshi
        :param frame: container object
        :param H: float: 0 to 100
        :param W: float: 0 to 100
        :param L: float: 0 to 100
        :param T: float: 0 to 100
        :param command: Function to run on user input
        :param bg: str : label color, css colours or hex codes
        :param fg: str : text color, css colours or hex codes
        :param fw: str : font weight (bold, normal)
        :param ff: str: font family ('calibri')
        :param input_type: str: one of 'regular', 'text' or 'password' default: 'regular' | Input Types > Regular: for small entry fields with horizontal scrolling | Password: hides text in the entry field | Text: Multiline inputs text box
        :param ac: str: default 'center' align content one of 'center', 'flex-start', 'flex-end'
        :param align: str: default 'center'
        :param justify: str: default 'center'
        :param display: str: default 'grid'
        :param bd_style: str : default 'None' (solid, dotted, dashed)
        :param bd_radius: str: default '0px'
        :param position: str: default 'absolute'
        :param px: bool : default False
        :param fs: float: font-size variable width default 0.8
        :param bd_width: str: default '0px'
        :param bd_color: str: default 'black'
        :param overflow: str: default 'visible'
        :param write_mode: str: default 'none' [none, horizontal-tb, vertical-rl, vertical-lr]
        :param letter_spacing: str: default '0px'
        :param single_line: bool: default False, whether the entry box supports multiline entry
        :param maxlen: int default 100, max characters that can be written in the text field
        :param line_height: str default '16px' line spacing between multiple lines in the textbox
        :return: Entry widget.


        '''

        if input_type == 'password':
            btn = tk.Input(input_type='password')
            btn.attributes['type'] = 'password'
            btn.style['background-color'] = 'lightgray'
            btn.onchange.connect(command)
        elif input_type == 'text':
            btn = tk.TextInput(single_line=single_line)
        else:
            btn = tk.Input()
            btn.style['background-color'] = 'lightgray'

        if px:
            btn.variable_name = 'drp'
            btn.css_height = str(f'{H}px')
            btn.css_width = str(f'{W}px')
            btn.css_left = str(f'{L}px')
            btn.css_top = str(f'{T}px')
            btn.css_font_size = str(f'{fs}px')
        else:
            btn.variable_name = 'btn'
            btn.css_height = str(f'{H}%')
            btn.css_width = str(f'{W}%')
            btn.css_left = str(f'{L}%')
            btn.css_top = str(f'{T}%')
            btn.css_font_size = str(f'{fs}vw')

        btn.attr_maxlength = maxlen
        btn.css_border_radius = bd_radius
        btn.css_border_style = bd_style
        btn.css_border_width = bd_width
        btn.css_border_color = bd_color
        btn.css_background_color = bg
        btn.css_color = fg
        btn.css_align_self = align
        btn.css_align_content = ac
        btn.css_align_items = align
        btn.css_display = display
        btn.css_justify_content = align
        btn.css_position = position
        btn.css_justify_content = justify
        btn.css_overflow = overflow
        btn.css_font_weight = fw
        btn.css_font_family = ff
        btn.css_writing_mode = write_mode
        btn.css_letter_spacing = letter_spacing
        btn.css_line_height = line_height
        btn.onchange.do(command)
        frame.append(btn)
        return btn


    def create_input_dialogue(self, frame, H, W, L, T, title='title', message='desc', bd_radius='0px',
                             command=None, bg='navyblue', fg='white', fs=0.7, bd_width='0px',
                             align='center', justify='space-around', ac='center', bd_style='none',
                             display='inline', position='absolute', px=False, bd_color='black'):

        '''Author: Aru Raghuvanshi
        :param H: float: 0 to 100
        :param W: float: 0 to 100
        :param L: float: 0 to 100
        :param T: float: 0 to 100
        :param title: str:
        :param message: str:
        :param command: function
        :param bg: str : css colours or hex codes
        :param fg: str : text color, css colours or hex codes
        :param ac: str: default 'center' align content one of 'center', 'flex-start', 'flex-end'
        :param align: str: default 'center'
        :param justify: str: default 'center'
        :param display: str: default 'grid'
        :param bd_style: str : default 'None' (solid, dotted, dashed)
        :param bd_radius: str: default '0px'
        :param position: str: default 'absolute'
        :param px: bool : default False
        :param fs: float: font-size variable width default 0.8
        :param bd_width: str: default '0px'
        :param bd_color: str: default 'black'
        :return: Entry widget.
        '''

        btn = tk.InputDialog(title=title, message=message)
        btn.confirm_value.do(command)

        if px:
            btn.variable_name = 'drp'
            btn.css_height = str(f'{H}px')
            btn.css_width = str(f'{W}px')
            btn.css_left = str(f'{L}px')
            btn.css_top = str(f'{T}px')
        else:
            btn.variable_name = 'btn'
            btn.css_height = str(f'{H}%')
            btn.css_width = str(f'{W}%')
            btn.css_left = str(f'{L}%')
            btn.css_top = str(f'{T}%')
            btn.css_font_size = str(f'{fs}vw')
        btn.css_background_color = bg
        btn.css_color = fg
        btn.css_align_self = align
        btn.css_align_content = ac
        btn.css_align_items = align
        btn.css_display = display
        btn.css_justify_content = align
        btn.css_position = position
        btn.css_justify_content = justify
        btn.css_border_radius = bd_radius
        btn.css_border_style = bd_style
        btn.css_border_width = bd_width
        btn.css_border_color = bd_color
        frame.append(btn)
        return btn


    # def create_date_picker2(self, frame, H, W, L, T, command=None, bg='white', fg='black', overflow='visble',
    #                        align='center', justify='space-around', fs=0.7, bd_width='0px',
    #                        margin='0px', bd_color='black', ac='center',
    #                        display='inline-flex', position='absolute', px=False, bd_style='none', bd_radius='0px'):
    #
    #     '''Author Aru Raghuvanshi
    #     :param frame: container object
    #      :param H: float: 0 to 100
    #     :param W: float: 0 to 100
    #     :param L: float: 0 to 100
    #     :param T: float: 0 to 100
    #     :param command : function to run on button press
    #     :param bg: str : label color, css colours or hex codes
    #     :param fg: str : text color, css colours or hex codes
    #     :param align: str: default 'center'
    #     :param ac: str: default 'center' align content one of 'center', 'flex-start', 'flex-end'
    #     :param justify: str: default 'space-around'
    #     :param display: str: default 'inline-flex'
    #     :param bd_style: str : default 'None' (solid, dotted, dashed)
    #     :param bd_radius: str: default '0px'
    #     :param position: str: default 'absolute'
    #     :param px: bool : default False
    #     :param fs: float: font-size variable width default 0.7
    #     :param margin: str: default '0px'
    #     :param bd_width: str: default '0px'
    #     :param bd_color: str: default 'black'
    #     :param overflow: str: default 'visible'
    #     :return: Date Picker widget'''
    #
    #     def utc2local():
    #         tzInfo = pytz.timezone('Asia/Kolkata')
    #         dttm = datetime.now(tz=tzInfo)
    #         dttm = dttm.strftime('%d-%m-%Y %H:%M:%S')
    #         dttm = str(dttm)[:16]
    #         dt = dttm.split(' ')[0]
    #         tm = dttm.split(' ')[1]
    #         # C.pr('date', dt, 'y')
    #         # C.pr('time', tm, 'y')
    #         return dt, tm
    #
    #     date, tm = utc2local()
    #     btn = tk.Date(default_value=date)
    #     if px:
    #         btn.variable_name = 'btn'
    #         btn.css_height = str(f'{H}px')
    #         btn.css_width = str(f'{W}px')
    #         btn.css_left = str(f'{L}px')
    #         btn.css_top = str(f'{T}px')
    #         btn.css_top = str(f'{fs}px')
    #     else:
    #         btn.variable_name = 'btn'
    #         btn.css_height = str(f'{H}%')
    #         btn.css_width = str(f'{W}%')
    #         btn.css_left = str(f'{L}%')
    #         btn.css_top = str(f'{T}%')
    #         btn.css_top = str(f'{fs}vw')
    #     btn.css_overflow = overflow
    #     btn.css_background_color = bg
    #     btn.css_color = fg
    #     btn.css_align_self = align
    #     btn.css_align_content = ac
    #     btn.css_align_items = align
    #     btn.css_display = display
    #     btn.css_justify_content = align
    #     btn.css_position = position
    #     btn.css_justify_content = justify
    #     btn.css_border_style = bd_style
    #     btn.css_border_width = bd_width
    #     btn.css_border_radius = bd_radius
    #     btn.css_border_color = bd_color
    #     btn.css_margin = margin
    #     btn.onchange.do(command)
    #     frame.append(btn)
    #     return btn

    def create_date_picker(self, frame, H, W, L, T, command=None, bg='linen', fg='black',
                          align='center', justify='space-around', fs=0.65, bd_width='0px', ac='center',
                          display='inline', position='absolute', px=False, bd_style='None', bd_radius='0px',
                          bd_color='black'):

        """Author Aru Raghuvanshi
        :param frame: container object
        :param H: float: 0 to 100
        :param W: float: 0 to 100
        :param L: float: 0 to 100
        :param T: float: 0 to 100
        :param command : function to run on button press
        :param bg: str : label color, css colours or hex codes
        :param fg: str : text color, css colours or hex codes
        :param align: str: default 'center'
        :param ac: str: default 'center' align content one of 'center', 'flex-start', 'flex-end'
        :param justify: str: default 'space-around'
        :param display: str: default 'inline-flex'
        :param bd_style: str : default 'None' (solid, dotted, dashed)
        :param bd_radius: str: default '0px'
        :param position: str: default 'absolute'
        :param px: bool : default False
        :param fs: float: font-size variable width default 0.65
        :param bd_width: str: default '0px'
        :param bd_color: str: default 'black'
        :return: Date Picker widget"""

        date, _ = self.utc2local()
        btn = tk.Date(default_value=date)
        if px:
            btn.variable_name = 'btn'
            btn.css_height = str(f'{H}px')
            btn.css_width = str(f'{W}px')
            btn.css_left = str(f'{L}px')
            btn.css_top = str(f'{T}px')
            btn.css_font_size = str(f'{fs}px')
        else:
            btn.variable_name = 'btn'
            btn.css_height = str(f'{H}%')
            btn.css_width = str(f'{W}%')
            btn.css_left = str(f'{L}%')
            btn.css_top = str(f'{T}%')
            btn.css_font_size = str(f'{fs}vw')
        btn.css_background_color = bg
        btn.css_color = fg
        btn.css_align_self = align
        btn.css_align_content = ac
        btn.css_align_items = align
        btn.css_display = display
        btn.css_justify_content = align
        btn.css_position = position
        btn.css_justify_content = justify
        btn.css_border_style = bd_style
        btn.css_border_width = bd_width
        btn.css_border_radius = bd_radius
        btn.css_border_color = bd_color
        btn.onchange.do(command)
        frame.append(btn)
        return btn


    def create_downloader(self, frame, H, W, L, T, text, file, bg='whitesmoke', fg='black', ff='calibri',
                          align='center', justify='space-around', fs=0.8, bd_radius='0px', fw='normal',
                          display='inline', position='absolute', px=False, ac='center', bd_style='none',
                          bd_width='0px', bd_color='black'):
        '''
        Author: Aru Raghuvanshi
        :param frame: container object
        :param H: float: 0 to 100
        :param W: float: 0 to 100
        :param L: float: 0 to 100
        :param T: float: 0 to 100
        :param text: str:
        :param file: str:
        param bg: str : label color, css colours or hex codes
        :param fg: str : text color, css colours or hex codes
        :param align: str: default 'center'
        :param ac: str: default 'center' align content one of 'center', 'flex-start', 'flex-end'
        :param justify: str: default 'space-around'
        :param display: str: default 'inline-flex'
        :param bd_style: str : default 'None' (solid, dotted, dashed)
        :param bd_radius: str: default '0px'
        :param position: str: default 'absolute'
        :param px: bool : default False
        :param fs: float: font-size variable width default 0.65
        :param bd_width: str: default '0px'
        :param bd_color: str: default 'black'
        :return Dowloader object
        '''

        btn = tk.FileDownloader(text=text, filename=file)

        if px:
            btn.variable_name = 'upl'
            btn.css_height = str(f'{H}px')
            btn.css_width = str(f'{W}px')
            btn.css_left = str(f'{L}px')
            btn.css_top = str(f'{T}px')
        else:
            btn.variable_name = 'btn'
            btn.css_height = str(f'{H}%')
            btn.css_width = str(f'{W}%')
            btn.css_left = str(f'{L}%')
            btn.css_top = str(f'{T}%')
            btn.css_font_size = str(f'{fs}vw')
        btn.css_font_family = ff
        btn.css_font_weight = fw
        btn.css_background_color = bg
        btn.css_color = fg
        btn.css_align_self = align
        btn.css_align_content = ac
        btn.css_align_content = align
        btn.css_align_items = align
        btn.css_display = display
        btn.css_justify_content = align
        btn.css_position = position
        btn.css_justify_content = justify
        btn.css_border_style = bd_style
        btn.css_border_width = bd_width
        btn.css_border_radius = bd_radius
        btn.css_border_color = bd_color
        frame.append(btn, key='file_downloader')
        return btn


    def create_label_checkbox(self, frame, H, W, L, T, text, command=None, val=False, bd_radius='0px',
                              bg='whitesmoke', fg='black', justify='space-around', fs=0.7, ac='center',
                              ff='calibri', fw='normal', display='flex', position='absolute', px=False,
                              align_items='center', align_self='auto'):

        '''Author Aru Raghuvanshi
        :param frame: container object
        :param H: float: 0 to 100
        :param W: float: 0 to 100
        :param L: float: 0 to 100
        :param T: float: 0 to 100
        :param text : Text on Checkbox Label
        :param command : function to run on button press
        :param bg: str : label color, css colours or hex codes
        :param fg: str : text color, css colours or hex codes
        :param justify: str: default 'space-around'
        :param display: str: default 'flex'
        :param position: str: default 'absolute'
        :param px: bool : default False
        :param fs: float: font-size variable width default 0.7
        :return: Label Checkbox widget'''

        btn = tk.CheckBoxLabel(text, val)

        if px:
            btn.variable_name = 'upl'
            btn.css_height = str(f'{H}px')
            btn.css_width = str(f'{W}px')
            btn.css_left = str(f'{L}px')
            btn.css_top = str(f'{T}px')
            btn.css_font_size = str(f'{fs}px')
        else:
            btn.variable_name = 'btn'
            btn.css_height = str(f'{H}%')
            btn.css_width = str(f'{W}%')
            btn.css_left = str(f'{L}%')
            btn.css_top = str(f'{T}%')
            btn.css_font_size = str(f'{fs}vw')
        btn.css_background_color = bg
        btn.css_color = fg
        btn.css_align_self = align_self
        btn.css_align_content = ac
        btn.css_align_items = align_items
        btn.css_display = display
        btn.css_border_radius = bd_radius
        btn.css_position = position
        btn.css_font_weight = fw
        btn.css_font_family = ff
        btn.css_justify_content = justify
        btn.onchange.do(command)
        frame.append(btn)
        return btn


    def create_slider(self, frame, H, W, L, T, max, min, command=None, step=1, px=False, fs=0.8,
                      bg='whitesmoke', bd_radius='0px', bd_style='none', bd_width='0px', bd_color='black',
                      position='absolute'):

        '''
         Author Aru Raghuvanshi
        :param frame: container object
         :param H: float: 0 to 100
        :param W: float: 0 to 100
        :param L: float: 0 to 100
        :param T: float: 0 to 100
        :param command : function to run on button press
        :param bd_style: str : default 'None' (solid, dotted, dashed)
        :param bd_radius: str: default '0px'
        :param bd_color: str : default 'black'
        :param bd_width: str: default '0px'
        :param bg: str : label color, css colours or hex codes
        :param position: str: default 'absolute'
        :param px: bool : default False
        :param fs: float: font-size variable width default 0.8
        :return: Slider Widget widget'''

        btn = tk.Slider(default_value='0', min=min, max=max, step=step)

        if px:
            btn.variable_name = 'sld'
            btn.css_height = str(f'{H}px')
            btn.css_width = str(f'{W}px')
            btn.css_left = str(f'{L}px')
            btn.css_top = str(f'{T}px')
            btn.css_font_size = str(f'{fs}px')
        else:
            btn.variable_name = 'btn'
            btn.css_height = str(f'{H}%')
            btn.css_width = str(f'{W}%')
            btn.css_left = str(f'{L}%')
            btn.css_top = str(f'{T}%')
            btn.css_font_size = str(f'{fs}vw')
        btn.css_position = position
        btn.css_background_color = bg
        btn.css_border_style = bd_style
        btn.css_border_width = bd_width
        btn.css_border_radius = bd_radius
        btn.css_border_color = bd_color
        btn.onchange.do(command)
        frame.append(btn)
        return btn


    def create_spinbox(self, frame, H, W, L, T, max, min, command=None, step=1, px=False, fs=0.8,
                      bg='whitesmoke', bd_radius='0px', bd_style='none', bd_width='0px', bd_color='black',
                      position='absolute', allow_editing=True):

        '''
         Author Aru Raghuvanshi
        :param frame: container object
         :param H: float: 0 to 100
        :param W: float: 0 to 100
        :param L: float: 0 to 100
        :param T: float: 0 to 100
        :param command : function to run on button press
        :param bd_style: str : default 'None' (solid, dotted, dashed)
        :param bd_radius: str: default '0px'
        :param bd_color: str : default 'black'
        :param bd_width: str: default '0px'
        :param bg: str : label color, css colours or hex codes
        :param position: str: default 'absolute'
        :param px: bool : default False
        :param fs: float: font-size variable width default 0.8
        :param allow_editing: bool : default True (Change values manually)
        :return: Slider Widget'''

        btn = tk.SpinBox(default_value=0, min_value=min, max_value=max, step=step, allow_editing=allow_editing)

        if px:
            btn.variable_name = 'spn'
            btn.css_height = str(f'{H}px')
            btn.css_width = str(f'{W}px')
            btn.css_left = str(f'{L}px')
            btn.css_top = str(f'{T}px')
            btn.css_font_size = str(f'{fs}px')
        else:
            btn.variable_name = 'btn'
            btn.css_height = str(f'{H}%')
            btn.css_width = str(f'{W}%')
            btn.css_left = str(f'{L}%')
            btn.css_top = str(f'{T}%')
            btn.css_font_size = str(f'{fs}vw')
        btn.css_position = position
        btn.css_background_color = bg
        btn.css_border_style = bd_style
        btn.css_border_width = bd_width
        btn.css_border_radius = bd_radius
        btn.css_border_color = bd_color
        btn.onchange.do(command)
        frame.append(btn)
        return btn


    def show_html(self, frame, htmlcontent, H, W, L, T, w=100, h=100, margin='4px',
                  border='1px solid black'):
        '''

        Author Aru Raghuvanshi
        :param frame: container object
        :param htmlcontent: str: path to html file
        :param H: float: 0 to 100
        :param W: float: 0 to 100
        :param L: float: 0 to 100
        :param T: float: 0 to 100
        :param w : float: 0 to 100 default 100 (width of image in container)
        :param h : float: 0 to 100 default 100 (width of image in container)
        :param margin: str: default '4px'
        :param border: str: format="1px solid black" example border='2px dashed red'
        :return: HTML in a container
        '''
        mc = gui.create_container(frame, H, W, L, T)

        frame = tk.Widget(_type='iframe', width=w, height=h, margin=margin)
        frame.attributes['src'] = htmlcontent
        frame.attributes['width'] = f'{w}%'
        frame.attributes['height'] = f'{h}%'
        frame.style['border'] = border

        mc.add_child('frame', frame)
        return frame


    def show_plotly(self, frame, htmlcontent, H, W, L, T, w=100, h=100, margin='0px',
                    border='1px solid black'):

        '''
        Author Aru Raghuvanshi
        :param frame: container object
        :param htmlcontent: str: path to html plotly file
         :param H: float: 0 to 100
        :param W: float: 0 to 100
        :param L: float: 0 to 100
        :param T: float: 0 to 100
        :param w : float: 0 to 100 default 100 (width of image in container)
        :param h : float: 0 to 100 default 100 (width of image in container)
        :param margin: str: default '0px'
        :param border: str: format="1px solid black" example border='2px dashed red'
        :return: plotly chart in a container
        '''
        mc = gui.create_container(frame, H, W, L, T)

        res = tk.load_resource(htmlcontent)
        btn = tk.Widget(_type='iframe', margin=margin)
        btn.attributes['src'] = res
        btn.attributes['width'] = f'{w}%'
        btn.attributes['height'] = f'{h}%'
        btn.style['border'] = border

        mc.add_child('frame', btn)
        # window.append(main_container)
        # returning the root widget
        return frame


# ------------------------------------ ADVANCED -------------------------------------------------------------- ]

    # def autolabels(self, frm, lst1, lst2, H, L, T, L2, n, bg='lavender', bg2='oldlace',
    #                   fg='black', fg2='black', align1='left', align2='left', justify1='left',
    #                   justify2='left'):
    #
    #     '''
    #     Author: Aru Raghuvanshi
    #     :param frm: frame or container holding the labels
    #     :param lst1: list: list for lhs
    #     :param lst2: list: list for rhs
    #     :param H: float: Height of Labels 0 to 100
    #     :param L: float: Left of lhs Labels 0 to 100
    #     :param T: float: Height of Labels 0 to 100
    #     :param L2: float: Left of rhs labels (spacing between lhs and rhs)
    #     :param L2: float: Left of rhs labels (spacing between lhs and rhs)
    #     :param n: float: Multiplier for vertical spacing between labels
    #     :param bg: str: color of lhs labels
    #     :param bg2: str: color of rhs labels
    #     :param fg: str: font color of lhs labels
    #     :param fg2: str: color of rhs labels
    #     :param align1: str: text align of lhs labels
    #     :param align2: str: text align of rhs labels
    #     :param justify1: str: text align of lhs labels
    #     :param justify2: str: text align of rhs labels
    #     :return: Frame, labels
    #
    #     Coloring based on conditions can be done through this example:
    #     frame, lbl, lbr = C.autolabels(self.frame_info, lst1, lst2, H, L, T, L2, n)
    #
    #     lbr[3].css_color = 'salmon'  # Change right side color on 3rd index
    #
    #     lbl[2].css_color = 'yellowgreen'    # Change left side color on 2nd index
    #
    #     '''
    #     lbll, lblr = [],[]
    #     if len(lst1) != len(lst2):
    #         C.cprint('\t - Autolabels Lists lst1 and lst2 need to be of same length', 'v')
    #         lbl1, lbl2 = None, None
    #         frm = None
    #         return frm, lbl1, lbl2
    #
    #     else:
    #         for (i, x), y in zip(enumerate(lst1), lst2):
    #             C.cprint(f'\t - Autolabel info: {i}: {x}, {y}', 'c')
    #             lbl1, lbl2 = C.labels(frm, H, len(str(x)), L, T + (i * n), H, len(str(y)),
    #                      L2, T + (i * n), text=str(x),
    #                      align1=align1, justify1=justify1, text2=str(y), bg=bg, fg=fg, fg2=fg2,
    #                      align2=align2, justify2=justify2, bg2=bg2)
    #
    #             lbll.append(lbl1)
    #             lblr.append(lbl2)
    #
    #         for l, r in zip(range(len(lbll)), range(len(lblr))):
    #             C.pr(f'\t - label1 {l}:', lbll[l].text, 'c')
    #             C.pr(f'\t - label2 {r}', lblr[r].text, 'c')
    #
    #         return frm, lbll, lblr

    def utc2local(self):
        utc = datetime.utcnow()
        tzInfo = pytz.timezone('Asia/Kolkata')
        dttm = datetime.now(tz=tzInfo)
        dttm = dttm.strftime('%d-%m-%Y %H:%M:%S')
        dttm = str(dttm)[:16]
        dt = dttm.split(' ')[0]
        tm = dttm.split(' ')[1]
        return dt, tm


    def string_to_dt(self, date_string, date_format='%Y-%m-%d'):
        '''
        :param date_string: str: incoming date string in format set by date_format
        :param date_format: str: expected format of incoming date
        :return: datetime obj with timestamp 00:00:00 if not specified in format
        '''
        from datetime import datetime
        dobj = datetime.strptime(date_string, date_format)
        return dobj


    def dt_to_string(self, dobj, format='%Y-%m-%d'):
        '''
        :param dobj: datetime obj
        :param format: str: expected format of returned date
        :return: str date in format set
        '''
        from datetime import datetime
        formatted_date = dobj.strftime(format)
        return formatted_date


    def cprint(self, text, c='w'):
        '''
        Author: Aru Raghuvanshi
        Use this function to print statements in different colours
        :param text: str
        :param c: str: one of [b, g, r, v, y, c, w, bb, gg, rr, vv, yy, cc, ww, u, s, i]
        :return: none

        s: strikethru, u:underline, i:italics default: white

        '''
        if c == 'b':
            print(f'\033[0;94m{text}\033[0m')
        elif c == 'g':
            print(f'\033[0;92m{text}\033[0m')
        elif c == 'r':
            print(f'\033[0;91m{text}\033[0m')
        elif c == 'v':
            print(f'\033[0;95m{text}\033[0m')
        elif c == 'y':
            print(f'\033[0;93m{text}\033[0m')
        elif c == 'c':
            print(f'\033[0;96m{text}\033[0m')
        elif c == 'w':
            print(f'\033[0;97m{text}\033[0m')
        elif c == 'bb':
            print(f'\033[1;94m{text}\033[0m')
        elif c == 'gg':
            print(f'\033[1;92m{text}\033[0m')
        elif c == 'rr':
            print(f'\033[1;91m{text}\033[0m')
        elif c == 'vv':
            print(f'\033[1;95m{text}\033[0m')
        elif c == 'yy':
            print(f'\033[1;93m{text}\033[0m')
        elif c == 'cc':
            print(f'\033[1;96m{text}\033[0m')
        elif c == 'ww':
            print(f'\033[1;97m{text}\033[0m')
        elif c == 'u':
            print(f'\033[0;4m{text}\033[0m')
        elif c == 's':
            print(f'\033[0;9m{text}\033[0m')
        elif c == 'i':
            print(f'\033[0;3m{text}\033[0m')
        else:
            pass


    def pr(self, t1, t2, c='w'):
        '''
        :param t1: str: text
        :param t2: str: text
        :param c: str: one of b,g,r,v,y,c,w,bb,gg,rr,vv,cc,yy,cc,ww,u,s,i
        :return: None
        '''
        self.cprint(f'{t1}: {t2}', c=c)


    def edit_df(self, df, unique_id_col, row_item, col, edit, save=False, filepath='', index=False):
        '''
        :param df : dataframe
        :param unique_id_col : name of the column that holds the unique row identifier
        :param row_item : value of the record item in the unique_id column
        :param col: name of the column whose record needs the edit
        :param edit: str: value (str) that needs to be edited
        :param save: bool: save file to csv (default false)
        :param filepath: str: path of the file to be saved to (default '')
        :param index: bool whether saved file should have index (default false)
        :return df: dataframe
        '''
        df.loc[df[unique_id_col] == row_item, col] = edit

        if save:
            df.to_csv(filepath, index=index)

        return df

    def add_to_df(self, df, lst, save=False, filepath='', index=False):
        '''
        :param df: dataframe to delete row from
        :param lst: list: complete list of the values to be entered into the dataframe, one element per column of df
        :param save: bool: save to csv (default false)
        :param filepath: str: filepath to save the csv file to (default '')
        :param index: bool: whether to save the index to csv file (default false)
        :return df
        '''
        try:
            dx = pd.DataFrame([lst], columns=df.columns)
            df = pd.concat([df, dx]).reset_index(drop=True)

            if save:
                df.to_csv(filepath, index=index)

        except Exception as e:
            print(f'Data Adding unsuccessful')
            print(e)

        return df

    def delete_row_from_df(self, df, unique_id_col, row_item, save=False, filepath='', index=False):
        '''
        :param df: dataframe to delete row from
        :param unique_id_col: name of the column that holds the unique_id of the row
        :param row_item: value of the unique_id
        :param save: bool: save to csv (default false)
        :param filepath: str: filepath to save the csv file to (default '')
        :param index: bool: whether to save the index to csv file (default false)
        :return df
        '''
        dx = df[df[unique_id_col] == row_item]
        df = df.drop(dx.index[0])

        if save:
            df.to_csv(filepath, index=index)

        return df


C = GUI()

