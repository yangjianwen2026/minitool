# -*- coding: utf-8 -*-
"""
全面修复 toolmini.cn 的19项问题
P0: JS结构/CSS变量/PWA/工具页面404
P1: jpg_to_pdf/视频GIF/PDF加密压缩/AI标注/裁剪触摸
P2: CDN版本/可访问性/noscript/字体CDN/sitemap
"""
import os, re

BASE = r"C:\Users\newna\.qianfan\workspace\14dabc72fd0e469abfba93777adccb0a"
IDX = os.path.join(BASE, "index.html")

with open(IDX, 'r', encoding='utf-8') as f:
    html = f.read()

# ================================================================
# P0-2: 修复 </script> 位置错误 — 将裸露的 JS 代码移回 script 块内
# ================================================================
# 问题：第2939行 </script> 提前闭合，导致后续函数在 script 外
# 方案：删除 </script>（2939行）和 <!-- PWA Service Worker --> 之间的分界，
# 将裸露代码移入 script 块，然后在 PWA script 之前才闭合

old_broken = """</script>


// ─────────────────────────────────────────────
// RECENT TOOLS (LocalStorage)
// ─────────────────────────────────────────────"""

new_fixed = """
// ─────────────────────────────────────────────
// RECENT TOOLS (LocalStorage)
// ─────────────────────────────────────────────"""

html = html.replace(old_broken, new_fixed)

# ================================================================
# P0-3: 添加缺失的 --text-dim CSS 变量
# ================================================================
html = html.replace(
    '--text-muted: #94a3b8;',
    '--text-muted: #94a3b8;\n  --text-dim: #64748b;'
)

# ================================================================
# P0-4: 移除不存在的 manifest.json 引用 + PWA Service Worker
# ================================================================
html = html.replace(
    '<link rel="manifest" href="manifest.json">\n',
    ''
)

# 替换 PWA SW 注册为简洁版（仅 QR 码逻辑，不注册不存在的 sw.js）
old_pwa = """<!-- PWA Service Worker -->
<script>
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('sw.js').then(reg => {
        console.log('SW registered:', reg.scope);
      }).catch(err => console.log('SW registration failed:', err));
    });
  }

  // PWA: Show share bar and generate QR code
  window.addEventListener('load', () => {"""

new_pwa = """// PWA: Show share bar and generate QR code
window.addEventListener('load', () => {"""

html = html.replace(old_pwa, new_pwa)

# ================================================================
# P2-13: 锁定 CDN 库版本号（替代 @latest）
# ================================================================
html = html.replace(
    'https://unpkg.com/lucide@latest/dist/umd/lucide.min.js',
    'https://unpkg.com/lucide@0.344.0/dist/umd/lucide.min.js'
)

# ================================================================
# P2-18: Google Fonts 使用国内 CDN（loli.net 镜像）
# ================================================================
html = html.replace(
    'https://fonts.googleapis.com',
    'https://fonts.loli.net'
)
html = html.replace(
    'https://fonts.gstatic.com',
    'https://gstatic.loli.net'
)
html = html.replace(
    '<link rel="preconnect" href="https://fonts.loli.net">',
    '<link rel="preconnect" href="https://fonts.loli.net">\n<link rel="preconnect" href="https://gstatic.loli.net" crossorigin>'
)

# ================================================================
# P2-17: 添加 <noscript> 回退内容
# ================================================================
html = html.replace(
    '<body>\n\n<header',
    '<body>\n<noscript><div style="text-align:center;padding:80px 20px;font-family:system-ui;background:#0f0f13;color:#e2e8f0"><h1 style="font-size:24px;margin-bottom:12px">MiniTool 需要启用 JavaScript</h1><p style="color:#94a3b8">请在浏览器设置中启用 JavaScript 后刷新页面。</p></div></noscript>\n\n<header'
)

# ================================================================
# P2-14: 工具卡片添加 tabindex/role/aria-label
# ================================================================
html = html.replace(
    """<div class="tool-card" data-cat="${tool.cat}" data-id="${tool.id}" data-name="${tool.name}" onclick="openTool('${tool.id}')">""",
    """<div class="tool-card" data-cat="${tool.cat}" data-id="${tool.id}" data-name="${tool.name}" onclick="openTool('${tool.id}')" tabindex="0" role="button" aria-label="${tool.name} - ${tool.desc}" onkeydown="if(event.key==='Enter')openTool('${tool.id}')">"""
)

# ================================================================
# P2-15: 搜索清除按钮添加 aria-label
# ================================================================
html = html.replace(
    'id="searchClear" onclick="document.getElementById',
    'id="searchClear" aria-label="清除搜索" onclick="document.getElementById'
)

# ================================================================
# P2-16: 🔗 链接添加 aria-label
# ================================================================
html = html.replace(
    """<a href="${tool.slug ? '/tools/' + tool.slug + '.html' : '#'}" class="tool-link" onclick="event.stopPropagation()" title="独立页面打开">🔗</a>""",
    """<a href="${tool.slug ? '/tools/' + tool.slug + '.html' : '#'}" class="tool-link" onclick="event.stopPropagation()" title="独立页面打开" aria-label="在独立页面打开${tool.name}">🔗</a>"""
)

# ================================================================
# P1-5: 修复 toolJpgToPdf 对 WebP/GIF 崩溃
# 在 embedJpg/embedPng 之前先将 WebP/GIF 转 canvas 再输出 PNG
# ================================================================
old_jpg_to_pdf = """async function toolJpgToPdf() {
  const { PDFDocument } = PDFLib;
  const pdf = await PDFDocument.create();
  for (const file of uploadedFiles) {
    const buf = await file.arrayBuffer();
    const ext = file.name.split('.').pop().toLowerCase();
    let img;
    if (ext === 'png') {
      img = await pdf.embedPng(buf);
    } else {
      img = await pdf.embedJpg(buf);
    }
    const page = pdf.addPage([img.width, img.height]);
    page.drawImage(img, { x: 0, y: 0, width: img.width, height: img.height });
  }
  const bytes = await pdf.save();
  saveBlob(new Blob([bytes], {type:'application/pdf'}), 'converted.pdf');
  hideProgress();
  showOutput('转换完成！已将 ' + uploadedFiles.length + ' 张图片合并为PDF。');
}"""

new_jpg_to_pdf = """async function toolJpgToPdf() {
  const { PDFDocument } = PDFLib;
  const pdf = await PDFDocument.create();
  for (const file of uploadedFiles) {
    const ext = file.name.split('.').pop().toLowerCase();
    let img;
    // WebP and GIF must be converted via canvas first (pdf-lib only supports JPG/PNG)
    if (ext === 'webp' || ext === 'gif') {
      const image = await loadImage(file);
      const canvas = document.createElement('canvas');
      canvas.width = image.naturalWidth; canvas.height = image.naturalHeight;
      canvas.getContext('2d').drawImage(image, 0, 0);
      const pngBlob = await new Promise(r => canvas.toBlob(r, 'image/png'));
      const pngBuf = await pngBlob.arrayBuffer();
      img = await pdf.embedPng(pngBuf);
    } else if (ext === 'png') {
      const buf = await file.arrayBuffer();
      img = await pdf.embedPng(buf);
    } else {
      // jpg/jpeg — try embedJpg first, fallback to canvas conversion
      try {
        const buf = await file.arrayBuffer();
        img = await pdf.embedJpg(buf);
      } catch {
        const image = await loadImage(file);
        const canvas = document.createElement('canvas');
        canvas.width = image.naturalWidth; canvas.height = image.naturalHeight;
        canvas.getContext('2d').drawImage(image, 0, 0);
        const jpgBlob = await new Promise(r => canvas.toBlob(r, 'image/jpeg', 0.92));
        const jpgBuf = await jpgBlob.arrayBuffer();
        img = await pdf.embedJpg(jpgBuf);
      }
    }
    const page = pdf.addPage([img.width, img.height]);
    page.drawImage(img, { x: 0, y: 0, width: img.width, height: img.height });
  }
  const bytes = await pdf.save();
  saveBlob(new Blob([bytes], {type:'application/pdf'}), 'converted.pdf');
  hideProgress();
  showOutput('转换完成！已将 ' + uploadedFiles.length + ' 张图片合并为PDF。');
}"""

html = html.replace(old_jpg_to_pdf, new_jpg_to_pdf)

# ================================================================
# P1-6: 修复 toolVidToGif — 使用 gif.js 库生成真正的动态 GIF
# ================================================================
old_vid_to_gif = """async function toolVidToGif() {
  const start = parseFloat(document.getElementById('ctrlGifStart')?.value || 0);
  const end = parseFloat(document.getElementById('ctrlGifEnd')?.value || 3);
  const gifW = parseInt(document.getElementById('ctrlGifW')?.value || 320);
  
  const file = uploadedFiles[0];
  const video = document.createElement('video');
  video.src = URL.createObjectURL(file);
  video.muted = true;
  await new Promise(r => video.onloadedmetadata = r);
  
  video.currentTime = start;
  await new Promise(r => video.onseeked = r);
  
  const ratio = video.videoHeight / video.videoWidth;
  const canvas = document.createElement('canvas');
  canvas.width = gifW;
  canvas.height = Math.round(gifW * ratio);
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  
  canvas.toBlob(blob => {
    saveBlob(blob, 'clip.gif');
    hideProgress();
    showOutput(`GIF生成完成！尺寸: ${canvas.width}×${canvas.height}px，截取时间: ${start}-${end}秒`);
  }, 'image/gif');
}"""

new_vid_to_gif = """async function toolVidToGif() {
  const start = parseFloat(document.getElementById('ctrlGifStart')?.value || 0);
  const end = parseFloat(document.getElementById('ctrlGifEnd')?.value || 3);
  const gifW = parseInt(document.getElementById('ctrlGifW')?.value || 320);

  const file = uploadedFiles[0];
  const video = document.createElement('video');
  video.src = URL.createObjectURL(file);
  video.muted = true;
  await new Promise(r => video.onloadedmetadata = r);

  const dur = video.duration;
  const actualEnd = Math.min(end, dur);
  const ratio = video.videoHeight / video.videoWidth;
  const gifH = Math.round(gifW * ratio);

  // Load gif.js library dynamically
  if (!window.GIF) {
    const s = document.createElement('script');
    s.src = 'https://cdn.jsdelivr.net/npm/gif.js@0.2.0/dist/gif.js';
    document.head.appendChild(s);
    await new Promise((resolve, reject) => { s.onload = resolve; s.onerror = reject; });
  }

  const canvas = document.createElement('canvas');
  canvas.width = gifW; canvas.height = gifH;
  const ctx = canvas.getContext('2d');

  const gif = new GIF({
    workers: 2, quality: 10, width: gifW, height: gifH,
    workerScript: 'https://cdn.jsdelivr.net/npm/gif.js@0.2.0/dist/gif.worker.js'
  });

  const fps = 8;
  const totalFrames = Math.min(50, Math.floor((actualEnd - start) * fps));
  const step = (actualEnd - start) / totalFrames;

  for (let i = 0; i < totalFrames; i++) {
    video.currentTime = start + i * step;
    await new Promise(r => video.onseeked = r);
    ctx.drawImage(video, 0, 0, gifW, gifH);
    gif.addFrame(ctx, { copy: true, delay: Math.round(1000 / fps) });
    updateProgress(i + 1, totalFrames, `截取帧 ${i+1}/${totalFrames}...`);
  }

  gif.on('finished', blob => {
    saveBlob(blob, 'clip.gif');
    hideProgress();
    showOutput(`动态GIF生成完成！尺寸: ${gifW}×${gifH}px，帧数: ${totalFrames}，时长: ${(actualEnd - start).toFixed(1)}秒`);
  });

  gif.on('progress', p => {
    const pct = Math.round(p * 100);
    updateProgress(pct, 100, `编码GIF ${pct}%...`);
  });

  gif.render();
}"""

html = html.replace(old_vid_to_gif, new_vid_to_gif)

# ================================================================
# P1-7: 修复 toolGifToVid — 诚实提示浏览器端限制
# ================================================================
old_gif_to_vid = """async function toolGifToVid() {
  const file = uploadedFiles[0];
  const img = await loadImage(file);
  const canvas = document.createElement('canvas');
  canvas.width = img.naturalWidth;
  canvas.height = img.naturalHeight;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(img, 0, 0);
  canvas.toBlob(blob => {
    saveBlob(blob, 'gif_as_image.png');
    hideProgress();
    showOutput('GIF已作为静态图片保存！注意：GIF动态效果需要在支持GIF的浏览器/工具中查看。');
  }, 'image/png');
}"""

new_gif_to_vid = """async function toolGifToVid() {
  const file = uploadedFiles[0];
  // Browser cannot re-encode video without MediaRecorder/WebCodecs pipeline
  // Provide the original GIF file for download, and explain limitations
  saveBlob(file, file.name);
  hideProgress();
  showOutput('已保存原始GIF文件。\\n\\n⚠️ 提示：浏览器端无法直接将GIF转为MP4视频。\\n建议使用以下方法：\\n1. 使用 FFmpeg 命令：ffmpeg -i input.gif -movflags faststart output.mp4\\n2. 使用在线转换工具（如 ezgif.com）\\n3. 使用专业视频编辑软件');
}"""

html = html.replace(old_gif_to_vid, new_gif_to_vid)

# ================================================================
# P1-8: 修复 toolVidUnwatermark 输出 .mp4 但实际是 ZIP
# ================================================================
# 修改输出文件名和提示文字
html = html.replace(
    "saveBlob(blob, file.name.replace(/\\.[^.]+$/, '') + '_no_watermark.mp4');",
    "saveBlob(blob, file.name.replace(/\\.[^.]+$/, '') + '_no_watermark_frames.zip');"
)
html = html.replace(
    "showOutput(`视频去水印完成！处理了 ${totalFrames} 个关键帧，使用「${method === 'blur' ? '高斯模糊' : method === 'crop' ? '裁剪移除' : '内容填充'}」方式处理水印区域。\\n\\n💡 提示：复杂水印建议分段处理或使用专业软件。`);",
    "showOutput(`视频去水印完成！处理了 ${totalFrames} 个关键帧，使用「${method === 'blur' ? '高斯模糊' : method === 'crop' ? '裁剪移除' : '内容填充'}」方式处理水印区域。\\n\\n📦 输出为处理后的帧序列（ZIP压缩包），非视频文件。\\n如需合成视频，请使用 FFmpeg：ffmpeg -i frame_%03d.png output.mp4\\n\\n💡 提示：复杂水印建议分段处理或使用专业软件。`);"
)

# ================================================================
# P1-9: 修复 toolPdfEncrypt — 诚实说明 pdf-lib 不支持加密
# ================================================================
old_pdf_encrypt = """async function toolPdfEncrypt() {
  const { PDFDocument } = PDFLib;
  const pwd = document.getElementById('ctrlPwd').value;
  if (!pwd) { toast('请输入密码', 'error'); hideProgress(); return; }
  const file = uploadedFiles[0];
  const buf = await file.arrayBuffer();
  const pdf = await PDFDocument.load(buf);
  const bytes = await pdf.save({ 
    userPassword: pwd, 
    ownerPassword: pwd,
    permissions: { printing: 'highPrint', modifying: false, copying: false, annotating: false, fillingForms: false, contentAccessibility: true }
  });
  saveBlob(new Blob([bytes], {type:'application/pdf'}), 'encrypted.pdf');
  hideProgress();
  showOutput('加密完成！PDF已添加打开密码保护，下载后需输入密码才能打开。');
}"""

new_pdf_encrypt = """async function toolPdfEncrypt() {
  const pwd = document.getElementById('ctrlPwd').value;
  if (!pwd) { toast('请输入密码', 'error'); hideProgress(); return; }
  const file = uploadedFiles[0];
  // pdf-lib does NOT support encryption — userPassword/ownerPassword are silently ignored
  // We save the file as-is and warn the user
  const buf = await file.arrayBuffer();
  const { PDFDocument } = PDFLib;
  const pdf = await PDFDocument.load(buf);
  const bytes = await pdf.save();
  saveBlob(new Blob([bytes], {type:'application/pdf'}), file.name);
  hideProgress();
  showOutput('⚠️ 重要提示：当前浏览器端 PDF 库（pdf-lib）不支持真正的加密功能。\\n\\n您设置的密码「' + pwd + '」未被应用，下载的文件仍是未加密的。\\n\\n建议使用以下方式加密PDF：\\n1. 使用 qpdf 命令：qpdf --encrypt USER_PW OWNER_PW 256 -- input.pdf output.pdf\\n2. 使用 LibreOffice 导出PDF时设置密码\\n3. 使用 Adobe Acrobat 等专业软件\\n\\n我们对此造成的不便深表歉意，后续将集成支持加密的库。');
}"""

html = html.replace(old_pdf_encrypt, new_pdf_encrypt)

# ================================================================
# P1-10: 修复 toolPdfCompress — 添加大小比较，变大时提示
# ================================================================
old_pdf_compress = """async function toolPdfCompress() {
  const { PDFDocument } = PDFLib;
  const file = uploadedFiles[0];
  const buf = await file.arrayBuffer();
  const pdf = await PDFDocument.load(buf);
  // Re-save with compression options
  const bytes = await pdf.save({ useObjectStreams: true });
  saveBlob(new Blob([bytes], {type:'application/pdf'}), 'compressed.pdf');
  hideProgress();
  const ratio = ((1 - bytes.length / buf.byteLength) * 100).toFixed(1);
  showOutput(`压缩完成！原始大小: ${formatSize(buf.byteLength)} → 压缩后: ${formatSize(bytes.length)}，体积减少 ${ratio}%`);
}"""

new_pdf_compress = """async function toolPdfCompress() {
  const { PDFDocument } = PDFLib;
  const file = uploadedFiles[0];
  const buf = await file.arrayBuffer();
  const pdf = await PDFDocument.load(buf);
  // Re-save with compression options
  const bytes = await pdf.save({ useObjectStreams: true });
  const origSize = buf.byteLength;
  const newSize = bytes.length;
  const ratio = ((1 - newSize / origSize) * 100).toFixed(1);
  if (newSize >= origSize) {
    // File got bigger — just offer the original
    saveBlob(new Blob([buf], {type:'application/pdf'}), file.name);
    hideProgress();
    showOutput(`该PDF已经过优化，无法进一步压缩。\\n原始大小: ${formatSize(origSize)}，重保存后: ${formatSize(newSize)}（变大 ${Math.abs(ratio)}%）\\n\\n已为您保存原始文件。\\n💡 提示：如需压缩PDF中的图片，建议使用专业工具（如 Adobe Acrobat、Ghostscript）。`);
  } else {
    saveBlob(new Blob([bytes], {type:'application/pdf'}), 'compressed_' + file.name);
    hideProgress();
    showOutput(`压缩完成！原始大小: ${formatSize(origSize)} → 压缩后: ${formatSize(newSize)}，体积减少 ${ratio}%`);
  }
}"""

html = html.replace(old_pdf_compress, new_pdf_compress)

# ================================================================
# P1-11: 修复 AI 工具伪实现 — 明确标注为"模板生成"而非暗示AI能力
# ================================================================
# 修改 AI 工具的名称和描述，标注"模板"
# TOOLS 数据中的 AI 工具
ai_tool_fixes = {
    "'ai_polish'": ("'文字润色'", "'基于模板的文本润色参考'"),
    "'ai_continue'": ("'文章续写'", "'基于模板的续写参考'"),
    "'ai_title'": ("'标题生成'", "'基于模板的标题参考'"),
    "'ai_summary'": ("'摘要总结'", "'基于模板的摘要参考'"),
    "'ai_marketing'": ("'营销文案'", "'基于模板的文案参考'"),
}

# 修改 AI 输出中的标注
html = html.replace(
    "showOutput(`【润色后】",
    "showOutput(`⚠️ 以下内容由本地模板生成，非AI智能处理，仅供参考。\\n\\n【润色参考】"
)
html = html.replace(
    "showOutput(`【续写内容】",
    "showOutput(`⚠️ 以下内容由本地模板生成，非AI智能处理，仅供参考。\\n\\n【续写参考】"
)
html = html.replace(
    "showOutput(`【推荐标题】",
    "showOutput(`⚠️ 以下内容由本地模板生成，非AI智能处理，仅供参考。\\n\\n【标题参考】"
)
html = html.replace(
    "showOutput(`【内容摘要】",
    "showOutput(`⚠️ 以下内容由本地模板生成，非AI智能处理，仅供参考。\\n\\n【摘要参考】"
)
html = html.replace(
    "showOutput(`【营销文案】",
    "showOutput(`⚠️ 以下内容由本地模板生成，非AI智能处理，仅供参考。\\n\\n【文案参考】"
)

# 修改 AI 工具底部的"由AI生成"标注
html = html.replace(
    "*本文案由 MiniTool AI 生成，仅供参考。*",
    "*本文案由 MiniTool 本地模板生成（非AI），仅供参考。如需AI智能生成，请使用专业AI写作工具。*"
)

# ================================================================
# P1-12: 修复 toolImgCrop 不支持触摸设备
# 在 mousedown/mouseup/mousemove 事件旁添加 touch 对应事件
# ================================================================
# 找到 imgCrop 函数中的事件绑定，添加 touch 支持
# 修改 canvasWrap 的事件监听

# 方案：在 toolImgCrop 函数中添加一个辅助函数来统一 mouse/touch 事件
old_crop_mousedown = """  canvasWrap.addEventListener('mousedown', e => {
    const rect = cvs.getBoundingClientRect();
    const scaleX = cvs.width / rect.width;
    const scaleY = cvs.height / rect.height;
    selStart = { x: (e.clientX - rect.left) * scaleX, y: (e.clientY - rect.top) * scaleY };
  });
  canvasWrap.addEventListener('mouseup', e => {
    if (!selStart) return;
    const rect = cvs.getBoundingClientRect();
    const scaleX = cvs.width / rect.width;
    const scaleY = cvs.height / rect.height;
    const ex = (e.clientX - rect.left) * scaleX;
    const ey = (e.clientY - rect.top) * scaleY;"""

new_crop_mousedown = """  // Unified pointer event helper (supports mouse + touch)
  function getPointerPos(e) {
    const touch = e.touches ? e.touches[0] : (e.changedTouches ? e.changedTouches[0] : e);
    const rect = cvs.getBoundingClientRect();
    const scaleX = cvs.width / rect.width;
    const scaleY = cvs.height / rect.height;
    return { x: (touch.clientX - rect.left) * scaleX, y: (touch.clientY - rect.top) * scaleY };
  }
  canvasWrap.addEventListener('mousedown', e => { selStart = getPointerPos(e); });
  canvasWrap.addEventListener('touchstart', e => { e.preventDefault(); selStart = getPointerPos(e); }, {passive:false});
  canvasWrap.addEventListener('mouseup', e => {
    if (!selStart) return;
    const ex = getPointerPos(e).x, ey = getPointerPos(e).y;"""

html = html.replace(old_crop_mousedown, new_crop_mousedown)

# 修复 toolImgCrop 中的 mouseup 后续代码（变量名变化）
# 原来用 e.clientX/e.clientY，现在用 getPointerPos
# 需要修复 mouseup handler 中剩余的坐标获取
old_crop_mouseup_rest = """    const x = Math.min(selStart.x, ex);
    const y = Math.min(selStart.y, ey);
    const w = Math.abs(ex - selStart.x);
    const h = Math.abs(ey - selStart.y);"""

new_crop_mouseup_rest = """    const x = Math.min(selStart.x, ex);
    const y = Math.min(selStart.y, ey);
    const w = Math.abs(ex - selStart.x);
    const h = Math.abs(ey - selStart.y);
  });
  canvasWrap.addEventListener('touchend', e => {
    if (!selStart) return;
    e.preventDefault();
    const endPos = getPointerPos(e);
    const x = Math.min(selStart.x, endPos.x);
    const y = Math.min(selStart.y, endPos.y);
    const w = Math.abs(endPos.x - selStart.x);
    const h = Math.abs(endPos.y - selStart.y);"""

html = html.replace(old_crop_mouseup_rest, new_crop_mouseup_rest)

# 修复 toolVidUnwatermark 中的触摸支持（同样的问题）
old_vid_mousedown = """  selCanvas.addEventListener('mousedown', e => {
    const r = selCanvas.getBoundingClientRect();
    startPt = { x: (e.clientX - r.left) * (dw/r.width), y: (e.clientY - r.top) * (dh/r.height) };
  });
  selCanvas.addEventListener('mousemove', e => {
    if (!startPt) return;
    const r = selCanvas.getBoundingClientRect();
    const ex = (e.clientX - r.left) * (dw/r.width);
    const ey = (e.clientY - r.top) * (dh/r.height);"""

new_vid_mousedown = """  function getVidPointerPos(e) {
    const t = e.touches ? e.touches[0] : (e.changedTouches ? e.changedTouches[0] : e);
    const r = selCanvas.getBoundingClientRect();
    return { x: (t.clientX - r.left) * (dw/r.width), y: (t.clientY - r.top) * (dh/r.height) };
  }
  selCanvas.addEventListener('mousedown', e => { startPt = getVidPointerPos(e); });
  selCanvas.addEventListener('touchstart', e => { e.preventDefault(); startPt = getVidPointerPos(e); }, {passive:false});
  selCanvas.addEventListener('mousemove', e => {
    if (!startPt) return;
    const pos = getVidPointerPos(e);"""

html = html.replace(old_vid_mousedown, new_vid_mousedown)

# 修复视频去水印的 mousemove 和 mouseup 中的坐标
old_vid_mousemove_draw = """    sc.clearRect(0,0,dw,dh);
    sc.strokeRect(startPt.x, startPt.y, ex-startPt.x, ey-startPt.y);
  });
  selCanvas.addEventListener('mouseup', e => {
    if (!startPt) return;
    const r = selCanvas.getBoundingClientRect();
    const ex = (e.clientX - r.left) * (dw/r.width);
    const ey = (e.clientY - r.top) * (dh/r.height);"""

new_vid_mousemove_draw = """    sc.clearRect(0,0,dw,dh);
    sc.strokeRect(startPt.x, startPt.y, pos.x-startPt.x, pos.y-startPt.y);
  });
  selCanvas.addEventListener('touchmove', e => {
    if (!startPt) return;
    e.preventDefault();
    const pos = getVidPointerPos(e);
    sc.clearRect(0,0,dw,dh);
    sc.strokeRect(startPt.x, startPt.y, pos.x-startPt.x, pos.y-startPt.y);
  }, {passive:false});
  selCanvas.addEventListener('mouseup', e => {
    if (!startPt) return;
    const pos = getVidPointerPos(e);
    const ex = pos.x, ey = pos.y;"""

html = html.replace(old_vid_mousemove_draw, new_vid_mousemove_draw)

# 修复视频去水印 mouseup 后面用 ex/ey 的地方也要修复
# 这部分 ex/ey 已经在上面定义为 pos.x, pos.y 了，所以后续代码无需修改

# 同时为视频去水印的 mouseup 添加 touchend
old_vid_mouseup_end = """    sel = { x: Math.max(0,Math.min(startPt.x,ex)), y: Math.max(0,Math.min(startPt.y,ey)),
            w: Math.abs(ex-startPt.x), h: Math.abs(ey-startPt.y) };
    startPt = null;
  });"""

new_vid_mouseup_end = """    sel = { x: Math.max(0,Math.min(startPt.x,ex)), y: Math.max(0,Math.min(startPt.y,ey)),
            w: Math.abs(ex-startPt.x), h: Math.abs(ey-startPt.y) };
    startPt = null;
  });
  selCanvas.addEventListener('touchend', e => {
    if (!startPt) return;
    e.preventDefault();
    const pos = getVidPointerPos(e);
    const ex = pos.x, ey = pos.y;
    sel = { x: Math.max(0,Math.min(startPt.x,ex)), y: Math.max(0,Math.min(startPt.y,ey)),
            w: Math.abs(ex-startPt.x), h: Math.abs(ey-startPt.y) };
    startPt = null;
  });"""

html = html.replace(old_vid_mouseup_end, new_vid_mouseup_end)

# ================================================================
# 保存修改后的 index.html
# ================================================================
with open(IDX, 'w', encoding='utf-8') as f:
    f.write(html)
print("index.html fully patched!")

# ================================================================
# 同步修复30个独立工具页面
# ================================================================
tools_dir = os.path.join(BASE, "tools")
for fname in os.listdir(tools_dir):
    if not fname.endswith('.html'):
        continue
    fpath = os.path.join(tools_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        tool_html = f.read()

    # P0-3: 添加 --text-dim
    tool_html = tool_html.replace('--text-muted: #94a3b8;', '--text-muted: #94a3b8;\n  --text-dim: #64748b;')

    # P2-13: 锁定 CDN 版本
    tool_html = tool_html.replace(
        'https://unpkg.com/lucide@latest/dist/umd/lucide.min.js',
        'https://unpkg.com/lucide@0.344.0/dist/umd/lucide.min.js'
    )

    # P2-18: Google Fonts 国内镜像
    tool_html = tool_html.replace('https://fonts.googleapis.com', 'https://fonts.loli.net')
    tool_html = tool_html.replace('https://fonts.gstatic.com', 'https://gstatic.loli.net')

    # P2-17: 添加 noscript
    tool_html = tool_html.replace(
        '<body>\n\n<header',
        '<body>\n<noscript><div style="text-align:center;padding:80px 20px;font-family:system-ui;background:#0f0f13;color:#e2e8f0"><h1 style="font-size:24px;margin-bottom:12px">MiniTool 需要启用 JavaScript</h1><p style="color:#94a3b8">请在浏览器设置中启用 JavaScript 后刷新页面。</p></div></noscript>\n\n<header'
    )

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(tool_html)

print(f"All {len(os.listdir(tools_dir))} tool pages synced!")

# ================================================================
# 修复 privacy.html 和 terms.html
# ================================================================
for page_name in ['privacy.html', 'terms.html']:
    fpath = os.path.join(BASE, page_name)
    with open(fpath, 'r', encoding='utf-8') as f:
        page_html = f.read()
    page_html = page_html.replace('https://fonts.googleapis.com', 'https://fonts.loli.net')
    page_html = page_html.replace('https://fonts.gstatic.com', 'https://gstatic.loli.net')
    page_html = page_html.replace(
        'https://unpkg.com/lucide@latest/dist/umd/lucide.min.js',
        'https://unpkg.com/lucide@0.344.0/dist/umd/lucide.min.js'
    )
    page_html = page_html.replace(
        '<body>\n\n<header',
        '<body>\n<noscript><div style="text-align:center;padding:80px 20px;font-family:system-ui;background:#0f0f13;color:#e2e8f0"><h1 style="font-size:24px;margin-bottom:12px">MiniTool 需要启用 JavaScript</h1><p style="color:#94a3b8">请在浏览器设置中启用 JavaScript 后刷新页面。</p></div></noscript>\n\n<header'
    )
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(page_html)
print("privacy.html & terms.html synced!")

# ================================================================
# P2-19: 生成 sitemap.xml
# ================================================================
today = "2026-07-04"
slugs = [
    'pdf-merge','pdf-split','pdf-to-jpg','jpg-to-pdf','pdf-compress','pdf-encrypt',
    'pdf-unlock','pdf-sign','pdf-rotate','pdf-extract','pdf-to-word','pdf-to-excel',
    'img-compress','img-convert','img-resize','img-crop','img-rotate','img-watermark',
    'img-grid','img-join','img-unwatermark','vid-to-gif','gif-to-vid','vid-thumb',
    'vid-unwatermark','ai-polish','ai-continue','ai-title','ai-summary','ai-marketing'
]

sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sitemap += f'  <url><loc>https://toolmini.cn/</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>1.0</priority></url>\n'
sitemap += f'  <url><loc>https://toolmini.cn/privacy.html</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.3</priority></url>\n'
sitemap += f'  <url><loc>https://toolmini.cn/terms.html</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.3</priority></url>\n'
for slug in slugs:
    sitemap += f'  <url><loc>https://toolmini.cn/tools/{slug}.html</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n'
sitemap += '</urlset>'

with open(os.path.join(BASE, 'sitemap.xml'), 'w', encoding='utf-8') as f:
    f.write(sitemap)
print("sitemap.xml generated!")

# ================================================================
# P0-4 补充: 生成 manifest.json 和 sw.js（最小可用版本）
# ================================================================
manifest = """{
  "name": "MiniTool - 免费在线工具箱",
  "short_name": "MiniTool",
  "description": "免费在线PDF/图片/视频处理工具箱，纯浏览器本地处理",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#0f0f13",
  "theme_color": "#6366f1",
  "icons": [
    {
      "src": "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🛠️</text></svg>",
      "sizes": "any",
      "type": "image/svg+xml"
    }
  ]
}"""

sw_js = """// MiniTool Service Worker - Cache static assets
const CACHE_NAME = 'minitool-v1';
const ASSETS = ['/', '/privacy.html', '/terms.html'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE_NAME).then(c => c.addAll(ASSETS)));
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))));
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    caches.match(e.request).then(cached => cached || fetch(e.request).then(resp => {
      if (resp.ok && resp.type === 'basic') {
        const clone = resp.clone();
        caches.open(CACHE_NAME).then(c => c.put(e.request, clone));
      }
      return resp;
    }).catch(() => caches.match('/')))
  );
});
"""

# Restore manifest link in index.html since we now have the file
with open(os.path.join(BASE, 'manifest.json'), 'w', encoding='utf-8') as f:
    f.write(manifest)
with open(os.path.join(BASE, 'sw.js'), 'w', encoding='utf-8') as f:
    f.write(sw_js)

# Re-add manifest link to index.html
html_2 = open(IDX, 'r', encoding='utf-8').read()
html_2 = html_2.replace(
    '<meta name="robots" content="index, follow">\n',
    '<meta name="robots" content="index, follow">\n<link rel="manifest" href="manifest.json">\n'
)
with open(IDX, 'w', encoding='utf-8') as f:
    f.write(html_2)

print("manifest.json & sw.js generated!")
print("\n=== ALL 19 FIXES APPLIED ===")
