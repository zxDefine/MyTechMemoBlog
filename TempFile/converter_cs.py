import json
import os
import re
from readline import insert_text

from store.subtitles_store import SubtitlesStore
from store.labels_store import LabelsStore
from store.source_store import SourceStore

# 生成static变量用
from converter_define_cs import CSharpStaticGenerator

#########################################################################################################
# 正式开发代码
#########################################################################################################
# 保存台词用list
SUBTITLES_STORE = SubtitlesStore('../../Renpy_Dragon_Unity/Dragon/Assets/RenpyResources/middle_data/dialogues.txt')

# 保存label用list
LABELS_STORE = LabelsStore('../../Renpy_Dragon_Unity/Dragon/Assets/RenpyResources/middle_data/labels.txt')

# 处理ID - 只是为了key不重复，没有任何意义
PROCESS_ID = 0

# 记录锁数
CURRENT_INDENT_NUM = 0

# 记录最后一个指令
LAST_COMMAND = ""

# 强制换行符
# FORCE_NEXT_LINE_SIGN = "/force_next_line"

# 加载define的内容
DEFINE_INFO = {}

# 加载所有的资源文件
ALL_SOURCE = {}

# 需要预加载的资源
PRE_LOAD_SOURCE = {}

# 删除冒号
def delete_colon(word:str):
    if word.endswith(':'):
        return word[:-1]
    return word

# 删除引号
def delete_double_sign(word:str):
    return word.replace('"', "")

# 是否含有数字
def has_num(words:str):
    nums ="0123456789"
    for num in nums:
        if words.find(num) != -1:
            return True
    return False

# 存储台词，并返回一个列表中的id
def save_subtitle(subtitile:str, file_path:str):
    global SUBTITLES_STORE

    # 添加新的对话数据
    subtitle_index = SUBTITLES_STORE.add(subtitile, file_path)
    assert subtitle_index != -1, "Error - save subtitles failed! {}".format(subtitile)

    # 返回当前数据的index
    return subtitle_index

# 存储label名，并返回一个列表中的id
def save_label_name(label_name:str, file_path:str):
    global LABELS_STORE

    # 保存label名
    file_name = get_file_name(file_path)
    label_index = LABELS_STORE.add(file_name, label_name, file_path)
    assert label_index != -1, "Error - save labels failed! {}".format(label_name)

    # 返回当前数据的index
    return label_index

# 获得指定文件路径的文件名
def get_file_name(file_path:str):
    # 提取文件名
    file_name_with_extension = os.path.basename(file_path)
    # 去掉扩展名
    file_name = os.path.splitext(file_name_with_extension)[0]
    return file_name

# 计算下一行的缩进数
def calc_next_line_indent_num(lines:[]):
    # 计算下一行的缩进数
    next_line_indent_num = 0
    if len(lines) > 0:
        # if FORCE_NEXT_LINE_SIGN in lines[0]:
        #     lines[0] = lines[0].replace(FORCE_NEXT_LINE_SIGN, "")
        #     next_line_indent_num = len(lines[0]) - len(lines[0].lstrip(' '))
        #     lines[0] = FORCE_NEXT_LINE_SIGN + lines[0]
        # else:
        #     next_line_indent_num = len(lines[0]) - len(lines[0].lstrip(' '))
        next_line_indent_num = len(lines[0]) - len(lines[0].lstrip(' '))
    return next_line_indent_num

# 返回空格数量
def calc_line_indent(current_line_indent_num):
    return "\n" + " " * (current_line_indent_num + 4)

# 检查这个define名称是否存在
# 返回在u3d中的正确的变量名列表
def check_define_name(word:str):
    global DEFINE_INFO
    target_key = delete_colon(word)
    return find_keys(DEFINE_INFO, target_key)

def find_keys(data, target_key, path=None):
    if path is None:
        path = []

    found_paths = []

    if isinstance(data, dict):
        for key, value in data.items():
            current_path = path + [key]
            if key == target_key:
                found_paths.extend(current_path)
            found_paths.extend(find_keys(value, target_key, current_path))
    elif isinstance(data, list):
        for index, item in enumerate(data):
            current_path = path + [f"[{index}]"]
            found_paths.extend(find_keys(item, target_key, current_path))

    return found_paths

# 组合成正确结构的变量名
def make_cs_name(key_list:[str]):
    cs_name = ""

    for item in key_list:
        cs_name = cs_name + item.capitalize() + "."

    return cs_name[:-1]

# 检查这个素材名是否存在
def get_source_file_path(name:str) -> str:
    global ALL_SOURCE
    return ALL_SOURCE.exists_images(name)

# 解析define的dict的内容
def converter_define():
    global DEFINE_INFO
    generator = CSharpStaticGenerator(DEFINE_INFO)
    lines = generator.generate()

    # 组成新的路径
    new_code_path = os.path.join(parent_dir,
                                 '..',
                                 'Renpy_Dragon_Unity',
                                 'Dragon',
                                 'Assets',
                                 'Script',
                                 'GameState.cs')

    # 规范化路径，防止路径中存在 '..' 没被解析
    new_code_path = os.path.normpath(new_code_path)

    # 获取该文件所在的目录
    target_dir = os.path.dirname(new_code_path)

    # 如果目录不存在，就创建目录（递归创建）
    os.makedirs(target_dir, exist_ok=True)

    # 最后组合成cs代码
    cs_code = "\n".join(lines)
    cs_code = '''// ReSharper disable InconsistentNaming\nusing System.Collections.Generic;
    \n''' + cs_code

    # 写入到对应文件中
    with open(new_code_path, "w", encoding="utf-8") as f:
        f.write(cs_code)

# 给上最后一个函数添加一个参数
def add_argument_to_last_pos(code_str, new_arg: str):
    interval_text = None
    # print("XXXXX ", code_str, "====> [{}]".format(new_arg))
    if code_str[-3] == "(" and new_arg[-2] != ",":
        interval_text = ""
    elif new_arg[-2] == ",":
        if code_str[-3] == "(":
            interval_text = ""
        else:
            interval_text = ", "
        new_arg = new_arg[:-2]
        # print("DDDD ", new_arg)
    elif new_arg[-2] == ")":
        interval_text = ""
        new_arg = new_arg[:-2]
        # print("WWWW ", new_arg)
    else:
        # print("EEEEE")
        interval_text = ","
    return code_str[:-2] + interval_text + new_arg + code_str[-2:]

# 获得unity3d里面的路径
def get_u3d_file_path(file_path:str):
    return "Assets/RenpyResources/" + file_path

# 添加预加载资源
def add_pre_load_source(file_path:str, file_type:str):
    global PRE_LOAD_SOURCE

    if file_type in PRE_LOAD_SOURCE.keys():
        PRE_LOAD_SOURCE[file_type].append(file_path)
    else:
        PRE_LOAD_SOURCE[file_type] = [file_path]

###############################################################
# 遍历每一行
def traversal_line(lines:list[str], cs_code:str, file_path:str):
    # 遍历每行内容
    while lines:
        # 使用全局变量存储
        # global FORCE_NEXT_LINE_SIGN
        global PROCESS_ID
        global CURRENT_INDENT_NUM
        global LAST_COMMAND

        # if FORCE_NEXT_LINE_SIGN in lines[0]:
        #     return

        # 计算当前的缩进数
        current_line_indent_num = len(lines[0]) - len(lines[0].lstrip(' '))

        # 检查当前的缩进数，来更新层级
        if CURRENT_INDENT_NUM > current_line_indent_num:
            # 结束本层级的遍历，返回上一层级
            CURRENT_INDENT_NUM = current_line_indent_num
            return cs_code

        # 获得当前行的数据
        line = lines.pop(0)

        # 如果有#注释，删除掉所有注释
        if "#" in line:
            delete_index = line.find("#")
            # 如果前一个不是"，不是被引用的状态的话
            if line[delete_index-1] != '"':
                line = line[:delete_index]

        # 把每行的内容拆成逐个关键字
        words = line.strip().split()

        # 如果一行都是空格的话，跳过此次循环
        if len(words) < 1:
            continue

        # 提取第一个关键字
        first_word = delete_colon(words[0])

        # 判断本行末时候有冒号
        has_end_colon_word = words[-1][-1] == ":"

        # 最后保存用的dict
        save_dict = {}
        cs_code_temp = ""

        # 当前的解析id
        current_function_id = ""

        # 强制同层 - play那样，非:嵌套里面的同行对应
        # 保存强制同层时候的key名顺序
        force_same_line_key_list = []

        # 注释
        if first_word == "#":
            continue

        # 开始解析
        if first_word == "label":
            # 获得label名
            label_name = delete_colon(words[1])
            save_label_name(label_name, file_path)

            # 添加一个label函数
            label_code = calc_line_indent(current_line_indent_num) + "public IEnumerator label_{}()".format(label_name)
            label_code += calc_line_indent(current_line_indent_num) + "{"

            # 添加到返回的cs代码中
            cs_code_temp += label_code

            # 解析完的数据全部pop掉
            words.pop(0)
            words.pop(0)

        elif first_word == "if":
            if "or" in words:
                # 判断条件
                condition1 = words[2]
                condition2 = words[6]

                # 保存if信息
                current_function_id = "if_{}".format(PROCESS_ID)
                PROCESS_ID += 1
                save_dict = {
                    current_function_id: {"function": "if", "op":"||", "data": [[words[1], condition1, delete_colon(words[3])], [words[5], condition2, delete_colon(words[7])]]}}

                # 解析完的数据全部pop掉
                # if1
                words.pop(0)
                words.pop(0)
                words.pop(0)
                words.pop(0)

                # or
                words.pop(0)

                # if2
                words.pop(0)
                words.pop(0)
                words.pop(0)

            elif "and" in words:
                # 判断条件
                condition1 = words[2]
                condition2 = words[6]

                # 保存if信息
                current_function_id = "if_{}".format(PROCESS_ID)
                PROCESS_ID += 1
                save_dict = {
                    current_function_id: {"function": "if", "op":"&&", "data": [[words[1], condition1, delete_colon(words[3])], [words[5], condition2, delete_colon(words[7])]]}}

                # 解析完的数据全部pop掉
                # if1
                words.pop(0)
                words.pop(0)
                words.pop(0)
                words.pop(0)

                # or
                words.pop(0)

                # if2
                words.pop(0)
                words.pop(0)
                words.pop(0)

            else:
                # 检查这个变量是不是登陆的变量
                key_list = check_define_name(words[1])
                # print(key_list)
                assert len(key_list) > 0,  "Error - if - Not exist define [{}]".format(words[1])

                # 添加一个if的代码块
                condition_name = make_cs_name(key_list)
                if_code = calc_line_indent(current_line_indent_num) + "if ({var1} {op} {var2})".format(var1=condition_name, op=words[2], var2=delete_colon(words[3]))
                if_code += calc_line_indent(current_line_indent_num) + "{"

                # 添加到返回的cs代码中
                cs_code_temp += if_code

                # 解析完的数据全部pop掉
                words.pop(0)
                words.pop(0)
                words.pop(0)
                words.pop(0)

        elif first_word == "else":
            # 保存if信息
            current_function_id = "else_{}".format(PROCESS_ID)
            PROCESS_ID += 1
            save_dict = {current_function_id: {"function": "else"}}

            # 解析完的数据全部pop掉
            words.pop(0)

        elif first_word == "show":
            # show - renpy语法 - 在某个图层上显示图片
            tex_name = delete_colon(words[1])

            # 检查这个变量是不是登陆过的变量
            show_code = ""
            if tex_name == "black":
                # 打开黑色贴图
                # 添加一个show的函数
                show_code = calc_line_indent(current_line_indent_num) + "yield return _gameMethods.OpenTextureBlack();"
            else:
                # 打开变量的贴图
                file_path = get_source_file_path(tex_name)
                assert file_path != "", "Error - show - Not exist define [{}]".format(tex_name)

                # 添加一个show的函数
                u3d_file_path = get_u3d_file_path(file_path)
                show_code = calc_line_indent(current_line_indent_num) + 'yield return _gameMethods.OpenTexture("{}");'.format(u3d_file_path)

                # 预读取准备
                add_pre_load_source(u3d_file_path, "image")

            # 添加到返回的cs代码中
            cs_code_temp += show_code

            # 解析完的数据全部pop掉
            words.pop(0)
            words.pop(0)

        elif first_word == "hide":
            # hide - renpy语法 - 将一个图像从图层中移除
            # 从图片名中获取图片标签(tag)，并将图层上该标签(tag)所对应的所有图像都移除。
            # 图片代称 todo:※需要寻找对应变量！！！
            tex_name = delete_colon(words[1])

            hide_code = ""
            if tex_name == "black":
                # 打开黑色贴图
                # 添加一个show的代码块
                hide_code = calc_line_indent(current_line_indent_num) + "yield return _gameMethods.CloseTextureBlack();"
            else:
                # 添加一个hide的代码块
                hide_code = calc_line_indent(current_line_indent_num) + "yield return _gameMethods.CloseTexture(GameState.{});".format(tex_name)

            # 添加到返回的cs代码中
            cs_code_temp += hide_code

            # 解析完的数据全部pop掉
            words.pop(0)
            words.pop(0)

        elif first_word == "scene":
            # scene - renpy语法 - scene语句会移除图层(layer)上所有的可视组件，并在该图层上显示一个图像
            # 场景语句开头是关键词 scene ，后面跟一个图像名，最后可能有若干个特性(property)
            # 图片代称 todo:※需要寻找对应变量！！！
            tex_name = delete_colon(words[1])

            # 检查这个变量是不是登陆过的变量
            res_list = check_define_name(tex_name)
            has_define = len(res_list) > 0
            # has_tex = get_define_word_convertered_list(tex_name)
            assert not has_define, "Error - scene - Not exist define [{}]".format(tex_name)

            # 添加一个scene的代码块
            scene_code = ""
            if tex_name is not None:
                # 跟show相同，显示图片
                if tex_name == "black":
                    # 打开黑色贴图
                    # 添加一个show的函数
                    scene_code = calc_line_indent(current_line_indent_num) + "yield return _gameMethods.OpenTextureBlack();"
                else:
                    # 打开变量的贴图
                    file_path = get_source_file_path(tex_name)
                    assert file_path != "", "Error - show - Not exist define [{}]".format(tex_name)

                    # 添加一个show的函数
                    u3d_file_path = get_u3d_file_path(file_path)
                    scene_code = calc_line_indent(current_line_indent_num) + 'yield return _gameMethods.OpenTexture("{}");'.format(u3d_file_path)

                    # 预读取准备
                    add_pre_load_source(u3d_file_path, "image")

            else:
                # 清空所有图片
                scene_code = calc_line_indent(current_line_indent_num) + "_gameMethods.CloseLayerAll();"

            # 添加到返回的cs代码中
            cs_code_temp += scene_code

            # 解析完的数据全部pop掉
            words.pop(0)
            words.pop(0)

        elif first_word == "with":
            # with - renpy语法 - 用于在场景切换时应用转场(transition)效果
            # with语句以关键词 with 开头，后跟一个简单表达式，该简单表达式可以转换为一个转场(transition)对象或者特殊值 None 。
            transition_data = delete_colon(words[1])

            # 保存with操作信息
            # current_function_id = "with_{}".format(PROCESS_ID)
            # PROCESS_ID += 1

            # 有转场类型+数值
            transition_code = ""
            if has_num(transition_data):
                if "Fade" in transition_data:
                    # 转场类型
                    transition_type = transition_data.split("(")[0]

                    # 转场数据
                    transition_value1 = words[1].replace("Fade", "").replace("(", "").replace(",", "")
                    transition_value2 = words[2].replace(",", "")
                    transition_value3 = words[3].replace(",", "")

                    # 颜色数据
                    transition_value4 = words[4].replace("color", "").replace("=", "").replace('"', "")

                    # 设计数据
                    save_dict = {current_function_id: {"function":"with_2_transition",
                                                       "data":{"type": transition_type,
                                                               "value":[transition_value1, transition_value2, transition_value3],
                                                               "color":transition_value4}}}

                    # 解析完的数据全部pop掉
                    words.clear()

                else:
                    # 转场类型
                    transition_type = transition_data.split("(")[0]
                    # 转场设置
                    transition_value = transition_data.split("(")[1].split(")")[0]

                    # 添加一个转场变化函数
                    if transition_type == "Dissolve":
                        if LAST_COMMAND in ["show", "hide", "camera"]:
                            cs_code = add_argument_to_last_pos(cs_code, "dissolve:{}f".format(transition_value))
                        else:
                            # 使用溶解效果切换新旧场景的转场效果。
                            transition_code = calc_line_indent(current_line_indent_num) + "yield return _gameMethods.TransitionDissolve({}f);".format(transition_value)

                    # 解析完的数据全部pop掉
                    words.pop(0)
                    words.pop(0)

            else:
                # 使用溶解效果切换新旧场景的转场效果。
                transition_code = calc_line_indent(current_line_indent_num) + 'yield return _gameMethods.Transition("{}");'.format(transition_data)

                # 解析完的数据全部pop掉
                words.pop(0)
                words.pop(0)

            # 添加到返回的cs代码中
            cs_code_temp += transition_code

        elif first_word[0] == '"':
            # 添加台词到台词专用数据库
            dialog_id = save_subtitle(line, file_path)

            # 添加一个dialog更新函数
            dialog_code = calc_line_indent(current_line_indent_num) + "yield return _gameMethods.OpenDialog({});".format(dialog_id)

            # 添加到返回的cs代码中
            cs_code_temp += dialog_code

            # 解析完的数据全部pop掉
            words.pop(0)

        elif first_word == 'subpixel':
            # subpixel - renpy语法 - 若为True，子组件将根据子像素(subpixel)确定位置。※todo:不懂是什么效果

            # 添加一个show的参数
            subpixel_code = "subpixel:{}".format("true" if delete_colon(words[1]) == "True" else "false")

            # 添加到返回的cs代码中
            cs_code_temp += subpixel_code + ", "

            # 解析完的数据全部pop掉
            words.pop(0)
            words.pop(0)

        elif first_word == "pos":
            # pos - renpy语法 - 相对坐标，以整个区域左上角为原点。
            # 获得数据 (x, y)
            # x
            x = words[1]
            x = x.replace("(", "")
            x = x.replace(",", "")

            # y
            y = words[2]
            y = y.replace(")", "")

            # 添加一个show的参数
            pos_code = "pos:new Vector2({}f, {}f)".format(x, y)

            # 添加到返回的cs代码中
            cs_code_temp += pos_code + ", "

            # 解析完的数据全部pop掉
            words.pop(0)
            words.pop(0)
            words.pop(0)

        elif first_word == "camera":
            # camera - renpy语法 - 这个语句与 show layer 语句相似，但 camera 语句不需要指定图层名，也不会在使用 scene 语句后清除效果。
            # perspective True，就能启用3D舞台系统。※todo:不是很懂作用

            # 添加一个camera的代码块
            camera_code = calc_line_indent(current_line_indent_num) + "_gameMethods.SetCamera();"

            # 添加到返回的cs代码中
            cs_code_temp += camera_code

            # 解析完的数据全部pop掉
            words.pop(0)

        elif first_word == "perspective":
            # perspective - renpy语法 - 该特性应用到某个变换时，启用透视渲染效果。 特性值应该是个3元元组，分别表示最近平面、1:1平面z轴距离和最远平面。

            # 添加一个perspective的参数
            perspective_code = "perspective:{}".format("true" if delete_colon(words[1]) == "True" else "false")

            # 添加到返回的cs代码中
            cs_code_temp += perspective_code + ", "

            # 解析完的数据全部pop掉
            words.pop(0)
            words.pop(0)

        elif first_word == "gl_depth":
            # gl_depth - renpy语法 - 可以让GPU根据深度 gl_depth 排列图像顺序

            # 添加一个gl_depth的参数
            gl_depth_code = "gl_depth:{}".format("true" if delete_colon(words[1]) == "True" else "false")

            # 添加到返回的cs代码中
            cs_code_temp += gl_depth_code + ", "

            # 解析完的数据全部pop掉
            words.pop(0)
            words.pop(0)

        elif first_word == "anchor":
            # anchor - renpy语法 - 锚点坐标，以可视组件左上角为原点。※todo:中心左边？
            # 获得数据 (x, y)
            # x
            x = words[1]
            x = x.replace("(", "")
            x = x.replace(",", "")

            # y
            y = words[2]
            y = y.replace(")", "")

            # 添加一个show的参数
            anchor_code = "anchor:new Vector2({}f, {}f)".format(x, y)

            # 添加到返回的cs代码中
            cs_code_temp += anchor_code + ", "

            # 解析完的数据全部pop掉
            words.pop(0)
            words.pop(0)
            words.pop(0)

        elif first_word == "xpos":
            # xpos - renpy语法 - 水平坐标，以整个区域的最左端为坐标零点。

            # 添加一个xpos的参数
            xpos_code = "xpos:{}f".format(delete_colon(words[1]))

            # 添加到返回的cs代码中
            cs_code_temp += xpos_code + ", "

            # 解析完的数据全部pop掉
            words.pop(0)
            words.pop(0)

        elif first_word == "ypos":
            # ypos - renpy语法 - 垂直坐标，以整个区域的最上端为坐标零点。

            # 添加一个xpos的参数
            ypos_code = "ypos:{}f".format(delete_colon(words[1]))

            # 添加到返回的cs代码中
            cs_code_temp += ypos_code + ", "

            # 解析完的数据全部pop掉
            words.pop(0)
            words.pop(0)

        elif first_word == "zpos":
            # zpos - renpy语法 - 改特性表示子组件在z轴方向的偏移。 当perspective特性值是False时，可以直接使用该特性值，否则需要乘以-1后再使用。
            # 如果设置该特性后子组件消失，可能的原因是作为父组件的可视组件本身的zpos是False。

            # 添加一个xpos的参数
            zpos_code = "zpos:{}f".format(delete_colon(words[1]))

            # 添加到返回的cs代码中
            cs_code_temp += zpos_code + ", "

            # 解析完的数据全部pop掉
            words.pop(0)
            words.pop(0)

        elif first_word == "zoom":
            # zoom - renpy语法 - 若该特性值为True，1:1平面(zone)的z轴距离将于该可视组件的zpos值保持一致。 子组件则根据 (zone - zpos) / zone 在x和y轴缩放。
            # 改特性用作背景的可视组件，在 zpos 为负值的情况下，不会出现显示过小无法覆盖整个屏幕的情况。 该项设置为True后，背景图像始终将以1:1的比例显示。
            value = delete_colon(words[1])

            # 添加一个show的参数
            zoom_code = "zoom:{}f".format(value)

            # 添加到返回的cs代码中
            cs_code_temp += zoom_code + ", "

            # 解析完的数据全部pop掉
            words.pop(0)
            words.pop(0)

        elif first_word == "yoffset":
            # yoffset - renpy语法 - 可视组件在垂直方向偏离的像素数。向下偏离时是正数。
            value = delete_colon(words[1])

            # 保存yoffset信息
            current_function_id = "yoffset_{}".format(PROCESS_ID)
            PROCESS_ID += 1
            save_dict = {current_function_id: {"function":"yoffset", "data":value}}

            # 解析完的数据全部pop掉
            words.pop(0)
            words.pop(0)

        elif first_word == "pause":
            # pause - renpy语法 - 可以让整个Ren’Py进程暂停，直到出现鼠标单击事件
            # 如果pause语句中给定一个数字，就只会暂停数字对应的秒数。
            value = delete_colon(words[1])

            # 保存pause信息
            current_function_id = "pause_{}".format(PROCESS_ID)
            PROCESS_ID += 1
            save_dict = {current_function_id: {"function":"pause", "data":value}}

            # 解析完的数据全部pop掉
            words.pop(0)
            words.pop(0)

        elif first_word == "easein_circ":
            # easein_circ - renpy语法 - 对应一种曲线变化的算法
            # 参见 https://doc.renpy.cn/zh-CN/transforms.html
            value = delete_colon(words[1])

            # 保存easein_circ信息
            current_function_id = "easein_circ_{}".format(PROCESS_ID)
            PROCESS_ID += 1
            save_dict = {current_function_id: {"function":"easein_circ", "data":value}}

            # 解析完的数据全部pop掉
            words.pop(0)
            words.pop(0)

        elif first_word == "alpha":
            # alpha - renpy语法 - 该值控制可视组件的不透明度
            value = delete_colon(words[1])

            # 保存zoom信息
            current_function_id = "alpha_{}".format(PROCESS_ID)
            PROCESS_ID += 1
            save_dict = {current_function_id: {"function":"alpha", "data":value}}

            # 解析完的数据全部pop掉
            words.pop(0)
            words.pop(0)

        elif first_word == "linear":
            # linear - renpy语法 - todo:线性调整？单位是时间？HP没有
            value = delete_colon(words[1])

            # 保存zoom信息
            current_function_id = "linear_{}".format(PROCESS_ID)
            PROCESS_ID += 1
            save_dict = {current_function_id: {"function":"linear", "data":value}}

            # 解析完的数据全部pop掉
            words.pop(0)
            words.pop(0)

        elif first_word == "blur":
            # blur - renpy语法 - 使用 blur 像素数模糊图像的子组件， blur 数值不超过可视组件的边长。
            # Ren’Py不同版本的模糊细节可能存在差异。模糊的结果可能存在瑕疵，尤其是模糊数值不断发生修改的情况下。

            # 添加一个blur的参数
            blur_code = "blur:{}f".format(delete_colon(words[1]))

            # 添加到返回的cs代码中
            cs_code_temp += blur_code + ", "

            # 解析完的数据全部pop掉
            words.pop(0)
            words.pop(0)

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # Creator:ZX
        elif first_word == "play":
            # play - renpy语法 - 语句用于播放音效和音乐。
            # ※※※如果某个文件正在通过通用通道播放，播放会被中断，并开始播放新的文件。

            # 根据不同channel进行判断
            play_code = ""
            sound_channel = delete_colon(words[1])
            if sound_channel == "sound":
                sound_file = delete_double_sign(delete_colon(words[2]))

                # 添加一个play函数的代码
                play_code = calc_line_indent(current_line_indent_num) + '_gameMethods.PlaySound(soundChannel:"{}", soundPath:"{}");'.format(sound_channel, sound_file)

                # 解析完的数据全部pop掉
                words.pop(0)
                words.pop(0)
                words.pop(0)

            elif sound_channel == "sounda" or sound_channel == "soundb" or sound_channel == "soundc" or sound_channel == "music":
                # 拿到复杂设置的sound_setting

                # # 添加一个play函数的代码
                # play_code = calc_line_indent(current_line_indent_num) + '_gameMethods.PlaySound(soundChannel:"{}", '.format(sound_channel)
                #
                # # 额外信息保存
                # play_info = {}
                # param_list_code = ""
                #
                # # 如果后续有携带参数链
                # if line.find("[") != -1:
                #     # 拿到[]内的参数
                #     # 找到括号左边位置
                #     left = line.find("[")
                #     right = line.find("]")
                #     bracket_command = line[left+1:right-1]
                #
                #     # 判断是一个audio还是多个audio
                #     audio_num = bracket_command.count(".mp3")
                #     play_code = "" if audio_num > 1 else play_code
                #
                #     # 循环[]内的参数
                #     bracket_command_words = bracket_command.split(",")
                #     for word in bracket_command_words:
                #         # print(word)
                #         if word.find("audio") != -1:
                #             # 携带文件信息
                #             value_command = word.split(">")
                #
                #             # 设置信息
                #             setting_info = value_command[0].replace('"', "").replace("<", "").strip().split(" ")
                #             # print(setting_info)
                #
                #             if setting_info[0] == "from":
                #                 # 添加播放文件, 跟指定的播放区间
                #                 param_list_code += '{}_start:{}f, {}_end:{}f, soundPath:"{}",'.format(setting_info[0], setting_info[1], setting_info[0], setting_info[3], value_command[1])
                #
                #             elif len(setting_info) == 1:
                #                 # 添加播放文件, 跟指定的播放区间
                #                 if audio_num == 1:
                #                     param_list_code += 'soundPath:"{}",'.format(value_command[0].replace('"', "").strip())
                #                 elif audio_num > 1:
                #                     play_code = play_code + calc_line_indent(current_line_indent_num) + '_gameMethods.PlaySound(soundChannel:"{}", soundPath:"{}"'.format(sound_channel, value_command[0].replace('"', "").strip())
                #             else:
                #                 assert False, "Error - Illegal [{}] info [{}]".format(sound_channel, setting_info)
                #
                #         elif word.find("silence") != -1:
                #             # 一段指定时间范围播放静音，格式类似“<silence 3.0>”，其中3.0表示需要的静音持续时间，单位为秒
                #             setting_info = word.replace('"', "").replace("<", "").replace(">", "").strip().split(" ")
                #
                #             # 添加静音的参数
                #             play_code = calc_line_indent(current_line_indent_num) + 'yield return _gameMethods.SilenceSound(soundChannel:"{}", time:{}f);'.format(sound_channel,setting_info[1]) + play_code
                #
                #         else:
                #             # 只是单纯设定
                #             value_command = word.replace('"', "").replace("<", "").replace(">", "").split(" ")
                #             play_info.update({value_command[0]:value_command[1]})
                #
                #     # 重塑，去掉play channel info后的line string
                #     new_line = line[right+2:]
                #     words = new_line.split(" ")
                #
                #     # 组合函数
                #     play_code += param_list_code + ")"
                #
                # else:
                #     sound_file = delete_colon(words[2])
                #     play_info.update({"sound_file":sound_file.replace('"', "").strip()})
                #
                #     # 重塑，去掉play channel info后的line string
                #     words = words[3:]
                #
                #     # 记录同行信息的保存位置
                #     force_same_line_key_list = [current_function_id, "data", "play_info"]

                # save_dict = {current_function_id: {"function": "play", "data": {"channel_name":sound_channel,"play_info":play_info}}}

                # 添加一个注释函数 - 解析完成后可以删除
                play_code = calc_line_indent(current_line_indent_num) + '// {}'.format(line.strip())

                # 清除解析行
                words.clear()

            else:
                assert False, "Error - Illegal play [{}]".format(sound_channel)

            # 添加到返回的cs代码中
            # print(play_code)
            cs_code_temp += play_code
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        elif first_word == "volume":
            # volume - renpy语法 - 指定音量值，音量范围为0.0到1.0

            # 添加一个volume的参数
            volume_code = "volume:{}f".format(delete_colon(words[1]))

            # 添加到返回的cs代码中
            cs_code_temp += volume_code + ", "

            # 解析完的数据全部pop掉
            words.pop(0)
            words.pop(0)

        elif first_word == "stop":
            # stop - renpy语法 - 后面跟需要静音的音频通道名
            # 最后有一个可选的 fadeout 分句。 如果没有fadeout时间没有指定，就使用 config.fadeout_audio 的配置值。
            sound_channel = delete_colon(words[1])

            # 添加一个stop的函数
            stop_code = calc_line_indent(current_line_indent_num) + '_gameMethods.StopSound(soundChannel:"{}");'.format(sound_channel)

            # 添加到返回的cs代码中
            cs_code_temp += stop_code

            # 解析完的数据全部pop掉
            words.pop(0)
            words.pop(0)

        elif first_word == "fadeout":
            # fadeout - renpy语法 - 【音乐】渐出

            # 添加一个fadeout的参数
            fade_out_code = "fadeOut:{}f".format(delete_colon(words[1]))

            # 添加到返回的cs代码中
            cs_code_temp += fade_out_code + ", "

            # 解析完的数据全部pop掉
            words.pop(0)
            words.pop(0)

        elif first_word == "fadein":
            # fadein - renpy语法 - 【音乐】渐入

            # 添加一个fadeout的参数
            fade_in_code = "fadeIn:{}f".format(delete_colon(words[1]))

            # 添加到返回的cs代码中
            cs_code_temp += fade_in_code + ", "

            # 解析完的数据全部pop掉
            words.pop(0)
            words.pop(0)

        elif first_word == "$":
            # renpy引擎调用

            # 需要保存的信息
            function = ""
            param = {}

            # 引擎内的操作
            inside_code = ""

            # 区别调用的是什么处理
            inside_words = words[1].split(".")
            if inside_words[0] == "renpy":
                if inside_words[1] == "music":
                    if inside_words[2].find("set_volume") != -1:
                        # function = "set_volume"

                        # 提取各个参数
                        volume = words[1].split("(")[1].replace(",", "")
                        # print(volume)

                        value2_command = words[2].split("=")
                        delay = value2_command[1].replace(",", "")
                        # print(delay)

                        value3_command = words[3].split("=")
                        sound_channel = value3_command[1].replace(")", "").replace("'", "")
                        # print(sound_channel)

                        # 添加一个set_volume的函数
                        inside_code = calc_line_indent(current_line_indent_num) + '_gameMethods.SetVolume(soundChannel:"{}", volume:{}f, delay:{}f);'.format(sound_channel, volume, delay)

                        # 解析完的数据全部pop掉
                        words.clear()

                    else:
                        assert False, "Error - $ {}".format(inside_words[0])
                else:
                    assert False, "Error - $ {}".format(inside_words[0])

            elif inside_words[0] == "persistent":
                # 只要游戏运行就始终保留值的修改结果，甚至读档都不影响持久化对象
                # 永久保持变量
                # function = "static_value"
                variable_name = words[1]
                # print(variable_name)
                # param = {"variable_name":variable_name, "value":words[3] if words[3].find("#") == -1 else words[3][:words[3].find("#")]}

                # 解析完的数据全部pop掉
                words.pop(0)
                words.pop(0)
                words.pop(0)
                words.pop(0)

            else:
                # 默认是全局变量名
                # 算式赋值
                if words[1] == words[3] and words[2] == "=" and words[4] == "+":
                    function = "static_value"
                    variable_name = words[1]
                    param = {"variable_name": variable_name,
                             "op":"+",
                             "value": words[-1]}

                    # 解析完的数据全部pop掉
                    words.clear()

                # 直接赋值
                elif words[2] == "=":
                    function = "static_value"
                    variable_name = words[1]
                    param = {"variable_name": variable_name,
                             "op": "=",
                             "value": words[-1]}

                    # 解析完的数据全部pop掉
                    words.clear()

                # assert False, "Error - $ {}".format(inside_words[0])

            # 保存对话操作信息
            current_function_id = "engine_{}".format(PROCESS_ID)
            PROCESS_ID += 1
            save_dict = {current_function_id: {"function":function, "param":param}}

            # 添加到返回的cs代码中
            cs_code_temp += inside_code

        elif first_word == "menu":
            # menu - renpy语法 - 该函数向用户显示一个菜单
            # 在每个元组中，第一个元素是一个文本标签(label)，第二个参数是该元素被选中时的返回值

            # 保存menu信息
            current_function_id = "menu_{}".format(PROCESS_ID)
            PROCESS_ID += 1
            save_dict = {current_function_id:{"function":"select_menu", "sons":{}}}

            # 解析完的数据全部pop掉
            words.pop(0)

        elif first_word == "jump":
            # jump - renpy语法 - 结束当前语句，并让主控流程跳转到给定的脚本标签(label)

            # 获得label_id
            label_name = words[1]
            label_id = save_label_name(label_name, file_path)

            # 保存jump信息
            current_function_id = "jump_{}".format(PROCESS_ID)
            PROCESS_ID += 1
            save_dict = {current_function_id:{"function":"jump_to", "label_id":label_id}}

            # 解析完的数据全部pop掉
            words.pop(0)
            words.pop(0)

        elif first_word == "voice":
            # voice - renpy语法 - 播放指定的语音

            # 语音文件
            voice_path = words[1]

            # 保存voice信息
            current_function_id = "voice_{}".format(PROCESS_ID)
            PROCESS_ID += 1
            save_dict = {current_function_id:{"function":"play_voice", "voice_path":voice_path}}

            # 解析完的数据全部pop掉
            words.pop(0)
            words.pop(0)

        elif first_word == "return":
            # return - renpy语法 - 结束当前label的内容

            # 保存voice信息
            current_function_id = "return_{}".format(PROCESS_ID)
            PROCESS_ID += 1
            save_dict = {current_function_id:{"function":"return"}}

            # 解析完的数据全部pop掉
            words.pop(0)

        elif first_word == "extend":
            # extend - renpy语法 - 使用最近一个发言角色，在原有对话内容后追加一行台词。
            # 快速扩展对话。这可以用于界面变更后的对话内容延续

            # 保存extend信息
            current_function_id = "extend_{}".format(PROCESS_ID)
            PROCESS_ID += 1
            save_dict = {current_function_id:{"function":"extend"}}

            # 解析完的数据全部pop掉
            words.pop(0)

        elif first_word == "python":
            # python - renpy语法 - 调用python功能
            # 跳过

            # 保存python信息
            current_function_id = "extend_{}".format(PROCESS_ID)
            PROCESS_ID += 1
            save_dict = {current_function_id:{"function":"python_function"}}

            # 解析完的数据全部pop掉
            words.pop(0)

        elif "achievement" in first_word:
            # 成就系统解锁
            inside_words = line.strip().replace("achievement", "").replace(".", "").split("(")

            # 添加成就
            if inside_words[0] == "grant":
                grant_value = inside_words[1].replace('"', "").replace(")", "")

                # 保存成就信息
                current_function_id = "achievement_{}".format(PROCESS_ID)
                PROCESS_ID += 1
                save_dict = {current_function_id:{"function":"achievement_grant", "value":grant_value}}

            # 同步更新成就
            elif inside_words[0] == "sync":
                # 保存成就信息
                current_function_id = "achievement_{}".format(PROCESS_ID)
                PROCESS_ID += 1
                save_dict = {current_function_id:{"function":"achievement_sync"}}

            # 强制报错
            else:
                assert False, "Error - achievement {}".format(inside_words)

            # 解析完的数据全部pop掉
            words.clear()

        else:
            # 检查这个变量是不是define的变量
            assert check_define_name(first_word), "Error - var - Not exist define [{}]".format(first_word)

            # 存储疑似变量的值
            variables = []
            words.pop(0)
            variables.append({"variable_name": first_word})

            # 将剩下的也作为变量存入
            while words:
                # 拿到当前的变量
                var = words.pop(0)
                if var == ":":
                    break

                var = delete_colon(var)

                if var[0] == '"':
                    # 字幕类型
                    # 保存对话操作信息
                    dialog_id = save_subtitle(var, file_path)
                    variables.append({"subtitle_id": dialog_id})

                else:
                    # 变量类型
                    variables.append({"variable_name": var})

            # 把变量列表存储起来
            current_function_id = "variable_{}".format(PROCESS_ID)
            PROCESS_ID += 1
            save_dict = {current_function_id: {"function": "variable", "variables": variables}}

            # 还未对应报错
            # assert False, "Error - Not exist word[{}]".format(first_word)

        # 更新当前行的缩进数
        CURRENT_INDENT_NUM = current_line_indent_num

        # 同行处理
        if len(words) > 0:
            # 组成新的同行string，并且插入到lines的最上面
            same_line = " ".join(words)
            same_line = " " * current_line_indent_num + same_line

            # 获得同级数据
            same_line_code = ""
            same_line_code = traversal_line([same_line], same_line_code, file_path)

            # 解析完的数据全部pop掉
            words.clear()

            # 再次更新当前行的缩进数
            CURRENT_INDENT_NUM = current_line_indent_num

            # 针对函数进行补完
            # play解析重写
            # if first_word == "play":
            #     if same_line_code[-2] == ",":
            #         same_line_code = same_line_code[:-2]
            #         same_line_code += ")"
            #     cs_code_temp = cs_code_temp[:-2] + ", "
            #     cs_code_temp += same_line_code + ";"

            if first_word == "stop":
                if same_line_code[-2] == ",":
                    same_line_code = same_line_code[:-2]
                    same_line_code += ")"
                cs_code_temp = cs_code_temp[:-2] + ", "
                cs_code_temp += same_line_code + ";"

            else:
                cs_code_temp += same_line_code

        # 如果有冒号的话，进行嵌套的解析
        if has_end_colon_word:
            # 获得嵌套数据
            colon_code = ""

            # 再获取一行看看是不是出于同一个引号层级下面
            if len(lines) > 0:
                # 遍历层级下的内容
                colon_code = traversal_line(lines, colon_code, file_path)
                # print(colon_code)

                # 再次更新当前行的缩进数
                CURRENT_INDENT_NUM = current_line_indent_num

                # 针对函数进行补完
                if first_word == "show":
                    # if colon_code[-2] == ",":
                    #     colon_code = colon_code[:-2]
                    #     colon_code += ")"
                    # cs_code_temp = cs_code_temp[:-2] + ", "
                    # cs_code_temp += colon_code + ";"
                    cs_code_temp = add_argument_to_last_pos(cs_code_temp, colon_code)

                elif first_word == "camera":
                    # if colon_code[-2] == ",":
                    #     colon_code = colon_code[:-2]
                    #     colon_code += ")"
                    # cs_code_temp = cs_code_temp[:-2]
                    # cs_code_temp += colon_code + ";"
                    cs_code_temp = add_argument_to_last_pos(cs_code_temp, colon_code)

                else:
                    cs_code_temp += colon_code

                    # 补完反括号
                    cs_code_temp += calc_line_indent(current_line_indent_num) + "}"

                # # 如果有嵌套的话，存入之前保存的
                # if "sons" in save_dict[current_function_id]:
                #     save_dict[current_function_id]["sons"].update(colon_dict)
                # else:
                #     save_dict[current_function_id]["sons"] = colon_dict

            # 没有余下内容的话，加一个反括号
            # else:

        # 保存解析的数据
        # ret_dict.update(save_dict)
        # print(cs_code_temp)
        # print(cs_code)
        cs_code += cs_code_temp
        # print(cs_code)

        # 重置save_dict
        save_dict = {}

        # 清除同行设置
        force_same_line_key_list = []

        # 记录最后一个执行的command
        LAST_COMMAND = first_word

        if len(lines) == 0:
            # print("ret ", cs_code)
            return cs_code


# 主要处理
def converter(content:str, file_path:str, test_line_num:int):
    # 返回转换好的cs代码
    file_name = get_file_name(file_path)
    cs_code = '''using System.Collections;
using UnityEngine;

public class {file_name} : ILabelProvider
'''.format(file_name=file_name)
    cs_code += "{"

    # 添加函数控制器
    cs_code += '''
    private GameMethods _gameMethods;
    
    public {file_name}(GameMethods gameMethods)
    '''.format(file_name=file_name)

    cs_code += '''{
        _gameMethods = gameMethods;
    }
    '''

    # 分割rpy代码成每行
    lines = content.strip().splitlines()
    if test_line_num > 0:
        lines = lines[:test_line_num]

    # 遍历每一行的数据，在进行转换
    cs_code = traversal_line(lines, cs_code, file_path)

    # 添加class的结尾括号
    cs_code += "\n" + "}"

    return cs_code


if __name__ == '__main__':
    ############################## 1.读取原始代码
    # 获取当前的文件路径
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 获取上一层级的文件路径
    parent_dir = os.path.dirname(current_dir)

    # 拼接目标模块所在的路径
    origin_code_path = os.path.join(parent_dir,
                               'middle_code',
                               'game',
                               'rpy',
                               'zhuxian',
                               'guodu',
                               'fanhuitu.rpy')

    # 规范化路径，防止路径中存在 '..' 没被解析
    origin_code_path = os.path.normpath(origin_code_path)

    # 读取原始代码
    with open(origin_code_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # 读取define, source, default的设定并进行转译
    # 读取第一个 JSON 文件
    try:
        with open("../code/defines_converte.json", 'r', encoding='utf-8') as f:
            DEFINE_INFO.update(json.load(f))
    except FileNotFoundError:
        open("../code/defines_converte.json", 'w', encoding='utf-8').close()

    # 读取第二个 JSON 文件
    try:
        with open("../code/defaults_converte.json", 'r', encoding='utf-8') as f:
            DEFINE_INFO.update(json.load(f))
    except FileNotFoundError:
        open("../code/defaults_converte.json", 'w', encoding='utf-8').close()
    converter_define()

    # 加载所有的资源文件
    ALL_SOURCE = SourceStore("../../dragon/files.txt")

    ####################2.预处理每行的信息
    converted_cs_code = converter(code, origin_code_path, 392)

    ####################3. 将转换好的代码，写入到middle下的对应文件位置
    # 组成新的路径
    new_code_path = os.path.join(parent_dir,
                                 '..',
                                 'Renpy_Dragon_Unity',
                                 'Dragon',
                                 'Assets',
                                 'Script',
                                 'GameScript',
                                 'game',
                                 'rpy',
                                 'zhuxian',
                                 'guodu',
                                 'fanhuitu.cs')

    # 规范化路径，防止路径中存在 '..' 没被解析
    new_code_path = os.path.normpath(new_code_path)

    # 获取该文件所在的目录
    target_dir = os.path.dirname(new_code_path)

    # 如果目录不存在，就创建目录（递归创建）
    os.makedirs(target_dir, exist_ok=True)

    # 写入到对应文件中
    with open(new_code_path, "w", encoding="utf-8") as f:
        f.write(converted_cs_code)

    # 与加载文件
    print("预加载文件dict: ", PRE_LOAD_SOURCE)

    # 预处理结束
    print("Done!")