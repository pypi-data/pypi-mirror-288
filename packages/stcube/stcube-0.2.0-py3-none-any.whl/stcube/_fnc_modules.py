import os
import os.path as path
import shutil
import zipfile
import colorama
import datetime
from stcube.core import *
from stcube._pyqt_pack import *

def zip_files(base_dir, fpaths, zip_path):
    """
    Zip the files to the target directory.
    :param rel_fpaths: list of relative file paths
    :param target_dir: target directory
    :return:
    """
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for fpath in fpaths:
            zipf.write(fpath, os.path.relpath(fpath, base_dir))

def unzip_files(zip_path, target_dir):
    """
    Unzip the files to the target directory.
    :param zip_path: zip file path
    :param target_dir: target directory
    :return:
    """
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        zipf.extractall(target_dir)


class ModuleWizardCollection:
    def __init__(self, name, rel_c_files, rel_h_files, *, brief=None, desc=None, author=None, adjust:bool=False):
        self.name = name
        self.rel_c_files = rel_c_files
        self.rel_h_files = rel_h_files

        self.brief = brief
        self.desc = desc
        self.author = author
        self.adjust = adjust  # 是否需要调整define

    def __str__(self):
        return f"ModuleWizardCollection({self.name})"

class Module(Functional):
    key = 'm|mod'
    doc = """
    Modules management.
        - Module is made from some .c/cpp .h/hpp files.
    .new: Create a new module from current project directory.
    .exp: Open the module directory in the explorer.
    """
    doc_zh = """
    模块管理模块, 展示当前的模块列表.
        - 模块是由一些.c/cpp .h/hpp文件创建的。
    .new: 从当前项目目录创建新模块。
    .exp: 在资源管理器中打开模块目录。
    """
    NOT_CONTAINS = ["/* USER CODE BEGIN Header */"]  # if contain any of these, it is not a module
    sys = Functional.sys + ['mods', 'scan_individual_files', 'induce_name', 'build_path_tree', 'modularize', 'get_collection', 'NOT_CONTAINS', 'scan_rmods']

    def loading(self):
        cp_open = self.ce.get('o|cd|open')
        if not cp_open:
            raise Exception("\n\nSystem Error: \n\tComponent<FOpen> not found. "
                            if setting.language == 'en' else
                            "\n\n系统错误: \n\t组件<FOpen>未找到。")
        self.cp_open = cp_open


    @staticmethod
    def mods(dir=MODS_DIR):
        if not os.path.exists(dir):
            os.makedirs(dir)
        ff = FileFinder(dir)
        fc = ff.find('.zip', '.ZIP')
        _res = []
        _infos = HOME_F.MODS_INFO if HOME_F.has('MODS_INFO') else {}
        for fpath in fc:
            fname = os.path.splitext(os.path.basename(fpath))[0]

            _flag = False  # 识别Mod
            for prefix in VALID_MOD_PREFIXS:
                if fname.startswith(prefix):
                    _flag = True
                    break
            if not _flag:
                continue

            last_change_time = os.path.getmtime(fpath)
            if fname in _infos:
                _info = _infos[fname]
                _res.append({
                    'name': fname,
                    'path': fpath,
                    'author': _info['author'],
                    'brief': _info['brief'],
                    'desc': _info['desc'],
                    'adjust': _info['adjust'],
                    'c_files': _info['c_files'],
                    'h_files': _info['h_files'],
                    'time': datetime.datetime.fromtimestamp(last_change_time).strftime("%Y-%m-%d %H:%M:%S")
                })
            else:
                _res.append({
                    'name': fname,
                    'path': fpath,
                    'author': 'Unknown',
                    'brief': 'Unknown',
                    'desc': 'Unknown',
                    'adjust': False,
                    'c_files': None,
                    'h_files': None,
                    'time': datetime.datetime.fromtimestamp(last_change_time).strftime("%Y-%m-%d %H:%M:%S")
                })
        return _res


    @staticmethod
    def scan_rmods(tar_dir, only_name=False) -> list[str]:
        tar_dir = path.abspath(tar_dir)
        for fname in os.listdir(tar_dir):
            if fname.endswith('.zip'):
                for prefix in VALID_MOD_PREFIXS:
                    if fname.startswith(prefix):
                        yield os.path.join(tar_dir, fname) if not only_name else fname
                        break

    @staticmethod
    def _ut_scan_individual_files(path):
        ff = FileFinder(path)
        fc = ff.find('.c', '.cpp', '.h', '.hpp', exclude='(main)|(sys.*)')
        _cs, _hs = [], []
        for fpath in fc:
            # check if contain USER CODE BEGIN Header
            with open_unknown_encoding_file(fpath, 'r') as f:
                f_read = f.read()
                _any_flag = False
                for nc in Module.NOT_CONTAINS:
                    if nc in f_read:
                        _any_flag = True
                        break
                if not _any_flag:
                    if fpath.endswith('.c') or fpath.endswith('.cpp'):
                        _cs.append(fpath)
                    else:
                        _hs.append(fpath)
        return _cs, _hs

    @staticmethod
    def _ut_induce_name(c_files, h_files):
        """
        Induce the module name from the files.
        * 自动把重复次数最多的文件名作为模块名
        :param c_files:
        :param h_files:
        :return:
        """
        cnames = [os.path.basename(f).split('.')[0] for f in c_files]
        hnames = [os.path.basename(f).split('.')[0] for f in h_files]
        chnames = cnames + hnames
        _name_count = {}
        for k in chnames:
            if k in _name_count:
                _name_count[k] += 1
            else:
                _name_count[k] = 1

        # get the most common name
        _max = 0
        _name = None
        for k, v in _name_count.items():
            if v > _max:
                _max = v
                _name = k

        return _name

    @staticmethod
    def _ut_build_path_tree(rel_paths):
        """
        输入多个相对路径，输出一个树状dict，例如:
        'a/b/c.txt'
        'a/000.txt'
        '12.txt'
        'a/256.txt'
        'a/b/d.txt'
        ->
        {
        '_': [12.txt, ],
        'a': {
            '_': [256.txt, 000.txt],
            'b': {
                '_': [c.txt, e.txt]
        }}}
        :param rel_paths:
        :return:
        """
        def cross_union(path_parts) -> dict:
            _res = {'_': []}
            for parts in path_parts:
                _len = len(parts)
                if _len == 0:
                    continue
                elif _len == 1:
                    _res['_'].append(parts[0])
                else:
                    level = parts[0]
                    if level not in _res:
                        _res[level] = []
                    _res[level].append(parts[1:])

            for k, v in _res.items():
                if k == '_':
                    continue
                if isinstance(v, list):
                    _res[k] = cross_union(v)
            return _res

        path_parts = [os.path.normpath(path).split(os.sep) for path in rel_paths]

        return cross_union(path_parts)

    def new(self):
        """
        Create a new module from the current project.
        :return:
        """
        if not os.path.exists(MODS_DIR):
            os.makedirs(MODS_DIR)
        if not self.ce.current:
            print("No current project. Try to open one." if setting.language == 'en' else "没有当前项目。尝试打开一个。")
            self.cp_open()
            if not self.ce.current:
                return
        print(('Set project path: ' if setting.language == 'en' else '项目路径: ')
              + os.path.join(self.ce.current, 'Core'))
        minfo = self.get_collection()
        if not minfo:
            print("User canceled." if setting.language == 'en' else "用户取消。")
            return
        print(f"Mod Name: {minfo.name}" if setting.language == 'en' else f"模块名: {minfo.name}")
        print(f"Author: {minfo.author}" if setting.language == 'en' else f"作者: {minfo.author}")
        print(f"Brief: {minfo.brief}" if setting.language == 'en' else f"简介: {minfo.brief}")
        print(f"Desc: {minfo.desc}" if setting.language == 'en' else f"描述: {minfo.desc}")
        print(f"Adjust: {minfo.adjust}" if setting.language == 'en' else f"是否需要调整: {minfo.adjust}")
        print(f"C Files: {minfo.rel_c_files}" if setting.language == 'en' else f"C文件: {minfo.rel_c_files}")
        print(f"H Files: {minfo.rel_h_files}" if setting.language == 'en' else f"H文件: {minfo.rel_h_files}")
        if minfo:
            self.modularize(minfo)

    def exp(self):
        """
        Open the module directory in the explorer.
        :return:
        """
        os.startfile(MODS_DIR)

    def modularize(self, minfo:ModuleWizardCollection):
        """
        Create a module from the ModuleWizardCollection.
        :param minfo:
        :return:
        """
        # check if the module name exists
        if os.path.exists(os.path.join(MODS_DIR, minfo.name)):
            print(f"Module '{minfo.name}' exists. Will move old into 'backups'."
                    if setting.language == 'en' else
                    f"模块 '{minfo.name}' 已经存在。将会把旧的模块移动到 'backups' 中。")

            # create backup dir
            _backup_dir = os.path.join(MODS_DIR, 'backups')
            if not os.path.exists(_backup_dir):
                os.makedirs(_backup_dir)

            # backup the old lib
            last_change_time = os.path.getmtime(os.path.join(MODS_DIR, minfo.name))
            _backup_path = os.path.join(_backup_dir, f'backup_{minfo.name}_before_{datetime.datetime.fromtimestamp(last_change_time).strftime("%Y-%m-%d_%H-%M-%S")}')
            shutil.move(os.path.join(MODS_DIR, minfo.name), _backup_path)

        # create the module(zip)
        ignore_flag = False
        for ignore_prefix in VALID_MOD_PREFIXS:
            if minfo.name.startswith(ignore_prefix):
                ignore_flag = True
                break
        file_fname = f"mod_{minfo.name}" if not ignore_flag else minfo.name
        paths = minfo.rel_c_files + minfo.rel_h_files
        paths = [os.path.join(self.ce.current, f) for f in paths]
        print(f"Creating module '{minfo.name}'. Please wait..." if setting.language == 'en' else f"创建模块 '{minfo.name}' 中，请稍等...")
        zip_files(self.ce.current, paths, os.path.join(MODS_DIR, f'{file_fname}.zip'))

        # add info into
        if not HOME_F.has('MODS_INFO'):
            HOME_F.MODS_INFO = {}
        _infos:dict = HOME_F.MODS_INFO
        _infos[file_fname] = {
            'author': minfo.author,
            'brief': minfo.brief,
            'desc': minfo.desc,
            'adjust': minfo.adjust,
            'c_files': minfo.rel_c_files,
            'h_files': minfo.rel_h_files,
        }
        HOME_F.MODS_INFO = _infos

        print(f"Module '{minfo.name}' created." if setting.language == 'en' else f"模块 '{minfo.name}' 创建完成。")



    def get_collection(self):
        proj_path = self.ce.current
        if not os.path.exists(proj_path):
            print("Project path not exists." if setting.language == 'en' else "项目路径不存在。")
            return
        core_path = os.path.join(proj_path, 'Core')
        cs, hs = Module._ut_scan_individual_files(core_path)
        # 用户名
        default_author = os.path.basename(os.path.expanduser('~'))
        # 计算ch—files到core_path的相对路径
        chfiles = cs + hs
        chfiles = [os.path.relpath(f, core_path) for f in chfiles]
        chtree = Module._ut_build_path_tree(chfiles)
        # 计算默认模块名
        _DEFAULT_PNAME = 'untitled'
        if os.path.exists(os.path.join(MODS_DIR, "mod_" + _DEFAULT_PNAME)):
            i = 1
            while os.path.exists(os.path.join(_DEFAULT_DIR, f"mod_{_DEFAULT_PNAME}{i}")):
                i += 1
            _DEFAULT_PNAME = f"{_DEFAULT_PNAME}{i}"

        _DEFAULTS = {
            'name': _DEFAULT_PNAME,  # 'untitled
            'author': default_author,
            'brief': "This is a custom module.",
            'desc': "This is a custom module description."
        }

        # UI
        win = MyQWidget()
        win.setWindowTitle("Create New Module")
        win.setFixedSize(1060, 580)
        base_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        rside_layout = QVBoxLayout()
        base_layout.addLayout(left_layout)
        base_layout.addLayout(right_layout)
        base_layout.addLayout(rside_layout)

        ## 左侧
        l_tree = QTreeWidget()  # checkable
        l_tree.setFixedWidth(350)
        #设置列数
        l_tree.setColumnCount(1)
        #设置树形控件头部的标题
        l_tree.setHeaderLabels(['Select Files'])

        #设置根节点
        root=QTreeWidgetItem(l_tree)
        root.setText(0,'Core')

        # 设置树形控件的列的宽度
        l_tree.setColumnWidth(0, 160)

        # 根据chtree构建树
        def build_tree(tree, parent):
            for k, v in tree.items():
                if k == '_':
                    for _v in v:
                        child = QTreeWidgetItem(parent)
                        child.setCheckState(0, Qt.Unchecked)
                        child.setText(0, _v)
                else:
                    child = QTreeWidgetItem(parent)
                    child.setText(0, k)
                    build_tree(v, child)

        build_tree(chtree, root)
        # expand all
        l_tree.expandAll()
        left_layout.addWidget(l_tree)

        current_cs, current_hs = [], []

        def _get_leafs(item, dir='') -> dict:
            _leafs = {}
            if item.childCount() == 0:
                _leafs[dir + item.text(0)] = item
            else:
                for i in range(item.childCount()):
                    _leafs.update(_get_leafs(item.child(i), dir + item.text(0) + '/'))
            return _leafs

        def get_selects(added=None) -> tuple[list[str], list[str]]:
            """
            Get the selected files.
            :return: c_files, h_files
            """
            _c_files, _h_files = [], []
            _leafs = _get_leafs(l_tree.topLevelItem(0))
            for path, item in _leafs.items():
                if item.checkState(0) == Qt.Checked:
                    if item.text(0).endswith('.c') or item.text(0).endswith('.cpp'):
                        _c_files.append(path)
                    else:
                        _h_files.append(path)
            if added:
                for a in added:
                    if a.endswith('.c') or a.endswith('.cpp'):
                        _c_files.append(a)
                    else:
                        _h_files.append(a)
            return _c_files, _h_files


        timer = QTimer(win)
        timer.setInterval(5000)
        def update(*args):
            current_cs.clear()
            current_hs.clear()
            cs, hs = get_selects()
            current_cs.extend(cs)
            current_hs.extend(hs)

            # update edit_name
            if cs or hs:
                name = Module._ut_induce_name(cs, hs)
                edit_name.setPlaceholderText(name)
                _DEFAULTS['name'] = name

        timer.timeout.connect(update)
        timer.start()


        ## 右侧

        # "Mark as Need-Adjust:"
        cb_adjust = QCheckBox("Mark as Need-Adjust" if setting.language == 'en' else "标记为需要调整")
        right_layout.addWidget(cb_adjust)

        tip_layout = QHBoxLayout()
        right_layout.addLayout(tip_layout)
        lbl_name = QLabel("Mod Name:" if setting.language == 'en' else "模块名称:")
        lbl_import = QLabel("Inherit Info:" if setting.language == 'en' else "继承信息:")
        edit_name = QLineEdit()
        edit_name.setPlaceholderText(_DEFAULT_PNAME)
        tip_layout.addWidget(lbl_name)
        _tip_space = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        tip_layout.addItem(_tip_space)
        tip_layout.addWidget(lbl_import)
        right_layout.addWidget(edit_name)

        lbl_author = QLabel("Author:" if setting.language == 'en' else "作者:")
        edit_author = QLineEdit()
        edit_author.setPlaceholderText(default_author)
        right_layout.addWidget(lbl_author)
        right_layout.addWidget(edit_author)

        lbl_brief = QLabel("Brief:" if setting.language == 'en' else "简介:")
        edit_brief = QLineEdit()
        edit_brief.setPlaceholderText("This is a custom module.")
        right_layout.addWidget(lbl_brief)
        right_layout.addWidget(edit_brief)

        lbl_desc = QLabel("Description:" if setting.language == 'en' else "描述:")
        text_desc = QTextEdit()
        text_desc.setFixedWidth(450)
        text_desc.setPlaceholderText("This is a custom module description.")
        right_layout.addWidget(lbl_desc)
        right_layout.addWidget(text_desc)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        right_layout.addItem(spacer)

        line_layout = QHBoxLayout()
        btn_create = QPushButton("Create" if setting.language == 'en' else "创建")
        btn_cancel = QPushButton("Cancel" if setting.language == 'en' else "取消")
        line_layout.addWidget(btn_create)
        line_layout.addWidget(btn_cancel)
        right_layout.addLayout(line_layout)

        ## 右边侧
        lbl_info = QLabel("Select a mod-info to inherit:" if setting.language == 'en' else "选择继承信息的模块:")
        r_list = QListWidget()
        r_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        r_list.setSelectionMode(QAbstractItemView.SingleSelection)
        r_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        r_list.setSortingEnabled(True)
        r_list.setAlternatingRowColors(True)
        r_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        r_list.setDragDropMode(QAbstractItemView.NoDragDrop)
        # add mods()
        mods = Module.mods()
        mod_names = ['_'] + [m['name'] for m in mods]
        r_list.addItems(mod_names)
        rside_layout.addWidget(lbl_info)
        rside_layout.addWidget(r_list)
        def _rlist_item_changed():
            # fill the info
            _sel_name = r_list.currentItem().text()
            if _sel_name == '_':
                return
            _sel_mod = [m for m in mods if m['name'] == _sel_name][0]
            edit_name.setPlaceholderText(_sel_mod['name'])
            edit_author.setPlaceholderText(_sel_mod['author'])
            edit_brief.setPlaceholderText(_sel_mod['brief'])
            text_desc.setPlaceholderText(_sel_mod['desc'])
            cb_adjust.setChecked(_sel_mod['adjust'])
            _DEFAULTS['name'] = _sel_mod['name']
            _DEFAULTS['author'] = _sel_mod['author']
            _DEFAULTS['brief'] = _sel_mod['brief']
            _DEFAULTS['desc'] = _sel_mod['desc']

        r_list.currentItemChanged.connect(_rlist_item_changed)

        return_data = [False, None]  # can return?, module info
        def create_module():
            cs, hs = get_selects()
            if not cs and not hs:
                print("No file selected." if setting.language == 'en' else "没有选择文件。")
                QPop(RbpopError("No file selected." if setting.language == 'en' else "没有选择文件。", 'Not enough info:'))
                return
            name = edit_name.text()
            name = name if name else _DEFAULTS['name']
            author = edit_author.text()
            author = author if author else _DEFAULTS['author']
            brief = edit_brief.text()
            brief = brief if brief else _DEFAULTS['brief']
            desc = text_desc.toPlainText()
            desc = desc if desc else _DEFAULTS['desc']
            adjust = cb_adjust.isChecked()
            return_data[0] = True
            return_data[1] = ModuleWizardCollection(name, cs, hs, brief=brief, desc=desc, author=author, adjust=adjust)

            win.close()

        btn_create.clicked.connect(create_module)
        def cancel():
            return_data[0] = True
            win.close()

        btn_cancel.clicked.connect(cancel)

        win.setLayout(base_layout)
        win.setStyleSheet("font-size: 20px;")
        win.on_delete = cancel
        win.show()

        app = UISP.app
        while not return_data[0]:
            app.processEvents()

        return return_data[1]

    def __call__(self):
        # show mods by table like library
        _mods = Module.mods()
        if _mods:
            print(colorama.Fore.BLUE + f"Modules:{colorama.Fore.RESET}"
                  if setting.language == 'en' else
                  colorama.Fore.BLUE + f"模块列表:{colorama.Fore.RESET}")
            heads = ['Mod Name', 'Author', 'Brief', 'Files', 'Change Time'] \
                    if setting.language == 'en' else \
                    ['模块名称', '作者', '简介', "文件数", '修改时间']
            values = []
            for mod in _mods:
                cs = mod['c_files'] if mod['c_files'] else []
                hs = mod['h_files'] if mod['h_files'] else []
                values.append([mod['name'].upper(), mod['author'], mod['brief'], f"{len(cs)}C{len(hs)}H", mod['time']])
            print(str_table(heads, *values))

        else:
            print(f"No modules found."
                  if setting.language == 'en' else
                  f"未找到任何模块(use mod.new to create one)。")


if __name__ == '__main__':
    path = r"C:\Users\22290\Desktop\test_H7\Core"
    cs, hs = Module._ut_scan_individual_files(path)
    print(Module._ut_induce_name(cs, hs))

