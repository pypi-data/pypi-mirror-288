import subprocess
from pathlib import Path
from matplotlib import font_manager, rcParams
import matplotlib.ticker as mtick
from matplotlib.ticker import MultipleLocator

import os
from os.path import join
import platform
import sci_plot_style

sci_plot_path = sci_plot_style.__path__[0]
pfont_path = join(sci_plot_path, 'styles', 'fonts')

def get_font_path(font_name):
    system = platform.system()
    font_path = None

    if system == 'Windows':
        # 检查系统字体目录
        system_font_path = os.path.join(os.environ['WINDIR'], 'Fonts', font_name)
        # 检查用户字体目录
        user_font_path = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Microsoft', 'Windows', 'Fonts', font_name)
        # python包目录
        package_font_path = join(pfont_path, font_name)
        if os.path.exists(system_font_path):
            font_path = system_font_path
        elif os.path.exists(user_font_path):
            font_path = user_font_path
        elif os.path.exists(package_font_path):
            font_path = package_font_path
    elif system == 'Darwin':  # macOS
        font_path = f'/Library/Fonts/{font_name}'
    elif system == 'Linux':
        font_path = f'/usr/share/fonts/{font_name}'
    else:
        raise FileNotFoundError(f"无法识别的操作系统，无法确定字体路径: {font_name}")


    return font_path

# 定义一个函数,用于设置字体
def set_font(font_size=10, font_name="times.ttf"):
    font_path = get_font_path(font_name)
    # 字体加载
    font_manager.fontManager.addfont(font_path)
    prop = font_manager.FontProperties(fname=font_path)

    # 字体设置
    rcParams["font.family"] = "sans-serif"  # 使用字体中的无衬线体
    rcParams["font.sans-serif"] = prop.get_name()  # 根据名称设置字体
    rcParams["font.size"] = font_size  # 设置字体大小
    rcParams["axes.unicode_minus"] = False  # 使坐标轴刻度标签正常显示正负号
    rcParams["svg.fonttype"] = "none"


def plot_as_emf(figure, **kwargs):
    # 获取inkscape_path
    inkscape_path = kwargs.get("inkscape_path", None)
    # 获取文件路径
    filepath = kwargs.get("filepath", None)
    # 获取dpi
    dpi = kwargs.get("dpi", 300)
    # 判断inkscape_path是否为空
    if inkscape_path is None:
        print("inkscape_path未指定")
    else:
        # 获取inkscape_path的路径
        inkscape_path = Path(inkscape_path).resolve()
    # 判断文件路径是否为空
    if filepath is not None:
        # 获取文件路径的路径
        filepath = Path(filepath).resolve()
        # 获取文件路径和文件名
        filepath, filename = filepath.parent, filepath.name
        filename = filepath.stem
        # 获取svg文件路径
        svg_filepath = filepath / f"{filename}.svg"
        # 获取emf文件路径
        emf_filepath = filepath / f"{filename}.emf"
        # 保存svg文件
        figure.savefig(svg_filepath, format="svg", dpi=dpi)
        # 将svg文件转换为emf文件
        subprocess.call(
            [inkscape_path, svg_filepath, "--export-type=emf", emf_filepath]
        )
        print(f"{emf_filepath} 生成成功")


# 定义一个函数,用于设置图表的样式
def set_style(
    ax,
    minorticks=True,
    x_minor=True,
    y_minor=True,
    xtick=None,
    yticks=None,
    visible_ticks_top_right=True,
    format=["%.1f", "%.1f"],
):

    '''设置图表的样式
    参数:
    ax:plt.axes对象,用于设置样式
    minorticks:bool,表示是否显示副刻度线
    x_minor:bool,表示是否显示x轴的副刻度线
    y_minor:bool,表示是否显示y轴的副刻度线
    xtick:float,表示x轴的主刻度线间隔
    yticks:float,表示y轴的主刻度线间隔
    visible_ticks_top_right:bool,表示是否去除上轴刻度
    format:list,表示x轴和y轴的主刻度线格式
    '''
    # 设置主刻度线间隔
    if xtick is not None:
        ax.xaxis.set_major_locator(MultipleLocator(xtick))
    if yticks is not None:
        ax.yaxis.set_major_locator(MultipleLocator(yticks))

    # 显示副刻度线
    if minorticks:
        ax.minorticks_on()

        # 获取 x 轴和 y 轴的主刻度线位置
        xticks = ax.get_xticks()
        yticks = ax.get_yticks()

        # 计算刻度线之间的差值
        xtick_interval = xticks[1] - xticks[0]
        ytick_interval = yticks[1] - yticks[0]

        # 设置副刻度线间隔
        if x_minor:
            ax.xaxis.set_minor_locator(MultipleLocator(xtick_interval * 0.5))
        else:
            ax.xaxis.set_minor_locator(MultipleLocator(xtick_interval))
        if y_minor:
            ax.yaxis.set_minor_locator(MultipleLocator(ytick_interval * 0.5))
        else:
            ax.yaxis.set_minor_locator(MultipleLocator(ytick_interval))
        # 修改有效小数位
        if format[0] is not None:
            ax.xaxis.set_major_formatter(mtick.FormatStrFormatter(format[0]))
        if format[1] is not None:
            ax.yaxis.set_major_formatter(mtick.FormatStrFormatter(format[1]))
    else:
        ax.minorticks_off()
    # 去除上轴刻度
    if not visible_ticks_top_right:
        # 去除上轴刻度
        visible_ticks = {
        "top": False,
        "right": False
        }
        ax.tick_params(axis="both", which="both",**visible_ticks)