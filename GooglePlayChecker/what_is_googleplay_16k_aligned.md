问：googleplay对上架app的so的16KB对齐要求，到底是指哪一部分的对齐要求

可以，而且这个工具只需要解析 `llvm-readelf -l` 的输出即可，不需要自己解析 ELF。

下面这个 Python 工具会：

* 调用 `llvm-readelf -l`
* 找出所有 `LOAD` Segment
* 检查最后一列 `Align`
* 判断是否 >= 0x4000
* 输出详细结果
* 返回 exit code（方便 CI 使用）

  * 0 = 通过
  * 1 = 不通过
  * 2 = 工具错误

---

## check_so_16k.py

```python
#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import argparse
import subprocess
import re
import sys
import os

REQUIRED_ALIGN = 0x4000


def parse_align(value: str):
    """
    将 readelf 输出中的 Align 字段转换为整数

    支持：
        0x4000
        16384
    """
    value = value.strip()

    if value.startswith("0x") or value.startswith("0X"):
        return int(value, 16)

    return int(value)


def check_so(readelf_path, so_path):
    cmd = [
        readelf_path,
        "-l",
        so_path
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
    except Exception as e:
        print("ERROR:", e)
        return False

    lines = result.stdout.splitlines()

    load_aligns = []

    i = 0
    while i < len(lines):

        line = lines[i].strip()

        if line.startswith("LOAD"):

            #
            # llvm-readelf 输出格式：
            #
            # LOAD           0x000000 ...
            #                0x123456 ...
            #                              R E    0x4000
            #

            if i + 1 >= len(lines):
                break

            second = lines[i + 1]

            m = re.search(r'0x[0-9A-Fa-f]+|\d+\s*$', second)

            if not m:
                print("Cannot parse Align:")
                print(second)
                return False

            align_text = m.group(0).strip()

            align = parse_align(align_text)

            load_aligns.append(align)

            i += 2
            continue

        i += 1

    if not load_aligns:
        print("No LOAD segment found.")
        return False

    print("=" * 60)
    print("File :", so_path)
    print("=" * 60)

    ok = True

    for idx, align in enumerate(load_aligns):

        passed = align >= REQUIRED_ALIGN

        print(
            "LOAD {:2d} : Align = 0x{:X} ({}) {}".format(
                idx,
                align,
                align,
                "PASS" if passed else "FAIL"
            )
        )

        if not passed:
            ok = False

    print()

    if ok:
        print("Result : PASS (Google Play 16KB ELF Alignment)")
    else:
        print("Result : FAIL")
        print("Reason : One or more LOAD segments have Align < 0x4000")

    return ok


def main():

    parser = argparse.ArgumentParser(
        description="Check ELF 16KB Alignment for Google Play"
    )

    parser.add_argument(
        "so",
        help="Path of .so"
    )

    parser.add_argument(
        "--readelf",
        default="llvm-readelf",
        help="Path to llvm-readelf"
    )

    args = parser.parse_args()

    if not os.path.exists(args.so):
        print("File not found:", args.so)
        sys.exit(2)

    ok = check_so(args.readelf, args.so)

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
```

---

## 使用方法

例如：

```bash
python check_so_16k.py libavpro.so
```

或者：

```bash
python check_so_16k.py libxxx.so --readelf D:\Android\NDK\toolchains\llvm\prebuilt\windows-x86_64\bin\llvm-readelf.exe
```

---

## 输出示例（通过）

```
============================================================
File : libxxx.so
============================================================

LOAD  0 : Align = 0x4000 (16384) PASS
LOAD  1 : Align = 0x4000 (16384) PASS
LOAD  2 : Align = 0x4000 (16384) PASS

Result : PASS (Google Play 16KB ELF Alignment)
```

---

## 输出示例（失败）

```
============================================================
File : libxxx.so
============================================================

LOAD  0 : Align = 0x1000 (4096) FAIL
LOAD  1 : Align = 0x4000 (16384) PASS
LOAD  2 : Align = 0x1000 (4096) FAIL

Result : FAIL
Reason : One or more LOAD segments have Align < 0x4000
```

---

## 我建议再升级一个版本

这个版本是基于**解析 `llvm-readelf -l` 文本输出**实现的，简单实用。

不过，**Google 官方实际上推荐使用 `llvm-readobj --elf-output-style=JSON`（较新的 LLVM 提供）或直接解析 ELF Program Header**，这样不会受不同 LLVM 版本输出格式变化的影响，也可以同时检查：

* 每个 `PT_LOAD` 的 `p_align`
* `p_offset % p_align == p_vaddr % p_align`
* `p_align >= 0x4000`
* 是否存在异常的 Program Header

这种实现会更加健壮，也更接近 Google Play 的实际检查逻辑。如果你需要一个长期用于自动化检测第三方 `.so` 的工具，我更推荐这种方案。


问：以下是一个输出信息：
Program Headers:
  Type           Offset   VirtAddr           PhysAddr           FileSiz  MemSiz   Flg Align
  PHDR           0x000040 0x0000000000000040 0x0000000000000040 0x0001f8 0x0001f8 R   0x8
  LOAD           0x000000 0x0000000000000000 0x0000000000000000 0x0a7120 0x0a7120 R E 0x4000
  LOAD           0x0a7120 0x00000000000ab120 0x00000000000ab120 0x003740 0x003740 RW  0x4000
  LOAD           0x0aa860 0x00000000000b2860 0x00000000000b2860 0x000a48 0x002270 RW  0x4000
  DYNAMIC        0x0a9b78 0x00000000000adb78 0x00000000000adb78 0x0001a0 0x0001a0 RW  0x8
  GNU_RELRO      0x0a7120 0x00000000000ab120 0x00000000000ab120 0x003740 0x004ee0 R   0x1
  GNU_EH_FRAME   0x018650 0x0000000000018650 0x0000000000018650 0x001134 0x001134 R   0x4
  GNU_STACK      0x000000 0x0000000000000000 0x0000000000000000 0x000000 0x000000 RW  0x0
  NOTE           0x000238 0x0000000000000238 0x0000000000000238 0x0000bc 0x0000bc R   0x4
使用llvm-readefl，或许到上面这些信息段，那么这个so合规吗


根据你提供的 `llvm-readelf -l` 输出，**这个 `.so` 从 ELF 的 16KB 对齐要求来看，是符合 Google Play 要求的。**

我们逐项分析。

| Type         |      Align | 是否检查  | 是否通过 |
| ------------ | ---------: | ----- | ---- |
| PHDR         |        0x8 | ❌ 不检查 | -    |
| LOAD         | **0x4000** | ✅ 检查  | ✅    |
| LOAD         | **0x4000** | ✅ 检查  | ✅    |
| LOAD         | **0x4000** | ✅ 检查  | ✅    |
| DYNAMIC      |        0x8 | ❌ 不检查 | -    |
| GNU_RELRO    |        0x1 | ❌ 不检查 | -    |
| GNU_EH_FRAME |        0x4 | ❌ 不检查 | -    |
| GNU_STACK    |        0x0 | ❌ 不检查 | -    |
| NOTE         |        0x4 | ❌ 不检查 | -    |

---

## 第一项：所有 LOAD Segment

Google Play 真正检查的是：

```
PT_LOAD
```

也就是

```
LOAD
```

你的共有三个：

```
LOAD  Align 0x4000
LOAD  Align 0x4000
LOAD  Align 0x4000
```

全部都是

```
0x4000
```

因此：

> **满足 Google Play 要求。**

---

## 第二项：Offset 是否正确

Google Play 实际还要求 ELF 能正确映射。

ELF Loader 要满足：

```
p_offset % p_align
==
p_vaddr % p_align
```

我们验证一下。

### 第一个 LOAD

```
Offset = 0x000000
Virt   = 0x000000
Align  = 0x4000
```

```
0 % 0x4000 = 0
0 % 0x4000 = 0
```

✔

---

### 第二个 LOAD

```
Offset = 0x0a7120
Virt   = 0x0ab120
Align  = 0x4000
```

计算余数：

```
0x0a7120 % 0x4000
```

```
0x3120
```

```
0x0ab120 % 0x4000
```

```
0x3120
```

一致。

✔

---

### 第三个 LOAD

```
Offset = 0x0aa860
Virt   = 0x0b2860
Align  = 0x4000
```

```
0x0aa860 % 0x4000
```

```
0x2860
```

```
0x0b2860 % 0x4000
```

```
0x2860
```

一致。

✔

---

所以 ELF 本身没有问题。

---

## 为什么 Offset 不是 0x4000 的倍数？

很多人第一次看都会疑惑：

```
Offset
0x0aa860
```

怎么看都不是

```
0x4000
```

的整数倍。

其实 ELF 从来没有要求：

```
Offset % Align == 0
```

真正要求的是：

```
Offset % Align
==
VirtAddr % Align
```

Linux Loader 就是根据这个关系 mmap 的。

所以这是完全合法的 ELF。

---

## 你的 Python 工具可以简化很多

实际上，如果你的工具只是为了检查 Google Play 是否接受，一个很简单的逻辑就够了：

```python
for each ProgramHeader:
    if Type == "LOAD":
        if Align < 0x4000:
            FAIL
```

再严谨一点，可以再检查：

```python
Offset % Align == VirtAddr % Align
```

如果不满足，也认为失败。

---

## 还有一个容易忽略的点

**Google Play 的检查并不仅限于 ELF。**

一个 APK 最终能否通过，还取决于另一个条件：

> **APK 中 `.so` 文件的 ZIP Entry 是否也进行了 16KB 对齐（ZIP alignment）。**

也就是说：

1. **ELF 对齐（你现在检查的）** ✅
2. **ZIP 对齐（APK 内部存储）** ✅

这两个都满足，Google Play 才会认为该原生库支持 16KB 页面。

对于你贴出来的这个 `.so`，**仅从 `llvm-readelf -l` 的结果来看，它已经符合 Google Play 的 ELF 16KB 对齐要求。** 如果这个 `.so` 最终打包进 APK 时也采用了 16KB ZIP 对齐（现代 Android Gradle Plugin 已会自动处理），那么它就是符合 Google Play 16KB 页面兼容要求的。
