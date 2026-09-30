"""extract_pdf_images.py — 导出 PDF 内嵌的全部图片（自动去重）
用法: python extract_pdf_images.py <input.pdf> [输出目录]
"""
import sys
import ctypes
from pathlib import Path


def _fix_console_encoding() -> None:
    """修复打包后的 exe 在中文 Windows 控制台输出乱码的问题。

    PyInstaller 的 exe 默认按 UTF-8 写字节，而 GBK 代码页的控制台会显示乱码。
    这里按控制台实际代码页重新配置输出编码：65001→UTF-8，其余→GBK。
    """
    try:
        import ctypes
        cp = ctypes.windll.kernel32.GetConsoleOutputCP()
    except Exception:
        return
    try:
        enc = "utf-8" if cp == 65001 else "gbk"
        sys.stdout.reconfigure(encoding=enc, errors="replace")
        sys.stderr.reconfigure(encoding=enc, errors="replace")
    except Exception:
        pass


_fix_console_encoding()


def print_help():
    print("""\
extract_pdf_images.py — 导出 PDF 内嵌的全部图片（自动去重）

用法:
  extract_pdf_images(.py|.exe) <input.pdf> [input2.pdf ...] [-o 输出目录]
  extract_pdf_images(.py|.exe) -i <input.pdf> [-i <input2.pdf> ...] [-o 输出目录]
  extract_pdf_images(.py|.exe) -help | -?

参数:
  <input.pdf>...   要处理的 PDF 文件，可多个（空格分隔）
  -i, --input      显式指定输入 PDF，可重复使用（与位置参数二选一或混用）
  -o, --output     输出目录（可选，默认 ./images）
  -help, -?        显示本帮助文档

示例:
  extract_pdf_images.py 报告.pdf
  extract_pdf_images.py 报告.pdf my_images          # 指定输出目录
  extract_pdf_images.py a.pdf b.pdf c.pdf           # 批量处理（拖拽多个文件到 exe 同理）
  extract_pdf_images.py -i a.pdf -i b.pdf -o out    # 显式选项写法
  extract_pdf_images.py -help

批量处理时:
  每个 PDF 会在输出目录下生成以自身文件名命名的子目录，避免图片重名。
  例如 -o out 处理 a.pdf 和 b.pdf → out/a/img_0001.png ... out/b/img_0001.png

输出:
  img_0001.png, img_0002.jpg ...   导出的图片（按导出顺序编号）
  _manifest.tsv                    清单：文件名 / xref / 首次页码 / 尺寸 / 格式 / 大小

说明:
  - 同一张图被多页共用时只导出一次（按 xref 去重）
  - 带透明通道(软蒙版)的图片会合成为透明 PNG
  - 只提取位图对象；矢量图形（如 AI 画的 logo）不是图片，无法导出
  - 扫描版 PDF 整页是单张大图，导出的就是页面原图

路径含空格怎么办:
  文件/目录名带空格时，必须用半角双引号 " 把整个路径括起来，
  否则空格会被当作参数分隔符导致路径被截断。例如:
    python extract_pdf_images.py "我的 报告.pdf" "我的 输出"
    python extract_pdf_images.py "D:\\我的文件\\2026 报告.pdf"
  也可以在资源管理器中把 PDF 直接拖拽到本脚本上运行，
  系统会自动用引号包裹路径，无需手工输入。

打包成可执行文件(exe)后:
  1. 打包命令（需先 pip install pyinstaller）:
       pyinstaller -F -n extract_pdf_images extract_pdf_images.py
     生成 dist/extract_pdf_images.exe，可拷贝到任意电脑运行
  2. 用法与 .py 完全一致，把 python extract_pdf_images.py 换成 extract_pdf_images.exe 即可
  3. 拖拽 1 个 PDF 到 exe 图标 → 直接导出；拖拽多个 → 批量导出（各占一个子目录）
  4. 无参数双击 exe → 显示本帮助，按回车键退出（窗口不会一闪而过）
  5. 中文控制台输出已做代码页自适应，不会乱码
""")


def extract_images(pdf_path: str, out_dir: str = "images") -> list[dict]:
    import pymupdf  # 延迟导入，保证 -help 在未安装依赖时也可用

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    records = []          # 每张导出图片的记录
    seen_xref = set()     # 已导出的 xref，用于去重
    counter = 0

    with pymupdf.open(pdf_path) as doc:
        for page_no, page in enumerate(doc, start=1):
            for img in page.get_images(full=True):
                xref = img[0]
                if xref in seen_xref:      # 多页共用的图只导出一次
                    continue
                seen_xref.add(xref)

                info = doc.extract_image(xref)
                ext = info["ext"]
                data = info["image"]

                # 有软蒙版(smask)时合成透明 PNG，避免导出成黑底/无背景
                smask = info.get("smask")
                if smask:
                    from io import BytesIO
                    from PIL import Image
                    base = Image.open(BytesIO(data)).convert("RGBA")
                    mask = Image.open(BytesIO(alpha := doc.extract_image(smask)["image"])).convert("L")
                    base.putalpha(mask)
                    buf = BytesIO()
                    base.save(buf, format="PNG")
                    data, ext = buf.getvalue(), "png"

                counter += 1
                fname = f"img_{counter:04d}.{ext}"
                (out / fname).write_bytes(data)
                records.append({
                    "file": fname,
                    "xref": xref,
                    "first_page": page_no,
                    "width": info["width"],
                    "height": info["height"],
                    "format": info["ext"],
                    "bytes": len(data),
                })

    # 无图片时给出友好提示，而不是崩溃
    if not records:
        print(f"  [{Path(pdf_path).name}] 未发现可导出的图片（可能全是矢量图形或纯文本页面）")
        return records

    # 导出清单，方便核对
    (out / "_manifest.tsv").write_text(
        "\t".join(records[0].keys()) + "\n" +
        "\n".join("\t".join(str(r[k]) for k in records[0]) for r in records),
        encoding="utf-8",
    )
    return records


def _friendly_path_error(pdf: str) -> None:
    """找不到文件时的友好提示，重点解释空格截断问题。"""
    print(f"[错误] 找不到文件: {pdf}")
    if " " in pdf:
        print("提示: 路径包含空格，请用半角双引号把整个路径括起来，例如:")
        print('  python extract_pdf_images.py "我的 报告.pdf"')
    else:
        print("提示: 请检查路径是否正确；路径含空格时需用双引号括起来。")
    print("可运行 python extract_pdf_images.py -help 查看完整帮助。")


def _print_help_and_exit(code: int = 0) -> None:
    """打印帮助并退出；exe 双击场景下等待按键，防止窗口一闪而过。

    仅当 stdin 是交互式控制台(如双击 exe)时才等待回车；
    管道/重定向/自动化调用时直接退出，避免阻塞。
    """
    print_help()
    if getattr(sys, "frozen", False) and sys.stdin.isatty():
        try:
            input("按回车键退出...")
        except EOFError:
            pass
    sys.exit(code)


def parse_args(argv: list[str]) -> tuple[list[str], str]:
    """解析命令行参数，返回 (输入PDF列表, 输出目录)。

    规则:
      - -help / -? / --help / -h: 打印帮助后退出
      - -i, --input <path>    : 显式输入 PDF，可重复
      - -o, --output <path>   : 输出目录
      - 位置参数: 以 .pdf 结尾(不区分大小写) → 输入; 否则 → 输出目录
      - 位置参数被空格拆开时（如「我的 报告.pdf」→ 两个参数），自动拼接检测
    """
    inputs: list[str] = []
    output: str | None = None
    i = 1
    while i < len(argv):
        a = argv[i]
        if a in ("-help", "-?", "--help", "-h"):
            _print_help_and_exit(0)
        elif a in ("-i", "--input"):
            if i + 1 >= len(argv):
                print(f"[错误] 选项 {a} 缺少参数值"); sys.exit(1)
            inputs.append(argv[i + 1]); i += 2
        elif a in ("-o", "--output"):
            if i + 1 >= len(argv):
                print(f"[错误] 选项 {a} 缺少参数值"); sys.exit(1)
            output = argv[i + 1]; i += 2
        elif a.startswith("-") and len(a) > 1:
            print(f"[错误] 未知选项: {a}")
            print("运行 extract_pdf_images -help 查看用法。")
            sys.exit(1)
        else:
            # 空格截断兜底：如「我的 报告.pdf」被拆成两个位置参数，尝试合并
            if (not a.lower().endswith(".pdf") and i + 1 < len(argv)
                    and argv[i + 1].lower().endswith(".pdf")):
                rejoined = a + " " + argv[i + 1]
                if Path(rejoined).is_file():
                    inputs.append(rejoined)
                    i += 2
                    continue
            if a.lower().endswith(".pdf"):
                inputs.append(a)
            else:
                if output is not None:
                    print(f"[错误] 无法确定参数 '{a}' 的含义：已有输出目录 '{output}'，且 '{a}' 不是 PDF 文件。")
                    sys.exit(1)
                output = a
            i += 1

    if not inputs:          # 无输入 → 帮助
        _print_help_and_exit(1)
    return inputs, output or "images"


def main() -> None:
    try:
        cp = ctypes.windll.kernel32.GetConsoleOutputCP()  # 查询控制台实际代码页
        enc = "utf-8" #f"cp{cp}" if cp else "utf-8"                # 如 936 → cp936(GBK)；65001 → cp65001(UTF-8)
        print(enc)
        sys.stdout.reconfigure(encoding=enc, errors="replace")
        sys.stderr.reconfigure(encoding=enc, errors="replace")
    except Exception as e:
        print(f"[警告] 设置控制台编码失败: {e}")
        return

    inputs, output = parse_args(sys.argv)

    # 输入检查：所有 PDF 必须真实存在
    for pdf in inputs:
        if not Path(pdf).is_file():
            _friendly_path_error(pdf)
            sys.exit(1)

    if len(inputs) == 1:
        recs = extract_images(inputs[0], output)
        print(f"[{Path(inputs[0]).name}] 共导出 {len(recs)} 张图片 → {output}")
        for r in recs:
            print(f"  {r['file']}  尺寸 {r['width']}x{r['height']}  xref={r['xref']}  首次出现于第 {r['first_page']} 页")
    else:
        print(f"批量处理 {len(inputs)} 个 PDF → 输出根目录: {output}")
        total = 0
        for pdf in inputs:
            outdir = str(Path(output) / Path(pdf).stem)
            recs = extract_images(pdf, outdir)
            total += len(recs)
            print(f"  [{Path(pdf).name}] {len(recs)} 张 → {outdir}")
        print(f"完成，共导出 {total} 张图片")

if __name__ == "__main__":
    backupCodePage = ctypes.windll.kernel32.GetConsoleOutputCP()  # 查询控制台实际代码页
    print("BOPExtractor is Bitmaps of PDF Extractor")
    main()
    enc = f"cp{backupCodePage}"
    sys.stdout.reconfigure(encoding=enc, errors="replace")