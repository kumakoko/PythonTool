"""
SO 文件对齐检查模块

用于检查 Android .so 文件是否符合 Google Play 的 16KB 对齐要求。
检查原理：
1. 调用 readelf -l 命令获取 ELF 文件的 Program Headers
2. 提取所有 LOAD Segment 的 Offset、VirtAddr 和 Align 值
3. 判断每个 LOAD Segment 是否满足以下两个条件：
   - Align >= 0x4000 (16384)
   - Offset % Align == VirtAddr % Align
"""

import subprocess
import re

# Google Play 要求的最小对齐值 (16KB = 16384 = 0x4000)
REQUIRED_ALIGN = 0x4000


def parse_hex(value):
    """
    解析十六进制字符串
    
    支持格式：0x4000 或 0X4000
    
    Args:
        value: 十六进制字符串
        
    Returns:
        int: 解析后的整数值
    """
    value = value.strip()
    if value.startswith("0x") or value.startswith("0X"):
        return int(value, 16)
    return int(value)


def parse_align(value):
    """
    解析对齐值字符串
    
    支持两种格式：十六进制(0x4000)和十进制(16384)。
    
    Args:
        value: 对齐值字符串
        
    Returns:
        int: 对齐值的整数表示
    """
    value = value.strip()
    
    # 处理十六进制格式 (如 0x4000)
    if value.startswith("0x") or value.startswith("0X"):
        return int(value, 16)
    
    # 处理十进制格式 (如 16384)
    return int(value)


def check_so_align(readelf_path, so_path):
    """
    检查单个 .so 文件的 16KB 对齐情况
    
    调用 readelf -l 命令解析 ELF 文件的 LOAD Segment，
    检查每个 LOAD Segment 是否满足 Google Play 的两个要求：
    1. Align >= 0x4000
    2. Offset % Align == VirtAddr % Align
    
    使用 subprocess.run() 执行命令，该函数会自动等待进程完成并回收资源，
    确保 readelf 进程正确关闭，不会造成资源泄漏。
    
    Args:
        readelf_path: readelf 程序的绝对路径
        so_path: 要检查的 .so 文件的绝对路径
        
    Returns:
        tuple: (检查结果, 结果信息列表)
            检查结果: True 表示通过，False 表示未通过或出错
            结果信息列表: 包含详细的检查过程和结果信息
    """
    # 构建 readelf 命令
    cmd = [readelf_path, "-l", so_path]
    # 存储检查结果信息
    results = []

    try:
        # 执行 readelf 命令，捕获输出
        # subprocess.run() 会自动等待进程完成，并关闭所有文件描述符
        # check=True 表示如果命令返回非零退出码，会抛出 CalledProcessError 异常
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            # 设置超时时间，防止 readelf 进程挂起
            timeout=60
        )
        
        # 进程已正常结束，资源已自动回收
        
    except subprocess.TimeoutExpired:
        # 命令执行超时
        results.append(f"ERROR: readelf 执行超时，文件: {so_path}")
        return False, results
    except subprocess.CalledProcessError as e:
        # 命令执行失败（非零退出码）
        results.append(f"ERROR: readelf 执行失败，退出码: {e.returncode}")
        results.append(f"标准错误: {e.stderr}")
        return False, results
    except FileNotFoundError:
        # readelf 程序未找到
        results.append(f"ERROR: 未找到 readelf 程序: {readelf_path}")
        return False, results
    except Exception as e:
        # 其他未知错误
        results.append(f"ERROR: {e}")
        return False, results

    # 将输出按行分割
    lines = result.stdout.splitlines()
    # 存储所有 LOAD Segment 的信息 (offset, virt_addr, align)
    load_segments = []

    # 逐行解析输出
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # 找到 LOAD Segment 开始行
        if line.startswith("LOAD"):
            # LOAD Segment 的格式：
            # 第一行: LOAD  Offset  VirtAddr  PhysAddr  FileSiz  MemSiz  Flg  Align
            # 或者 llvm-readelf 格式：
            # LOAD           0x000000 ...
            #                0x123456 ...
            #                              R E    0x4000
            
            # 获取第一行内容，提取 Offset 和 VirtAddr
            first_line_parts = line.split()
            
            if len(first_line_parts) < 3:
                results.append("Cannot parse LOAD segment:")
                results.append(line)
                return False, results
            
            # 提取 Offset (第二个字段)
            try:
                offset = parse_hex(first_line_parts[1])
            except ValueError:
                results.append(f"Cannot parse Offset: {first_line_parts[1]}")
                return False, results
            
            # 提取 VirtAddr (第三个字段)
            try:
                virt_addr = parse_hex(first_line_parts[2])
            except ValueError:
                results.append(f"Cannot parse VirtAddr: {first_line_parts[2]}")
                return False, results
            
            # 获取 Align 值
            align = None
            
            # 尝试从第一行末尾提取 Align（标准 readelf 格式）
            if len(first_line_parts) >= 8:
                try:
                    align = parse_align(first_line_parts[-1])
                except ValueError:
                    align = None
            
            # 如果第一行没有 Align，尝试从第二行提取（llvm-readelf 格式）
            if align is None and i + 1 < len(lines):
                second_line = lines[i + 1]
                m = re.search(r'0x[0-9A-Fa-f]+|\d+\s*$', second_line)
                if m:
                    try:
                        align = parse_align(m.group(0).strip())
                    except ValueError:
                        align = None
            
            if align is None:
                results.append("Cannot parse Align:")
                results.append(line)
                if i + 1 < len(lines):
                    results.append(lines[i + 1])
                return False, results
            
            # 添加到 LOAD Segment 列表
            load_segments.append({
                'offset': offset,
                'virt_addr': virt_addr,
                'align': align
            })
            
            # 跳过已处理的行
            if i + 1 < len(lines) and not lines[i + 1].strip().startswith("LOAD"):
                i += 2
            else:
                i += 1
            continue
        
        # 处理下一行
        i += 1

    # 检查是否找到 LOAD Segment
    if not load_segments:
        results.append("No LOAD segment found.")
        return False, results

    # 输出检查结果详情
    results.append("=" * 60)
    results.append(f"File : {so_path}")
    results.append("=" * 60)

    # 判断所有 LOAD Segment 是否都满足对齐要求
    ok = True
    for idx, seg in enumerate(load_segments):
        offset = seg['offset']
        virt_addr = seg['virt_addr']
        align = seg['align']
        
        # 检查条件1: Align >= 0x4000
        align_ok = align >= REQUIRED_ALIGN
        
        # 检查条件2: Offset % Align == VirtAddr % Align
        if align == 0:
            # 避免除以零
            offset_ok = False
        else:
            offset_ok = (offset % align) == (virt_addr % align)
        
        # 综合判断该 Segment 是否通过
        passed = align_ok and offset_ok
        status = "PASS" if passed else "FAIL"
        
        # 输出每个 LOAD Segment 的检查结果
        results.append(f"LOAD {idx:2d} :")
        results.append(f"      Offset = 0x{offset:X}")
        results.append(f"      Virt   = 0x{virt_addr:X}")
        results.append(f"      Align  = 0x{align:X} ({align})")
        
        # 输出条件1检查结果
        if align_ok:
            results.append(f"      [条件1] Align >= 0x4000 : PASS")
        else:
            results.append(f"      [条件1] Align >= 0x4000 : FAIL (要求 >= 0x4000)")
        
        # 输出条件2检查结果
        if align == 0:
            results.append(f"      [条件2] Offset % Align == VirtAddr % Align : FAIL (Align 为 0)")
        else:
            offset_mod = offset % align
            virt_mod = virt_addr % align
            if offset_ok:
                results.append(f"      [条件2] 0x{offset:X} % 0x{align:X} == 0x{virt_addr:X} % 0x{align:X} : PASS")
                results.append(f"              ({offset_mod} == {virt_mod})")
            else:
                results.append(f"      [条件2] 0x{offset:X} % 0x{align:X} == 0x{virt_addr:X} % 0x{align:X} : FAIL")
                results.append(f"              ({offset_mod} != {virt_mod})")
        
        results.append(f"      状态 : {status}")
        results.append("")
        
        # 如果有任何一个不满足要求，整体结果为失败
        if not passed:
            ok = False

    # 输出最终结果
    results.append("=" * 60)
    if ok:
        results.append("Result : PASS (Google Play 16KB ELF Alignment)")
    else:
        results.append("Result : FAIL")
        # 分析失败原因
        fail_reasons = []
        for seg in load_segments:
            if seg['align'] < REQUIRED_ALIGN:
                fail_reasons.append(f"Align < 0x4000")
                break
        for seg in load_segments:
            if seg['align'] != 0 and (seg['offset'] % seg['align']) != (seg['virt_addr'] % seg['align']):
                fail_reasons.append(f"Offset % Align != VirtAddr % Align")
                break
        results.append("Reason : " + ", ".join(fail_reasons))

    return ok, results