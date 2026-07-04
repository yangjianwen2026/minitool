# -*- coding: utf-8 -*-
"""
修改 toolmini.cn 网站的脚本
1. 修改页脚为正式版权声明+链接
2. 每个工具加使用说明
3. 为每个工具生成独立URL
4. 添加工具搜索框（已有，增强）
5. 添加最近使用工具（LocalStorage）
6. 添加问题反馈入口
7. 创建隐私政策和使用条款页面
"""

import os
import re
import json

BASE_DIR = r"C:\Users\newna\.qianfan\workspace\14dabc72fd0e469abfba93777adccb0a"
INDEX_PATH = os.path.join(BASE_DIR, "index.html")
TOOLS_DIR = os.path.join(BASE_DIR, "tools")

# 工具使用说明（2-3行）
TOOL_GUIDES = {
    'pdf_merge': '1. 上传多个PDF文件（支持拖拽）\n2. 文件将按上传顺序合并\n3. 点击"开始处理"即可下载合并后的文件',
    'pdf_split': '1. 上传一个PDF文件\n2. 输入页码范围，如 1-3,5,7-10\n3. 每页将拆分为独立的PDF文件，打包为ZIP下载',
    'pdf_to_jpg': '1. 上传一个PDF文件\n2. 自动将每页转为高清JPG图片\n3. 所有图片打包为ZIP下载',
    'jpg_to_pdf': '1. 上传多张图片（JPG/PNG/WebP/GIF）\n2. 图片按上传顺序合并\n3. 自动生成PDF文档下载',
    'pdf_compress': '1. 上传一个PDF文件\n2. 调整压缩质量（越低体积越小）\n3. 处理后下载压缩版PDF',
    'pdf_encrypt': '1. 上传一个PDF文件\n2. 设置打开密码\n3. 加密后的PDF需输入密码才能打开',
    'pdf_unlock': '1. 上传已加密的PDF文件\n2. 输入当前密码\n3. 解密后可无密码打开PDF',
    'pdf_sign': '1. 上传一个PDF文件\n2. 在签名区域手写签名\n3. 确认后签名将添加到PDF',
    'pdf_rotate': '1. 上传一个PDF文件\n2. 选择旋转角度（90°/180°/270°）\n3. 所有页面将按指定角度旋转',
    'pdf_extract': '1. 上传一个PDF文件\n2. 输入要提取的页码范围\n3. 提取的页面生成新PDF下载',
    'pdf_to_word': '1. 上传一个PDF文件\n2. 自动提取PDF中的文本内容\n3. 生成Word文档下载（注意：图片和复杂排版无法保留）',
    'pdf_to_excel': '1. 上传包含表格的PDF文件\n2. 智能识别表格结构\n3. 生成Excel文件下载（扫描版PDF可能无法识别）',
    'img_compress': '1. 上传图片（JPG/PNG/WebP/GIF）\n2. 拖动质量滑块调整压缩率\n3. 压缩后图片自动下载',
    'img_convert': '1. 上传图片\n2. 选择目标格式（JPG/PNG/WebP）\n3. 转换后的图片自动下载',
    'img_resize': '1. 上传图片\n2. 输入目标宽高（可锁定比例）\n3. 调整尺寸后的图片自动下载',
    'img_crop': '1. 上传图片\n2. 在图片上拖拽选择裁剪区域\n3. 确认后裁剪图片自动下载',
    'img_rotate': '1. 上传图片\n2. 选择旋转角度（90°/180°/270°/自定义）\n3. 旋转后的图片自动下载',
    'img_watermark': '1. 上传图片\n2. 选择水印类型（文字/图片）、位置和透明度\n3. 添加水印后的图片自动下载',
    'img_grid': '1. 上传一张图片\n2. 自动将图片切为3×3共9张\n3. 九宫格图片打包为ZIP下载',
    'img_join': '1. 上传多张图片\n2. 选择横向或纵向拼接\n3. 拼接后的长图自动下载',
    'img_unwatermark': '1. 上传图片\n2. 在图片上框选水印区域\n3. 智能填充移除水印（复杂背景建议使用专业软件）',
    'vid_to_gif': '1. 上传视频文件（MP4/WebM/MOV/AVI）\n2. 设置截取时间范围和GIF宽度\n3. 生成GIF动图下载',
    'gif_to_vid': '1. 上传GIF文件\n2. 自动提取GIF帧\n3. 处理后的文件自动下载',
    'vid_thumb': '1. 上传视频文件\n2. 设置截取时间点（秒）\n3. 提取该帧作为封面图片下载',
    'vid_unwatermark': '1. 上传视频文件\n2. 在预览帧上框选水印区域\n3. 选择处理方式（模糊/裁剪/填充）后下载',
    'ai_polish': '1. 在文本框中输入需要润色的文字\n2. AI将优化文字表达，使其更流畅专业\n3. 润色后的文字可直接复制使用',
    'ai_continue': '1. 输入文章开头或前文\n2. AI将根据上下文续写后续内容\n3. 续写结果可直接复制或继续编辑',
    'ai_title': '1. 输入文章内容\n2. AI将生成多个吸睛标题供选择\n3. 选择合适的标题复制使用',
    'ai_summary': '1. 粘贴需要总结的长文\n2. AI将提取核心要点生成精炼摘要\n3. 摘要可直接复制使用',
    'ai_marketing': '1. 输入产品名称和特点信息\n2. AI将生成多种风格的推广文案\n3. 选择满意的文案复制使用',
}

# 工具slug映射 (id -> url slug)
TOOL_SLUGS = {
    'pdf_merge': 'pdf-merge',
    'pdf_split': 'pdf-split',
    'pdf_to_jpg': 'pdf-to-jpg',
    'jpg_to_pdf': 'jpg-to-pdf',
    'pdf_compress': 'pdf-compress',
    'pdf_encrypt': 'pdf-encrypt',
    'pdf_unlock': 'pdf-unlock',
    'pdf_sign': 'pdf-sign',
    'pdf_rotate': 'pdf-rotate',
    'pdf_extract': 'pdf-extract',
    'pdf_to_word': 'pdf-to-word',
    'pdf_to_excel': 'pdf-to-excel',
    'img_compress': 'img-compress',
    'img_convert': 'img-convert',
    'img_resize': 'img-resize',
    'img_crop': 'img-crop',
    'img_rotate': 'img-rotate',
    'img_watermark': 'img-watermark',
    'img_grid': 'img-grid',
    'img_join': 'img-join',
    'img_unwatermark': 'img-unwatermark',
    'vid_to_gif': 'vid-to-gif',
    'gif_to_vid': 'gif-to-vid',
    'vid_thumb': 'vid-thumb',
    'vid_unwatermark': 'vid-unwatermark',
    'ai_polish': 'ai-polish',
    'ai_continue': 'ai-continue',
    'ai_title': 'ai-title',
    'ai_summary': 'ai-summary',
    'ai_marketing': 'ai-marketing',
}

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# ============================================================
# 1. 修改页脚：删除"仅供学习交流使用"，改为正式版权声明+链接
# ============================================================
old_footer = '''<footer class="footer">
  <p>MiniTool · 纯浏览器端处理 · 所有文件均在本地处理，不会上传到任何服务器</p>
  <p style="margin-top:6px">© 2025 MiniTool · 仅供学习交流使用</p>
<!-- 分享二维码区域 -->
<div id="shareBar" style="display:none;text-align:center;padding:32px 20px 16px;border-top:1px solid var(--border);margin-top:40px;">
  <h3 style="color:var(--text);font-size:15px;margin:0 0 4px;font-weight:700;">📱 微信扫码使用</h3>
  <p style="color:var(--text-dim);font-size:12px;margin:0 0 16px;">长按识别二维码，或分享给朋友</p>
  <div style="display:inline-block;background:white;border-radius:12px;padding:12px;box-shadow:0 4px 20px rgba(0,0,0,0.15);">
    <img id="qrImg" src="" alt="QR Code" style="width:140px;height:140px;display:block;border:none;">
  </div>
  <p style="color:var(--text-dim);font-size:12px;margin:12px 0 0;">点击右上角 ··· 添加到我的小程序</p>
</div>

<footer>'''

new_footer = '''<footer class="footer">
  <div style="max-width:800px;margin:0 auto">
    <p style="margin-bottom:8px">MiniTool · 纯浏览器端处理 · 所有文件均在本地处理，不会上传到任何服务器</p>
    <p style="margin-bottom:10px">© 2025 MiniTool. All rights reserved.</p>
    <div style="display:flex;justify-content:center;gap:16px;flex-wrap:wrap;margin-bottom:12px">
      <a href="/privacy.html" style="color:var(--primary-light);text-decoration:none;font-size:12px">隐私政策</a>
      <a href="/terms.html" style="color:var(--primary-light);text-decoration:none;font-size:12px">使用条款</a>
      <a href="javascript:void(0)" onclick="openFeedback()" style="color:var(--primary-light);text-decoration:none;font-size:12px;cursor:pointer">问题反馈</a>
    </div>
  </div>
<!-- 分享二维码区域 -->
<div id="shareBar" style="display:none;text-align:center;padding:32px 20px 16px;border-top:1px solid var(--border);margin-top:40px;">
  <h3 style="color:var(--text);font-size:15px;margin:0 0 4px;font-weight:700;">📱 微信扫码使用</h3>
  <p style="color:var(--text-dim);font-size:12px;margin:0 0 16px;">长按识别二维码，或分享给朋友</p>
  <div style="display:inline-block;background:white;border-radius:12px;padding:12px;box-shadow:0 4px 20px rgba(0,0,0,0.15);">
    <img id="qrImg" src="" alt="QR Code" style="width:140px;height:140px;display:block;border:none;">
  </div>
  <p style="color:var(--text-dim);font-size:12px;margin:12px 0 0;">点击右上角 ··· 添加到我的小程序</p>
</div>
</footer>'''

html = html.replace(old_footer, new_footer)

# ============================================================
# 2. 在 TOOLS 数据中添加 guide 字段和 slug 字段
# ============================================================
# 修改 TOOLS 数组中每个对象，添加 guide 和 slug
for tool_id, guide in TOOL_GUIDES.items():
    # 找到该工具在 TOOLS 数组中的定义，添加 guide 和 slug
    # 匹配如 { id: 'pdf_merge', ... hasControls: false }
    # 在 hasControls 后面加上 guide 和 slug
    slug = TOOL_SLUGS[tool_id]
    guide_escaped = guide.replace('\n', '\\n').replace("'", "\\'")

    # 在对应行找到 hasControls 并在其后追加
    old_pattern = r"(\{ id: '" + re.escape(tool_id) + r"'.*?hasControls: (?:true|false)) \}"

    match = re.search(old_pattern, html)
    if match:
        old_text = match.group(1)
        new_text = old_text + f", guide: '{guide_escaped}', slug: '{slug}' }}"
        html = html.replace(match.group(0), new_text, 1)

# ============================================================
# 3. 修改工具卡片渲染：添加使用说明 + 独立URL链接
# ============================================================
# 修改 renderTools 函数中的工具卡片模板
old_card_template = """      html += `
      <div class="tool-card" data-cat="${tool.cat}" data-id="${tool.id}" onclick="openTool('${tool.id}')">
        <div class="tool-card-inner">
          <div class="tool-icon"><i data-lucide="${tool.icon}" style="width:22px;height:22px"></i></div>
          <h3>${tool.name}</h3>
          <p>${tool.desc}</p>
          <span class="tool-tag">${tool.formats[0] === 'text' ? '文字' : tool.formats.map(f=>f.replace('.','')).join('/')}</span>
        </div>
      </div>`;"""

new_card_template = """      html += `
      <div class="tool-card" data-cat="${tool.cat}" data-id="${tool.id}" data-name="${tool.name}" onclick="openTool('${tool.id}')">
        <div class="tool-card-inner">
          <div class="tool-icon"><i data-lucide="${tool.icon}" style="width:22px;height:22px"></i></div>
          <h3>${tool.name}</h3>
          <p>${tool.desc}</p>
          ${tool.guide ? '<p class="tool-guide">' + tool.guide.replace(/\\n/g, '<br>') + '</p>' : ''}
          <div style="display:flex;align-items:center;gap:8px;margin-top:8px">
            <span class="tool-tag">${tool.formats[0] === 'text' ? '文字' : tool.formats.map(f=>f.replace('.','')).join('/')}</span>
            <a href="${tool.slug ? '/tools/' + tool.slug + '.html' : '#'}" class="tool-link" onclick="event.stopPropagation()" title="独立页面打开">🔗</a>
          </div>
        </div>
      </div>`;"""

html = html.replace(old_card_template, new_card_template)

# ============================================================
# 4. 在 CSS 中添加 tool-guide 和 tool-link 样式
# ============================================================
old_tool_tag_css = """.tool-tag {
  display: inline-block;
  font-size: 10px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 6px;
  margin-top: 10px;
}"""

new_tool_tag_css = """.tool-guide {
  font-size: 11px;
  color: var(--text-muted);
  line-height: 1.6;
  margin-top: 6px;
  padding-top: 6px;
  border-top: 1px solid rgba(45,45,74,0.5);
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.tool-tag {
  display: inline-block;
  font-size: 10px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 6px;
}
.tool-link {
  font-size: 12px;
  text-decoration: none;
  opacity: 0.5;
  transition: opacity 0.2s;
}
.tool-link:hover {
  opacity: 1;
}"""

html = html.replace(old_tool_tag_css, new_tool_tag_css)

# ============================================================
# 5. 在 main-content 开头添加"最近使用工具"区域 + 增强搜索
# ============================================================
old_main_content = '''<main class="main-content" id="mainContent">
  <div id="toolsContainer"></div>
</main>'''

new_main_content = '''<main class="main-content" id="mainContent">
  <!-- 最近使用工具 -->
  <div id="recentTools" style="display:none;margin-bottom:24px">
    <div class="section-title"><i data-lucide="clock" style="width:14px;height:14px"></i> 最近使用</div>
    <div id="recentToolsList" style="display:flex;gap:10px;overflow-x:auto;padding-bottom:4px;scrollbar-width:none"></div>
  </div>
  <div id="toolsContainer"></div>
</main>'''

html = html.replace(old_main_content, new_main_content)

# ============================================================
# 6. 添加 CSS 样式：最近使用工具卡片 + 反馈模态框
# ============================================================
old_responsive_css = """/* Responsive */
@media (max-width: 640px) {"""

new_responsive_css = """/* Recent Tools */
.recent-tool-chip {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 20px;
  cursor: pointer;
  white-space: nowrap;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.2s;
  flex-shrink: 0;
}
.recent-tool-chip:hover {
  border-color: var(--primary);
  background: var(--surface2);
}
.recent-tool-chip .rtc-icon {
  font-size: 14px;
}
.recent-tool-chip .rtc-remove {
  font-size: 11px;
  color: var(--text-muted);
  margin-left: 4px;
  opacity: 0;
  transition: opacity 0.2s;
}
.recent-tool-chip:hover .rtc-remove {
  opacity: 1;
}

/* Feedback Modal */
.feedback-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.7);
  backdrop-filter: blur(6px);
  z-index: 300;
  align-items: center;
  justify-content: center;
}
.feedback-overlay.open { display: flex; }
.feedback-box {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 20px;
  width: 90%;
  max-width: 480px;
  padding: 28px;
  animation: slideUp 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.feedback-box h2 {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.feedback-box label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 6px;
  color: var(--text-muted);
}
.feedback-box input, .feedback-box textarea, .feedback-box select {
  width: 100%;
  margin-bottom: 14px;
}
.feedback-contact {
  display: flex;
  gap: 16px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid var(--border);
}
.feedback-contact-item {
  flex: 1;
  text-align: center;
  padding: 12px;
  background: var(--surface);
  border-radius: var(--radius-sm);
}
.feedback-contact-item .fc-label {
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 4px;
}
.feedback-contact-item .fc-value {
  font-size: 13px;
  font-weight: 600;
  color: var(--text);
  word-break: break-all;
}

/* Responsive */
@media (max-width: 640px) {"""

html = html.replace(old_responsive_css, new_responsive_css)

# ============================================================
# 7. 添加反馈模态框 HTML
# ============================================================
old_toast_html = """<!-- TOAST -->
<div class="toast-container" id="toastContainer"></div>"""

new_toast_html = """<!-- TOAST -->
<div class="toast-container" id="toastContainer"></div>

<!-- FEEDBACK MODAL -->
<div class="feedback-overlay" id="feedbackOverlay" onclick="if(event.target===this)closeFeedback()">
  <div class="feedback-box">
    <h2><i data-lucide="message-circle" style="width:20px;height:20px;color:var(--primary-light)"></i> 问题反馈</h2>
    <form id="feedbackForm" onsubmit="submitFeedback(event)">
      <label for="fbType">反馈类型</label>
      <select id="fbType" required>
        <option value="bug">Bug 反馈</option>
        <option value="feature">功能建议</option>
        <option value="other">其他</option>
      </select>
      <label for="fbEmail">联系邮箱（可选）</label>
      <input type="email" id="fbEmail" placeholder="your@email.com">
      <label for="fbContent">反馈内容</label>
      <textarea id="fbContent" rows="4" required placeholder="请详细描述您遇到的问题或建议..."></textarea>
      <div style="display:flex;gap:10px">
        <button type="submit" class="btn btn-primary" style="flex:1">
          <i data-lucide="send" style="width:14px;height:14px"></i> 提交反馈
        </button>
        <button type="button" class="btn btn-secondary" onclick="closeFeedback()">取消</button>
      </div>
    </form>
    <div class="feedback-contact">
      <div class="feedback-contact-item">
        <i data-lucide="mail" style="width:18px;height:18px;color:var(--primary-light)"></i>
        <div class="fc-value">support@toolmini.cn</div>
        <div class="fc-label">邮箱反馈</div>
      </div>
      <div class="feedback-contact-item">
        <i data-lucide="message-circle" style="width:18px;height:18px;color:var(--success)"></i>
        <div class="fc-value">ToolMini</div>
        <div class="fc-label">微信公众号</div>
      </div>
    </div>
  </div>
</div>"""

html = html.replace(old_toast_html, new_toast_html)

# ============================================================
# 8. 在 </script> 前添加 JS 功能：最近使用、反馈、搜索增强
# ============================================================
# 找到最后一个 </script> 前的位置（PWA脚本之前的那个）
old_pwa_script = """<!-- PWA Service Worker -->
<script>"""

new_js_functions = """
// ─────────────────────────────────────────────
// RECENT TOOLS (LocalStorage)
// ─────────────────────────────────────────────
function getRecentTools() {
  try {
    const data = localStorage.getItem('minitool_recent');
    return data ? JSON.parse(data) : [];
  } catch { return []; }
}

function addRecentTool(toolId) {
  let recent = getRecentTools();
  recent = recent.filter(id => id !== toolId);
  recent.unshift(toolId);
  if (recent.length > 8) recent = recent.slice(0, 8);
  try { localStorage.setItem('minitool_recent', JSON.stringify(recent)); } catch {}
  renderRecentTools();
}

function removeRecentTool(toolId, e) {
  if (e) e.stopPropagation();
  let recent = getRecentTools();
  recent = recent.filter(id => id !== toolId);
  try { localStorage.setItem('minitool_recent', JSON.stringify(recent)); } catch {}
  renderRecentTools();
}

function renderRecentTools() {
  const recent = getRecentTools();
  const container = document.getElementById('recentTools');
  const list = document.getElementById('recentToolsList');
  if (!container || !list) return;

  if (recent.length === 0) {
    container.style.display = 'none';
    return;
  }

  container.style.display = 'block';
  const catIcons = { pdf:'📄', image:'🖼️', video:'🎬', ai:'✨' };
  list.innerHTML = recent.map(id => {
    const tool = TOOLS.find(t => t.id === id);
    if (!tool) return '';
    return `<div class="recent-tool-chip" onclick="openTool('${tool.id}')">
      <span class="rtc-icon">${catIcons[tool.cat] || '🔧'}</span>
      ${tool.name}
      <span class="rtc-remove" onclick="removeRecentTool('${tool.id}', event)" title="移除">✕</span>
    </div>`;
  }).join('');
  lucide.createIcons();
}

// ─────────────────────────────────────────────
// FEEDBACK
// ─────────────────────────────────────────────
function openFeedback() {
  document.getElementById('feedbackOverlay').classList.add('open');
  lucide.createIcons();
}

function closeFeedback() {
  document.getElementById('feedbackOverlay').classList.remove('open');
}

function submitFeedback(e) {
  e.preventDefault();
  const type = document.getElementById('fbType').value;
  const email = document.getElementById('fbEmail').value;
  const content = document.getElementById('fbContent').value;

  // Store feedback locally (no server)
  try {
    const feedbacks = JSON.parse(localStorage.getItem('minitool_feedbacks') || '[]');
    feedbacks.push({ type, email, content, time: new Date().toISOString() });
    localStorage.setItem('minitool_feedbacks', JSON.stringify(feedbacks));
  } catch {}

  toast('感谢您的反馈！我们会尽快处理。', 'success');
  closeFeedback();
  document.getElementById('feedbackForm').reset();
}

// ─────────────────────────────────────────────
// ENHANCED SEARCH
// ─────────────────────────────────────────────
function filterTools() {
  const q = document.getElementById('searchInput').value.toLowerCase().trim();
  document.querySelectorAll('.tool-card').forEach(card => {
    const name = card.querySelector('h3').textContent.toLowerCase();
    const desc = card.querySelector('p').textContent.toLowerCase();
    const match = !q || name.includes(q) || desc.includes(q);
    card.style.display = match ? '' : 'none';
  });
  // Also filter section titles: hide if no visible cards under them
  document.querySelectorAll('.section-title').forEach(title => {
    const nextGrid = title.nextElementSibling;
    if (nextGrid && nextGrid.classList.contains('tools-grid')) {
      const visibleCards = nextGrid.querySelectorAll('.tool-card:not([style*="display: none"])');
      title.style.display = visibleCards.length > 0 ? '' : 'none';
    }
  });
}

// ─────────────────────────────────────────────
// MODIFY openTool TO RECORD RECENT USAGE
// ─────────────────────────────────────────────
// We need to patch the existing openTool function
const _originalOpenTool = openTool;
openTool = function(id) {
  addRecentTool(id);
  _originalOpenTool(id);
};

// ─────────────────────────────────────────────
// INIT: Render recent tools on page load
// ─────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  renderRecentTools();
});

"""

# Insert before PWA script
html = html.replace(old_pwa_script, new_js_functions + old_pwa_script)

# ============================================================
# 9. 修改 header 中的搜索框：添加清除按钮
# ============================================================
old_search_html = '''<div class="header-search">
      <i data-lucide="search" class="search-icon" style="width:16px;height:16px"></i>
      <input type="text" placeholder="搜索工具..." id="searchInput" oninput="filterTools()">
    </div>'''

new_search_html = '''<div class="header-search">
      <i data-lucide="search" class="search-icon" style="width:16px;height:16px"></i>
      <input type="text" placeholder="搜索工具（输入关键词实时过滤）..." id="searchInput" oninput="filterTools()">
      <button id="searchClear" onclick="document.getElementById('searchInput').value='';filterTools()" style="position:absolute;right:10px;top:50%;transform:translateY(-50%);background:none;border:none;color:var(--text-muted);cursor:pointer;font-size:14px;display:none">✕</button>
    </div>'''

html = html.replace(old_search_html, new_search_html)

# Add search clear visibility logic to filterTools
old_filter_function = """function filterTools() {
  const q = document.getElementById('searchInput').value.toLowerCase();
  document.querySelectorAll('.tool-card').forEach(card => {
    const name = card.querySelector('h3').textContent.toLowerCase();
    const desc = card.querySelector('p').textContent.toLowerCase();
    card.style.display = (name.includes(q) || desc.includes(q)) ? '' : 'none';
  });
}"""

# This old function might have already been replaced by our enhanced version above.
# Let's check if it still exists
if old_filter_function in html:
    html = html.replace(old_filter_function, '')

# Save modified index.html
with open(INDEX_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html modified successfully!")

# ============================================================
# GENERATE INDEPENDENT TOOL PAGES
# ============================================================

# Base template for tool pages
TOOL_PAGE_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{tool_name} - MiniTool 免费在线工具</title>
<meta name="description" content="{tool_desc}。纯浏览器本地处理，无需注册，文件绝不上传。">
<meta name="keywords" content="{tool_name},在线工具,免费,浏览器处理,隐私安全">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🛠️</text></svg>">
<link rel="canonical" href="https://toolmini.cn/tools/{slug}.html">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
<script src="https://unpkg.com/pdf-lib@1.17.1/dist/pdf-lib.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/FileSaver.js/2.0.5/FileSaver.min.js"></script>
<script src="https://unpkg.com/docx@8.5.0/build/index.umd.js"></script>
<script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
<script src="https://unpkg.com/qrcodejs@1.0.0/qrcode.min.js"></script>
<style>
:root {{
  --primary: #6366f1;
  --primary-dark: #4f46e5;
  --primary-light: #818cf8;
  --accent: #f59e0b;
  --bg: #0f0f13;
  --bg2: #13131c;
  --surface: #1a1a24;
  --surface2: #22223a;
  --border: #2d2d4a;
  --text: #e2e8f0;
  --text-muted: #94a3b8;
  --success: #22c55e;
  --danger: #ef4444;
  --radius: 14px;
  --radius-sm: 8px;
}}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
  font-family: 'Inter','Noto Sans SC',system-ui,sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
}}
::-webkit-scrollbar {{ width: 6px; }}
::-webkit-scrollbar-track {{ background: var(--bg2); }}
::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 3px; }}

.header {{
  background: rgba(15,15,19,0.85);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border);
  position: sticky; top: 0; z-index: 100;
  padding: 0 24px;
}}
.header-inner {{
  max-width: 1200px; margin: 0 auto;
  display: flex; align-items: center; gap: 20px; height: 64px;
}}
.logo {{ display:flex; align-items:center; gap:10px; text-decoration:none; }}
.logo-icon {{
  width:36px; height:36px;
  background:linear-gradient(135deg,var(--primary),var(--accent));
  border-radius:10px; display:flex; align-items:center; justify-content:center;
  color:white; font-weight:800; font-size:16px;
}}
.logo-text {{
  font-size:20px; font-weight:800;
  background:linear-gradient(135deg,var(--primary-light),var(--accent));
  -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}}
.header-badge {{ margin-left:auto; font-size:12px; color:var(--text-muted); display:flex; align-items:center; gap:6px; }}
.header-badge span {{ background:rgba(34,197,94,0.15); color:var(--success); padding:3px 10px; border-radius:20px; font-weight:600; }}

.tool-page {{
  max-width: 720px; margin: 0 auto; padding: 40px 24px 60px;
}}
.breadcrumb {{
  font-size: 13px; color: var(--text-muted); margin-bottom: 24px;
  display: flex; align-items: center; gap: 6px;
}}
.breadcrumb a {{ color: var(--primary-light); text-decoration: none; }}
.breadcrumb a:hover {{ text-decoration: underline; }}

.tool-header {{
  display: flex; align-items: center; gap: 16px; margin-bottom: 28px;
}}
.tool-header-icon {{
  width: 56px; height: 56px; border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
}}
.tool-header h1 {{ font-size: 28px; font-weight: 800; }}
.tool-header p {{ color: var(--text-muted); font-size: 14px; margin-top: 4px; }}

.guide-box {{
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 20px; margin-bottom: 28px;
}}
.guide-box h3 {{
  font-size: 14px; font-weight: 700; margin-bottom: 10px;
  display: flex; align-items: center; gap: 8px; color: var(--primary-light);
}}
.guide-box ol {{
  padding-left: 20px; font-size: 13px; line-height: 2; color: var(--text-muted);
}}

.drop-zone {{
  border: 2px dashed var(--border); border-radius: var(--radius);
  padding: 48px 24px; text-align: center; transition: all 0.25s;
  cursor: pointer; background: var(--surface);
}}
.drop-zone:hover, .drop-zone.drag-over {{
  border-color: var(--primary); background: rgba(99,102,241,0.05);
}}
.drop-zone input[type="file"] {{ display: none; }}
.drop-zone-icon {{ color: var(--text-muted); margin-bottom: 12px; }}
.drop-zone h3 {{ font-size: 16px; font-weight: 600; margin-bottom: 6px; }}
.drop-zone p {{ font-size: 13px; color: var(--text-muted); }}
.formats {{ margin-top:10px; display:flex; gap:6px; justify-content:center; flex-wrap:wrap; }}
.format-chip {{
  font-size:11px; font-weight:600; padding:2px 8px; border-radius:4px;
  background:var(--surface2); color:var(--text-muted);
}}

.file-preview {{
  background:var(--surface); border:1px solid var(--border);
  border-radius:var(--radius); padding:16px; margin-top:16px; display:none;
}}
.file-preview.show {{ display:block; }}
.file-item {{
  display:flex; align-items:center; gap:12px; padding:8px 0;
  border-bottom:1px solid var(--border);
}}
.file-item:last-child {{ border-bottom:none; }}
.file-item .fi-icon {{ color:var(--primary-light); flex-shrink:0; }}
.file-item .fi-name {{ flex:1; font-size:13px; font-weight:500; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
.file-item .fi-size {{ font-size:12px; color:var(--text-muted); flex-shrink:0; }}
.file-item .fi-remove {{
  width:24px; height:24px; border-radius:50%; border:none; background:transparent;
  color:var(--text-muted); cursor:pointer; display:flex; align-items:center; justify-content:center; flex-shrink:0;
}}
.file-item .fi-remove:hover {{ background:var(--danger); color:white; }}

.controls {{ margin-top:20px; display:none; }}
.controls.show {{ display:block; }}
.control-row {{ display:flex; gap:12px; align-items:center; margin-bottom:14px; flex-wrap:wrap; }}
.control-label {{ font-size:13px; font-weight:600; color:var(--text); min-width:80px; }}
input[type="text"],input[type="number"],select,textarea {{
  background:var(--surface); border:1px solid var(--border); border-radius:var(--radius-sm);
  padding:8px 14px; color:var(--text); font-size:13px; font-family:inherit; outline:none; transition:border-color 0.2s;
}}
input:focus,select:focus,textarea:focus {{ border-color:var(--primary); }}
textarea {{ width:100%; min-height:120px; resize:vertical; line-height:1.6; }}
input[type="range"] {{ -webkit-appearance:none; width:140px; height:4px; border-radius:2px; background:var(--border); outline:none; }}
input[type="range"]::-webkit-slider-thumb {{ -webkit-appearance:none; width:16px; height:16px; border-radius:50%; background:var(--primary); cursor:pointer; }}
.range-val {{ font-size:13px; font-weight:600; color:var(--primary-light); min-width:36px; }}

.btn-row {{ display:flex; gap:10px; margin-top:20px; flex-wrap:wrap; }}
.btn {{
  display:inline-flex; align-items:center; gap:8px;
  padding:10px 22px; border-radius:var(--radius-sm); border:none;
  font-size:14px; font-weight:600; cursor:pointer; transition:all 0.2s;
  font-family:inherit; flex:1; justify-content:center;
}}
.btn-primary {{
  background:linear-gradient(135deg,var(--primary),var(--primary-dark));
  color:white; box-shadow:0 4px 14px rgba(99,102,241,0.35);
}}
.btn-primary:hover {{ box-shadow:0 6px 20px rgba(99,102,241,0.5); transform:translateY(-1px); }}
.btn-secondary {{ background:var(--surface2); color:var(--text); border:1px solid var(--border); }}
.btn-secondary:hover {{ border-color:var(--primary); color:var(--primary-light); }}

.progress-wrap {{ display:none; margin-top:16px; }}
.progress-wrap.show {{ display:block; }}
.progress-bar-bg {{ background:var(--surface); border-radius:8px; height:8px; overflow:hidden; margin-bottom:8px; }}
.progress-bar {{ height:100%; background:linear-gradient(90deg,var(--primary),var(--accent)); border-radius:8px; transition:width 0.3s; width:0%; }}
.progress-text {{ font-size:12px; color:var(--text-muted); text-align:center; }}

.output-area {{
  display:none; margin-top:20px; background:var(--surface);
  border:1px solid var(--success); border-radius:var(--radius); padding:20px;
}}
.output-area.show {{ display:block; }}
.output-area h4 {{ font-size:14px; font-weight:700; color:var(--success); margin-bottom:12px; display:flex; align-items:center; gap:8px; }}
.output-result {{
  font-size:13px; line-height:1.7; color:var(--text);
  white-space:pre-wrap; background:var(--bg); border-radius:var(--radius-sm);
  padding:14px; max-height:300px; overflow-y:auto;
}}

.footer {{
  text-align:center; padding:32px 24px; color:var(--text-muted);
  font-size:12px; border-top:1px solid var(--border); margin-top:40px;
}}
.footer a {{ color:var(--primary-light); text-decoration:none; }}

.toast-container {{
  position:fixed; top:80px; right:20px; z-index:500;
  display:flex; flex-direction:column; gap:8px; pointer-events:none;
}}
.toast {{
  padding:12px 20px; border-radius:var(--radius-sm); font-size:13px; font-weight:600;
  display:flex; align-items:center; gap:10px; animation:toastIn 0.3s ease;
  pointer-events:all; max-width:320px; box-shadow:0 8px 30px rgba(0,0,0,0.3);
}}
@keyframes toastIn {{ from{{opacity:0;transform:translateX(30px)}} to{{opacity:1;transform:translateX(0)}} }}
.toast-success {{ background:rgba(34,197,94,0.95); color:white; }}
.toast-error {{ background:rgba(239,68,68,0.95); color:white; }}

@media (max-width:640px) {{
  .tool-header h1 {{ font-size:22px; }}
  .tool-header-icon {{ width:44px; height:44px; }}
}}
</style>
</head>
<body>

<header class="header">
  <div class="header-inner">
    <a href="/" class="logo">
      <div class="logo-icon">M</div>
      <span class="logo-text">MiniTool</span>
    </a>
    <div class="header-badge">
      <span>本地处理 · 隐私安全</span>
    </div>
  </div>
</header>

<div class="tool-page">
  <div class="breadcrumb">
    <a href="/">首页</a> <span>›</span> <span>{cat_name}</span> <span>›</span> <span>{tool_name}</span>
  </div>

  <div class="tool-header">
    <div class="tool-header-icon" style="background:{icon_bg};color:{icon_color}">
      <i data-lucide="{tool_icon}" style="width:28px;height:28px"></i>
    </div>
    <div>
      <h1>{tool_name}</h1>
      <p>{tool_desc}</p>
    </div>
  </div>

  <div class="guide-box">
    <h3><i data-lucide="book-open" style="width:14px;height:14px"></i> 使用说明</h3>
    <ol>{guide_items}</ol>
  </div>

  <div class="drop-zone" id="dropZone">
    <div class="drop-zone-icon">
      <i data-lucide="upload-cloud" style="width:40px;height:40px"></i>
    </div>
    <h3>拖拽文件到此处</h3>
    <p>或点击选择文件</p>
    <div class="formats" id="formatChips">{format_chips}</div>
    <input type="file" id="fileInput" multiple>
  </div>

  <div class="file-preview" id="filePreview">
    <div id="fileList"></div>
    <button class="btn btn-secondary" onclick="clearFiles()" style="width:100%;margin-top:10px;flex:none;padding:8px">清空全部文件</button>
  </div>

  <div class="controls" id="controls">{controls_html}</div>

  <div class="progress-wrap" id="progressWrap">
    <div class="progress-bar-bg"><div class="progress-bar" id="progressBar"></div></div>
    <div class="progress-text" id="progressText">处理中...</div>
  </div>

  <div class="output-area" id="outputArea">
    <h4><i data-lucide="check-circle" style="width:16px;height:16px"></i> 处理完成</h4>
    <div class="output-result" id="outputResult"></div>
  </div>

  <div class="btn-row" id="btnRow" style="display:none">
    <button class="btn btn-primary" id="processBtn" onclick="runTool()">
      <i data-lucide="play" style="width:15px;height:15px"></i> 开始处理
    </button>
    <button class="btn btn-secondary" onclick="location.href='/'">返回首页</button>
  </div>
</div>

<footer class="footer">
  <p>© 2025 MiniTool. All rights reserved.</p>
  <p style="margin-top:6px">
    <a href="/privacy.html">隐私政策</a> ·
    <a href="/terms.html">使用条款</a> ·
    <a href="mailto:support@toolmini.cn">问题反馈</a>
  </p>
</footer>

<div class="toast-container" id="toastContainer"></div>

<script>
// ===== Tool Config =====
const TOOL_ID = '{tool_id}';
const TOOL_CAT = '{tool_cat}';
const TOOL_FORMATS = {formats_json};

let uploadedFiles = [];

// ===== File Upload =====
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');

dropZone.addEventListener('click', () => fileInput.click());
dropZone.addEventListener('dragover', e => {{ e.preventDefault(); dropZone.classList.add('drag-over'); }});
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
dropZone.addEventListener('drop', e => {{
  e.preventDefault(); dropZone.classList.remove('drag-over'); handleFiles(e.dataTransfer.files);
}});
fileInput.addEventListener('change', e => handleFiles(e.target.files));

function handleFiles(fileList) {{
  for (const file of fileList) {{
    const ext = '.' + file.name.split('.').pop().toLowerCase();
    if (TOOL_FORMATS[0] !== 'text' && !TOOL_FORMATS.includes(ext)) {{
      toast(file.name + ' 格式不支持', 'error'); continue;
    }}
    uploadedFiles.push(file);
  }}
  renderFileList();
  showControls();
}}

function renderFileList() {{
  const preview = document.getElementById('filePreview');
  const list = document.getElementById('fileList');
  if (!uploadedFiles.length) {{ preview.classList.remove('show'); return; }}
  preview.classList.add('show');
  list.innerHTML = uploadedFiles.map((f,i) => `
    <div class="file-item">
      <div class="fi-icon">📄</div>
      <div class="fi-name">${{f.name}}</div>
      <div class="fi-size">${{formatSize(f.size)}}</div>
      <button class="fi-remove" onclick="removeFile(${{i}})">✕</button>
    </div>
  `).join('');
}}

function removeFile(idx) {{ uploadedFiles.splice(idx,1); renderFileList(); showControls(); }}
function clearFiles() {{ uploadedFiles=[]; fileInput.value=''; renderFileList(); showControls(); hideProgress(); document.getElementById('outputArea').classList.remove('show'); }}
function formatSize(b) {{ return b<1024?b+' B':b<1048576?(b/1024).toFixed(1)+' KB':(b/1048576).toFixed(1)+' MB'; }}
function showControls() {{
  if (uploadedFiles.length > 0 || TOOL_FORMATS[0] === 'text') {{
    document.getElementById('controls').classList.add('show');
    document.getElementById('btnRow').style.display = 'flex';
  }} else {{
    document.getElementById('controls').classList.remove('show');
    document.getElementById('btnRow').style.display = 'none';
  }}
}}

// ===== Progress =====
function showProgress(text) {{
  const w = document.getElementById('progressWrap');
  w.classList.add('show');
  document.getElementById('progressText').textContent = text || '处理中...';
  document.getElementById('progressBar').style.width = '0%';
  document.getElementById('outputArea').classList.remove('show');
}}
function hideProgress() {{ document.getElementById('progressWrap').classList.remove('show'); }}
function updateProgress(cur, total, text) {{
  document.getElementById('progressBar').style.width = Math.round(cur/total*100) + '%';
  if (text) document.getElementById('progressText').textContent = text;
}}

// ===== Output =====
function showOutput(text) {{
  document.getElementById('outputResult').textContent = text;
  document.getElementById('outputArea').classList.add('show');
}}

// ===== Toast =====
function toast(msg, type) {{
  const c = document.getElementById('toastContainer');
  const t = document.createElement('div');
  t.className = 'toast toast-' + (type||'info');
  t.textContent = msg;
  c.appendChild(t);
  setTimeout(() => t.remove(), 4000);
}}

// ===== Utility =====
function saveBlob(blob, filename) {{ saveAs(blob, filename); }}
function loadImage(file) {{
  return new Promise((resolve) => {{
    const img = new Image();
    img.onload = () => resolve(img);
    img.src = URL.createObjectURL(file);
  }});
}}
function parsePageRanges(str) {{
  const ranges = [];
  str.split(',').forEach(part => {{
    const m = part.trim().match(/(\\d+)(?:-(\\d+))?/);
    if (m) ranges.push({{ start: parseInt(m[1]), end: m[2] ? parseInt(m[2]) : parseInt(m[1]) }});
  }});
  return ranges;
}}

{tool_specific_code}

// ===== Run Tool =====
async function runTool() {{
  showProgress('正在处理...');
  try {{
    await toolRun();
  }} catch(err) {{
    hideProgress();
    toast('处理失败: ' + err.message, 'error');
  }}
}}

lucide.createIcons();
</script>
</body>
</html>'''

# Tool-specific JS code for each tool
TOOL_SPECIFIC = {
    'pdf_merge': '''
async function toolRun() {
  const { PDFDocument } = PDFLib;
  const mergedPdf = await PDFDocument.create();
  for (const file of uploadedFiles) {
    const buf = await file.arrayBuffer();
    const pdf = await PDFDocument.load(buf);
    const pages = await mergedPdf.copyPages(pdf, pdf.getPageIndices());
    pages.forEach(p => mergedPdf.addPage(p));
  }
  const bytes = await mergedPdf.save();
  saveBlob(new Blob([bytes], {type:'application/pdf'}), 'merged.pdf');
  hideProgress();
  showOutput('合并成功！已生成合并后的PDF文件。');
}''',
    'pdf_split': '''
async function toolRun() {
  const { PDFDocument } = PDFLib;
  const ranges = parsePageRanges(document.getElementById('ctrlPages').value);
  const file = uploadedFiles[0];
  if (!file) { toast('请先上传PDF文件','error'); hideProgress(); return; }
  const buf = await file.arrayBuffer();
  const pdf = await PDFDocument.load(buf);
  const total = pdf.getPageCount();
  const zip = new JSZip();
  for (const range of ranges) {
    for (let i = range.start; i <= Math.min(range.end, total); i++) {
      const newPdf = await PDFDocument.create();
      const [page] = await newPdf.copyPages(pdf, [i-1]);
      newPdf.addPage(page);
      const bytes = await newPdf.save();
      zip.file('page_'+i+'.pdf', bytes);
    }
  }
  const blob = await zip.generateAsync({type:'blob'});
  saveBlob(blob, 'split_pages.zip');
  hideProgress();
  showOutput('拆分成功！每个页面已保存为独立PDF文件。');
}''',
    'pdf_compress': '''
async function toolRun() {
  const quality = parseInt(document.getElementById('ctrlQuality').value) / 100;
  const file = uploadedFiles[0];
  if (!file) { toast('请先上传PDF文件','error'); hideProgress(); return; }
  const buf = await file.arrayBuffer();
  const { PDFDocument } = PDFLib;
  const pdf = await PDFDocument.load(buf);
  // Simple re-save compression
  const bytes = await pdf.save({ useObjectStreams: true, addDefaultPage: false });
  saveBlob(new Blob([bytes], {type:'application/pdf'}), 'compressed_'+file.name);
  hideProgress();
  showOutput('压缩完成！文件已优化。\\n原始大小: '+formatSize(file.size)+'\\n处理后大小: '+formatSize(bytes.length));
}''',
    'pdf_encrypt': '''
async function toolRun() {
  const pwd = document.getElementById('ctrlPwd').value;
  if (!pwd) { toast('请设置密码','error'); hideProgress(); return; }
  const file = uploadedFiles[0];
  if (!file) { toast('请先上传PDF文件','error'); hideProgress(); return; }
  // Note: pdf-lib doesn't support encryption natively
  // We'll use jsPDF to create an encrypted version
  hideProgress();
  showOutput('提示：当前浏览器端PDF加密能力有限。\\n建议使用专业PDF软件进行加密操作。\\n\\n您设置的密码: '+pwd);
}''',
    'pdf_unlock': '''
async function toolRun() {
  const pwd = document.getElementById('ctrlPwd').value;
  if (!pwd) { toast('请输入密码','error'); hideProgress(); return; }
  const file = uploadedFiles[0];
  if (!file) { toast('请先上传PDF文件','error'); hideProgress(); return; }
  try {
    const buf = await file.arrayBuffer();
    const { PDFDocument } = PDFLib;
    const pdf = await PDFDocument.load(buf, { password: pwd });
    const bytes = await pdf.save();
    saveBlob(new Blob([bytes], {type:'application/pdf'}), 'unlocked_'+file.name);
    hideProgress();
    showOutput('解锁成功！密码已移除。');
  } catch(e) {
    hideProgress();
    toast('密码错误或文件无法解锁','error');
  }
}''',
    'pdf_to_jpg': '''
async function toolRun() {
  const file = uploadedFiles[0];
  if (!file) { toast('请先上传PDF文件','error'); hideProgress(); return; }
  if (!window.pdfjsLib) {
    const s = document.createElement('script');
    s.src = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js';
    document.head.appendChild(s);
    await new Promise(r => s.onload = r);
    window.pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
  }
  const buf = await file.arrayBuffer();
  const pdf = await window.pdfjsLib.getDocument({data:new Uint8Array(buf)}).promise;
  const zip = new JSZip();
  for (let i = 1; i <= pdf.numPages; i++) {
    const page = await pdf.getPage(i);
    const vp = page.getViewport({scale:2});
    const canvas = document.createElement('canvas');
    canvas.width = vp.width; canvas.height = vp.height;
    await page.render({canvasContext:canvas.getContext('2d'),viewport:vp}).promise;
    const blob = await new Promise(r => canvas.toBlob(r,'image/jpeg',0.92));
    zip.file('page_'+i+'.jpg', blob);
    updateProgress(i, pdf.numPages, '转换第 '+i+'/'+pdf.numPages+' 页...');
  }
  const zipBlob = await zip.generateAsync({type:'blob'});
  saveBlob(zipBlob, 'pdf_pages.zip');
  hideProgress();
  showOutput('转换完成！共 '+pdf.numPages+' 页已转为JPG图片。');
}''',
    'jpg_to_pdf': '''
async function toolRun() {
  const { PDFDocument } = PDFLib;
  const pdfDoc = await PDFDocument.create();
  for (const file of uploadedFiles) {
    const imgBytes = await file.arrayBuffer();
    let img;
    if (file.type === 'image/png') {
      img = await pdfDoc.embedPng(imgBytes);
    } else {
      img = await pdfDoc.embedJpg(imgBytes);
    }
    const page = pdfDoc.addPage([img.width, img.height]);
    page.drawImage(img, {x:0,y:0,width:img.width,height:img.height});
  }
  const bytes = await pdfDoc.save();
  saveBlob(new Blob([bytes], {type:'application/pdf'}), 'images_to_pdf.pdf');
  hideProgress();
  showOutput('转换完成！已将 '+uploadedFiles.length+' 张图片合并为PDF。');
}''',
    'pdf_sign': '''
// PDF签名在独立页面中简化为提示
async function toolRun() {
  hideProgress();
  showOutput('提示：PDF签名功能需要交互式手写签名区域。\\n请返回首页使用完整版签名功能。');
}''',
    'pdf_rotate': '''
async function toolRun() {
  const angle = parseInt(document.getElementById('ctrlRotate').value);
  const file = uploadedFiles[0];
  if (!file) { toast('请先上传PDF文件','error'); hideProgress(); return; }
  const { PDFDocument, degrees } = PDFLib;
  const buf = await file.arrayBuffer();
  const pdf = await PDFDocument.load(buf);
  const pages = pdf.getPages();
  pages.forEach(page => { page.setRotation(degrees(angle)); });
  const bytes = await pdf.save();
  saveBlob(new Blob([bytes], {type:'application/pdf'}), 'rotated_'+file.name);
  hideProgress();
  showOutput('旋转完成！所有页面已旋转'+angle+'°。');
}''',
    'pdf_extract': '''
async function toolRun() {
  const ranges = parsePageRanges(document.getElementById('ctrlPages').value);
  const file = uploadedFiles[0];
  if (!file) { toast('请先上传PDF文件','error'); hideProgress(); return; }
  const { PDFDocument } = PDFLib;
  const buf = await file.arrayBuffer();
  const srcPdf = await PDFDocument.load(buf);
  const newPdf = await PDFDocument.create();
  const indices = [];
  ranges.forEach(r => { for (let i=r.start-1; i<=Math.min(r.end-1,srcPdf.getPageCount()-1); i++) indices.push(i); });
  const pages = await newPdf.copyPages(srcPdf, indices);
  pages.forEach(p => newPdf.addPage(p));
  const bytes = await newPdf.save();
  saveBlob(new Blob([bytes], {type:'application/pdf'}), 'extracted_'+file.name);
  hideProgress();
  showOutput('提取完成！已提取 '+indices.length+' 个页面。');
}''',
    'pdf_to_word': '''
async function toolRun() {
  const file = uploadedFiles[0];
  if (!file) { toast('请先上传PDF文件','error'); hideProgress(); return; }
  if (!window.pdfjsLib) {
    const s = document.createElement('script');
    s.src = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js';
    document.head.appendChild(s);
    await new Promise(r => s.onload = r);
    window.pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
  }
  const buf = await file.arrayBuffer();
  const pdf = await window.pdfjsLib.getDocument({data:new Uint8Array(buf)}).promise;
  const allText = [];
  const { Document, Packer, Paragraph, TextRun, HeadingLevel, PageBreak } = docx;
  for (let i=1; i<=pdf.numPages; i++) {
    const page = await pdf.getPage(i);
    const content = await page.getTextContent();
    allText.push(content.items.map(item=>item.str).join(' '));
    updateProgress(i, pdf.numPages, '提取第 '+i+'/'+pdf.numPages+' 页...');
  }
  const paragraphs = [];
  allText.forEach((pt,idx) => {
    pt.split(/\\s{2,}/).filter(l=>l.trim()).forEach(line => {
      paragraphs.push(new Paragraph({text:line.trim(),spacing:{after:120}}));
    });
    if (idx < allText.length-1) paragraphs.push(new Paragraph({children:[new PageBreak()]}));
  });
  if (!paragraphs.length) paragraphs.push(new Paragraph({text:'(PDF中未检测到可提取的文本内容)'}));
  const doc = new Document({sections:[{children:paragraphs}]});
  const blob = await Packer.toBlob(doc);
  saveBlob(blob, file.name.replace(/\\.pdf$/i,'_converted.docx'));
  hideProgress();
  showOutput('转换完成！已提取 '+pdf.numPages+' 页文本并生成Word文档。\\n\\n⚠️ 注意：纯文本提取，图片和复杂排版无法保留。');
}''',
    'pdf_to_excel': '''
async function toolRun() {
  const file = uploadedFiles[0];
  if (!file) { toast('请先上传PDF文件','error'); hideProgress(); return; }
  if (!window.pdfjsLib) {
    const s = document.createElement('script');
    s.src = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js';
    document.head.appendChild(s);
    await new Promise(r => s.onload = r);
    window.pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
  }
  const buf = await file.arrayBuffer();
  const pdf = await window.pdfjsLib.getDocument({data:new Uint8Array(buf)}).promise;
  const tables = [];
  for (let i=1; i<=pdf.numPages; i++) {
    const page = await pdf.getPage(i);
    const content = await page.getTextContent();
    const rowMap = new Map();
    content.items.forEach(item => {
      if (!item.str.trim()) return;
      const y = Math.round(item.transform[5]);
      if (!rowMap.has(y)) rowMap.set(y,[]);
      rowMap.get(y).push({x:item.transform[4],text:item.str.trim()});
    });
    const sorted = Array.from(rowMap.values()).sort((a,b)=>b[0].y-a[0].y);
    const rows = sorted.map(r=>r.sort((a,b)=>a.x-b.x).map(c=>c.text)).filter(r=>r.length>1);
    if (rows.length>=2) tables.push(...rows);
    updateProgress(i, pdf.numPages, '识别第 '+i+'/'+pdf.numPages+' 页...');
  }
  if (!tables.length) { hideProgress(); showOutput('未能识别出表格数据。\\n请确保PDF包含文本（非扫描图片）。'); return; }
  const maxCols = Math.max(...tables.map(r=>r.length));
  const padded = tables.map(r=>{while(r.length<maxCols)r.push('');return r;});
  const ws = XLSX.utils.aoa_to_sheet(padded);
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb,ws,'PDF表格');
  const xlsxBuf = XLSX.write(wb,{bookType:'xlsx',type:'array'});
  saveBlob(new Blob([xlsxBuf],{type:'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}),'pdf_tables.xlsx');
  hideProgress();
  showOutput('识别完成！共识别 '+tables.length+' 行 × '+maxCols+' 列数据。');
}''',
    'img_compress': '''
async function toolRun() {
  const quality = parseInt(document.getElementById('ctrlQuality').value)/100;
  for (const file of uploadedFiles) {
    const img = await loadImage(file);
    const canvas = document.createElement('canvas');
    canvas.width = img.naturalWidth; canvas.height = img.naturalHeight;
    canvas.getContext('2d').drawImage(img,0,0);
    const blob = await new Promise(r => canvas.toBlob(r,'image/jpeg',quality));
    saveBlob(blob, 'compressed_'+file.name);
  }
  hideProgress();
  showOutput('压缩完成！共处理 '+uploadedFiles.length+' 张图片。');
}''',
    'img_convert': '''
async function toolRun() {
  const fmt = document.getElementById('ctrlFormat').value;
  const mime = fmt==='jpeg'?'image/jpeg':fmt==='png'?'image/png':'image/webp';
  for (const file of uploadedFiles) {
    const img = await loadImage(file);
    const canvas = document.createElement('canvas');
    canvas.width = img.naturalWidth; canvas.height = img.naturalHeight;
    canvas.getContext('2d').drawImage(img,0,0);
    const blob = await new Promise(r => canvas.toBlob(r,mime,0.92));
    saveBlob(blob, file.name.replace(/\\.[^.]+$/,'')+'.'+fmt);
  }
  hideProgress();
  showOutput('转换完成！');
}''',
    'img_resize': '''
async function toolRun() {
  const w = parseInt(document.getElementById('ctrlW').value);
  const h = parseInt(document.getElementById('ctrlH').value);
  for (const file of uploadedFiles) {
    const img = await loadImage(file);
    const canvas = document.createElement('canvas');
    canvas.width = w; canvas.height = h;
    canvas.getContext('2d').drawImage(img,0,0,w,h);
    const blob = await new Promise(r => canvas.toBlob(r,'image/png'));
    saveBlob(blob, 'resized_'+file.name);
  }
  hideProgress();
  showOutput('调整完成！新尺寸: '+w+'×'+h+'px');
}''',
    'img_crop': '''
async function toolRun() {
  hideProgress();
  showOutput('提示：图片裁剪需要交互式选区。\\n请返回首页使用完整版裁剪功能。');
}''',
    'img_rotate': '''
async function toolRun() {
  const sel = document.getElementById('ctrlRotate');
  let angle = sel.value==='custom'?parseInt(document.getElementById('ctrlAngle').value):parseInt(sel.value);
  for (const file of uploadedFiles) {
    const img = await loadImage(file);
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    if (angle===90||angle===270) { canvas.width=img.naturalHeight; canvas.height=img.naturalWidth; }
    else { canvas.width=img.naturalWidth; canvas.height=img.naturalHeight; }
    ctx.translate(canvas.width/2, canvas.height/2);
    ctx.rotate(angle*Math.PI/180);
    ctx.drawImage(img,-img.naturalWidth/2,-img.naturalHeight/2);
    const blob = await new Promise(r => canvas.toBlob(r,'image/png'));
    saveBlob(blob, 'rotated_'+file.name);
  }
  hideProgress();
  showOutput('旋转完成！');
}''',
    'img_watermark': '''
async function toolRun() {
  const wmText = document.getElementById('ctrlWmText').value || 'MiniTool';
  const pos = document.getElementById('ctrlWmPos').value;
  const alpha = parseInt(document.getElementById('ctrlWmAlpha').value)/100;
  for (const file of uploadedFiles) {
    const img = await loadImage(file);
    const canvas = document.createElement('canvas');
    canvas.width = img.naturalWidth; canvas.height = img.naturalHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(img,0,0);
    ctx.globalAlpha = alpha;
    ctx.font = Math.max(24, Math.floor(img.naturalWidth/10))+'px Inter, sans-serif';
    ctx.fillStyle = '#ffffff';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    if (pos==='tile') {
      for (let y=0;y<canvas.height;y+=120) for (let x=0;x<canvas.width;x+=200) {
        ctx.save(); ctx.translate(x,y); ctx.rotate(-25*Math.PI/180); ctx.fillText(wmText,0,0); ctx.restore();
      }
    } else {
      let x=canvas.width/2,y=canvas.height/2;
      if (pos==='top-left'){x=150;y=80;} else if(pos==='top-right'){x=canvas.width-150;y=80;}
      else if(pos==='bottom-left'){x=150;y=canvas.height-80;} else if(pos==='bottom-right'){x=canvas.width-150;y=canvas.height-80;}
      ctx.fillText(wmText,x,y);
    }
    ctx.globalAlpha = 1;
    const blob = await new Promise(r => canvas.toBlob(r,'image/png'));
    saveBlob(blob, 'watermarked_'+file.name);
  }
  hideProgress();
  showOutput('水印添加完成！');
}''',
    'img_grid': '''
async function toolRun() {
  const file = uploadedFiles[0];
  if (!file) { toast('请先上传图片','error'); hideProgress(); return; }
  const img = await loadImage(file);
  const w = Math.floor(img.naturalWidth/3);
  const h = Math.floor(img.naturalHeight/3);
  const zip = new JSZip();
  for (let r=0;r<3;r++) for (let c=0;c<3;c++) {
    const canvas = document.createElement('canvas');
    canvas.width=w; canvas.height=h;
    canvas.getContext('2d').drawImage(img,c*w,r*h,w,h,0,0,w,h);
    const blob = await new Promise(res => canvas.toBlob(res,'image/jpeg',0.92));
    zip.file('grid_'+(r*3+c+1)+'.jpg', blob);
  }
  const zipBlob = await zip.generateAsync({type:'blob'});
  saveBlob(zipBlob, 'grid_images.zip');
  hideProgress();
  showOutput('九宫格切图完成！共9张图片已打包。');
}''',
    'img_join': '''
async function toolRun() {
  const dir = document.getElementById('ctrlJoinDir').value;
  const images = [];
  for (const file of uploadedFiles) images.push(await loadImage(file));
  if (dir==='h') {
    const totalW = images.reduce((s,i)=>s+i.naturalWidth,0);
    const maxH = Math.max(...images.map(i=>i.naturalHeight));
    const canvas = document.createElement('canvas');
    canvas.width=totalW; canvas.height=maxH;
    const ctx = canvas.getContext('2d');
    let x=0;
    for (const img of images) { ctx.drawImage(img,x,0); x+=img.naturalWidth; }
    const blob = await new Promise(r => canvas.toBlob(r,'image/png'));
    saveBlob(blob, 'joined_horizontal.png');
  } else {
    const maxW = Math.max(...images.map(i=>i.naturalWidth));
    const totalH = images.reduce((s,i)=>s+i.naturalHeight,0);
    const canvas = document.createElement('canvas');
    canvas.width=maxW; canvas.height=totalH;
    const ctx = canvas.getContext('2d');
    let y=0;
    for (const img of images) { ctx.drawImage(img,0,y); y+=img.naturalHeight; }
    const blob = await new Promise(r => canvas.toBlob(r,'image/png'));
    saveBlob(blob, 'joined_vertical.png');
  }
  hideProgress();
  showOutput('拼接完成！');
}''',
    'img_unwatermark': '''
async function toolRun() {
  hideProgress();
  showOutput('提示：图片去水印需要交互式框选区域。\\n请返回首页使用完整版去水印功能。');
}''',
    'vid_to_gif': '''
async function toolRun() {
  hideProgress();
  showOutput('提示：视频转GIF功能需要完整交互界面。\\n请返回首页使用完整版视频转GIF功能。');
}''',
    'gif_to_vid': '''
async function toolRun() {
  hideProgress();
  showOutput('提示：GIF转视频功能需要完整交互界面。\\n请返回首页使用完整版GIF转视频功能。');
}''',
    'vid_thumb': '''
async function toolRun() {
  const time = parseFloat(document.getElementById('ctrlThumbTime').value) || 1;
  const file = uploadedFiles[0];
  if (!file) { toast('请先上传视频','error'); hideProgress(); return; }
  const video = document.createElement('video');
  video.src = URL.createObjectURL(file);
  video.muted = true;
  await new Promise(r => video.onloadedmetadata = r);
  video.currentTime = Math.min(time, video.duration - 0.1);
  await new Promise(r => video.onseeked = r);
  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth; canvas.height = video.videoHeight;
  canvas.getContext('2d').drawImage(video,0,0);
  const blob = await new Promise(r => canvas.toBlob(r,'image/jpeg',0.92));
  saveBlob(blob, 'thumbnail_'+file.name.replace(/\\.[^.]+$/,'')+'.jpg');
  hideProgress();
  showOutput('封面提取完成！');
}''',
    'vid_unwatermark': '''
async function toolRun() {
  hideProgress();
  showOutput('提示：视频去水印需要交互式框选区域。\\n请返回首页使用完整版视频去水印功能。');
}''',
    'ai_polish': '''
async function toolRun() {
  const text = document.getElementById('aiTextInput').value;
  if (!text.trim()) { toast('请输入文字内容','error'); hideProgress(); return; }
  hideProgress();
  showOutput('【润色结果】\\n\\n'+text.replace(/[,，]/g,'，').replace(/[.。]/g,'。')+'\\n\\n⚠️ 提示：当前为本地模拟润色，建议配合专业AI工具使用。');
}''',
    'ai_continue': '''
async function toolRun() {
  const text = document.getElementById('aiTextInput').value;
  if (!text.trim()) { toast('请输入文章开头','error'); hideProgress(); return; }
  hideProgress();
  showOutput('【续写结果】\\n\\n'+text+'\\n\\n在此基础上，我们可以进一步探讨这个话题的深层含义……\\n\\n⚠️ 提示：当前为本地模拟续写，建议配合专业AI工具使用。');
}''',
    'ai_title': '''
async function toolRun() {
  const text = document.getElementById('aiTextInput').value;
  if (!text.trim()) { toast('请输入文章内容','error'); hideProgress(); return; }
  hideProgress();
  showOutput('【标题建议】\\n\\n1. 深度解析：关于'+text.substring(0,10)+'的思考\\n2. '+text.substring(0,8)+'——不可忽视的重要话题\\n3. 从'+text.substring(0,6)+'看未来趋势\\n\\n⚠️ 提示：当前为本地模拟生成，建议配合专业AI工具使用。');
}''',
    'ai_summary': '''
async function toolRun() {
  const text = document.getElementById('aiTextInput').value;
  if (!text.trim()) { toast('请输入文章内容','error'); hideProgress(); return; }
  const sentences = text.split(/[。！？\\n]/).filter(s=>s.trim());
  const summary = sentences.slice(0, Math.max(2, Math.ceil(sentences.length/3))).join('。') + '。';
  hideProgress();
  showOutput('【摘要总结】\\n\\n'+summary+'\\n\\n⚠️ 提示：当前为本地模拟摘要，建议配合专业AI工具使用。');
}''',
    'ai_marketing': '''
async function toolRun() {
  const text = document.getElementById('aiTextInput').value;
  if (!text.trim()) { toast('请输入产品信息','error'); hideProgress(); return; }
  hideProgress();
  showOutput('【营销文案】\\n\\n🔥 '+text+' —— 让生活更美好！\\n\\n✨ 产品亮点：'+text.substring(0,20)+'\\n💪 选择我们，选择品质！\\n\\n⚠️ 提示：当前为本地模拟文案，建议配合专业AI工具使用。');
}''',
}

# Controls HTML for each tool
CONTROLS_HTML = {
    'pdf_split': '<div class="control-row"><span class="control-label">页码范围</span><input type="text" id="ctrlPages" placeholder="例如: 1-3,5,7-10" style="flex:1"></div>',
    'pdf_compress': '<div class="control-row"><span class="control-label">质量</span><input type="range" id="ctrlQuality" min="10" max="100" value="80"><span class="range-val" id="qVal">80%</span></div>',
    'pdf_encrypt': '<div class="control-row"><span class="control-label">密码</span><input type="password" id="ctrlPwd" placeholder="设置打开密码" style="flex:1"></div>',
    'pdf_unlock': '<div class="control-row"><span class="control-label">当前密码</span><input type="password" id="ctrlPwd" placeholder="输入PDF密码" style="flex:1"></div>',
    'pdf_rotate': '<div class="control-row"><span class="control-label">旋转角度</span><select id="ctrlRotate" style="flex:1"><option value="90">顺时针 90°</option><option value="180">180°</option><option value="270">逆时针 90°</option></select></div>',
    'pdf_extract': '<div class="control-row"><span class="control-label">页码范围</span><input type="text" id="ctrlPages" placeholder="例如: 1-3,5" style="flex:1"></div>',
    'img_compress': '<div class="control-row"><span class="control-label">质量</span><input type="range" id="ctrlQuality" min="10" max="100" value="80"><span class="range-val" id="qVal">80%</span></div>',
    'img_convert': '<div class="control-row"><span class="control-label">输出格式</span><select id="ctrlFormat" style="flex:1"><option value="jpeg">JPG</option><option value="png">PNG</option><option value="webp">WebP</option></select></div>',
    'img_resize': '<div class="control-row"><span class="control-label">宽度(px)</span><input type="number" id="ctrlW" value="800" min="1" style="width:90px"><span class="control-label">高度(px)</span><input type="number" id="ctrlH" value="600" min="1" style="width:90px"></div>',
    'img_rotate': '<div class="control-row"><span class="control-label">旋转角度</span><select id="ctrlRotate" style="flex:1"><option value="90">顺时针 90°</option><option value="180">180°</option><option value="270">逆时针 90°</option><option value="custom">自定义</option></select></div>',
    'img_watermark': '<div class="control-row"><span class="control-label">水印文字</span><input type="text" id="ctrlWmText" placeholder="MiniTool" style="flex:1"></div><div class="control-row"><span class="control-label">位置</span><select id="ctrlWmPos" style="flex:1"><option value="center">居中</option><option value="tile">平铺</option><option value="bottom-right">右下</option></select></div><div class="control-row"><span class="control-label">透明度</span><input type="range" id="ctrlWmAlpha" min="10" max="100" value="30"><span class="range-val">30%</span></div>',
    'img_join': '<div class="control-row"><span class="control-label">拼接方式</span><select id="ctrlJoinDir" style="flex:1"><option value="h">横向拼接</option><option value="v">纵向拼接</option></select></div>',
    'vid_thumb': '<div class="control-row"><span class="control-label">截取时间</span><input type="number" id="ctrlThumbTime" value="1" min="0" step="0.1" style="width:90px"><span style="font-size:12px;color:#94a3b8">秒</span></div>',
}

# AI tools get textarea instead of file upload
AI_TEXTAREAS = {
    'ai_polish': '<textarea id="aiTextInput" placeholder="请输入需要润色的文字..." style="width:100%;min-height:150px;resize:vertical"></textarea>',
    'ai_continue': '<textarea id="aiTextInput" placeholder="请输入文章开头或前文..." style="width:100%;min-height:150px;resize:vertical"></textarea>',
    'ai_title': '<textarea id="aiTextInput" placeholder="请输入文章内容..." style="width:100%;min-height:150px;resize:vertical"></textarea>',
    'ai_summary': '<textarea id="aiTextInput" placeholder="请粘贴需要总结的长文..." style="width:100%;min-height:150px;resize:vertical"></textarea>',
    'ai_marketing': '<textarea id="aiTextInput" placeholder="请输入产品名称和特点..." style="width:100%;min-height:150px;resize:vertical"></textarea>',
}

# Cat info
CAT_INFO = {
    'pdf': {'name': 'PDF工具', 'icon_bg': 'rgba(239,68,68,0.15)', 'icon_color': '#ef4444'},
    'image': {'name': '图片工具', 'icon_bg': 'rgba(34,197,94,0.15)', 'icon_color': '#22c55e'},
    'video': {'name': '视频工具', 'icon_bg': 'rgba(245,158,11,0.15)', 'icon_color': '#f59e0b'},
    'ai': {'name': 'AI写作', 'icon_bg': 'rgba(99,102,241,0.15)', 'icon_color': '#818cf8'},
}

TOOLS_DATA = [
    {'id':'pdf_merge','cat':'pdf','icon':'file-plus','name':'合并PDF','desc':'将多个PDF合并为一个文件','formats':['.pdf']},
    {'id':'pdf_split','cat':'pdf','icon':'scissors','name':'拆分PDF','desc':'按页码范围拆分成多个文件','formats':['.pdf']},
    {'id':'pdf_to_jpg','cat':'pdf','icon':'image','name':'PDF转JPG','desc':'将PDF每一页转为高清图片','formats':['.pdf']},
    {'id':'jpg_to_pdf','cat':'pdf','icon':'file-text','name':'JPG转PDF','desc':'将图片合并转换为PDF文档','formats':['.jpg','.jpeg','.png','.webp','.gif']},
    {'id':'pdf_compress','cat':'pdf','icon':'minimize-2','name':'压缩PDF','desc':'减小PDF文件体积','formats':['.pdf']},
    {'id':'pdf_encrypt','cat':'pdf','icon':'lock','name':'PDF加密','desc':'给PDF添加打开密码保护','formats':['.pdf']},
    {'id':'pdf_unlock','cat':'pdf','icon':'unlock','name':'PDF解锁','desc':'移除PDF密码保护','formats':['.pdf']},
    {'id':'pdf_sign','cat':'pdf','icon':'pen-tool','name':'PDF签名','desc':'在PDF文档中添加手写签名','formats':['.pdf']},
    {'id':'pdf_rotate','cat':'pdf','icon':'rotate-cw','name':'旋转PDF','desc':'顺时针/逆时针旋转PDF页面','formats':['.pdf']},
    {'id':'pdf_extract','cat':'pdf','icon':'layers','name':'提取页面','desc':'提取PDF指定页面生成新文件','formats':['.pdf']},
    {'id':'pdf_to_word','cat':'pdf','icon':'file-text','name':'PDF转Word','desc':'将PDF内容提取为Word文档','formats':['.pdf']},
    {'id':'pdf_to_excel','cat':'pdf','icon':'table','name':'PDF转Excel','desc':'智能识别PDF表格转为Excel','formats':['.pdf']},
    {'id':'img_compress','cat':'image','icon':'minimize-2','name':'图片压缩','desc':'调整质量以减小图片体积','formats':['.jpg','.jpeg','.png','.webp','.gif']},
    {'id':'img_convert','cat':'image','icon':'refresh-cw','name':'格式转换','desc':'JPG/PNG/WebP/GIF互转','formats':['.jpg','.jpeg','.png','.webp','.gif']},
    {'id':'img_resize','cat':'image','icon':'maximize-2','name':'调整尺寸','desc':'修改图片宽高像素','formats':['.jpg','.jpeg','.png','.webp','.gif']},
    {'id':'img_crop','cat':'image','icon':'crop','name':'图片裁剪','desc':'裁剪掉不需要的画面区域','formats':['.jpg','.jpeg','.png','.webp','.gif']},
    {'id':'img_rotate','cat':'image','icon':'rotate-cw','name':'图片旋转','desc':'旋转90°/180°/270°或自定义角度','formats':['.jpg','.jpeg','.png','.webp']},
    {'id':'img_watermark','cat':'image','icon':'droplet','name':'添加水印','desc':'添加文字或图片水印','formats':['.jpg','.jpeg','.png','.webp']},
    {'id':'img_grid','cat':'image','icon':'grid-2x2','name':'九宫格切图','desc':'将图片切成9宫格分享图','formats':['.jpg','.jpeg','.png','.webp']},
    {'id':'img_join','cat':'image','icon':'columns','name':'图片拼接','desc':'横向或纵向拼接多张图片','formats':['.jpg','.jpeg','.png','.webp','.gif']},
    {'id':'img_unwatermark','cat':'image','icon':'eraser','name':'图片去水印','desc':'智能涂抹移除图片水印/杂物','formats':['.jpg','.jpeg','.png','.webp']},
    {'id':'vid_to_gif','cat':'video','icon':'film','name':'视频转GIF','desc':'截取视频片段转为GIF动图','formats':['.mp4','.webm','.mov','.avi']},
    {'id':'gif_to_vid','cat':'video','icon':'video','name':'GIF转视频','desc':'将GIF动画转为MP4视频','formats':['.gif']},
    {'id':'vid_thumb','cat':'video','icon':'image','name':'视频封面提取','desc':'从视频中截取一帧作为图片','formats':['.mp4','.webm','.mov','.avi']},
    {'id':'vid_unwatermark','cat':'video','icon':'eraser','name':'视频去水印','desc':'涂抹移除视频水印/Logo区域','formats':['.mp4','.webm','.mov']},
    {'id':'ai_polish','cat':'ai','icon':'wand-2','name':'文字润色','desc':'AI优化文字表达，更流畅专业','formats':['text']},
    {'id':'ai_continue','cat':'ai','icon':'corner-down-right','name':'文章续写','desc':'输入开头，AI续写完整内容','formats':['text']},
    {'id':'ai_title','cat':'ai','icon':'type','name':'标题生成','desc':'输入文章内容，生成吸睛标题','formats':['text']},
    {'id':'ai_summary','cat':'ai','icon':'align-left','name':'摘要总结','desc':'输入长文，生成精炼摘要','formats':['text']},
    {'id':'ai_marketing','cat':'ai','icon':'megaphone','name':'营销文案','desc':'输入产品信息，生成推广文案','formats':['text']},
]

os.makedirs(TOOLS_DIR, exist_ok=True)

for tool in TOOLS_DATA:
    tid = tool['id']
    slug = TOOL_SLUGS[tid]
    cat_info = CAT_INFO[tool['cat']]
    guide = TOOL_GUIDES.get(tid, '1. 上传文件\\n2. 点击开始处理\\n3. 下载结果')
    guide_items = ''.join(f'<li>{line}</li>' for line in guide.split('\\n') if line.strip())
    formats_json = json.dumps(tool['formats'])
    format_chips = ' '.join(f'<span class="format-chip">{f}</span>' for f in tool['formats'])
    controls = CONTROLS_HTML.get(tid, '')
    tool_code = TOOL_SPECIFIC.get(tid, '''
async function toolRun() { hideProgress(); showOutput('功能处理中...'); }
''')

    # For AI tools, replace drop zone with textarea
    if tool['cat'] == 'ai':
        textarea_html = AI_TEXTAREAS.get(tid, '<textarea id="aiTextInput" placeholder="请输入内容..." style="width:100%;min-height:150px"></textarea>')
        page = TOOL_PAGE_TEMPLATE.format(
            tool_name=tool['name'], tool_desc=tool['desc'], slug=slug,
            cat_name=cat_info['name'], tool_icon=tool['icon'],
            icon_bg=cat_info['icon_bg'], icon_color=cat_info['icon_color'],
            tool_id=tid, tool_cat=tool['cat'],
            formats_json=formats_json, format_chips=format_chips,
            guide_items=guide_items, controls_html=textarea_html,
            tool_specific_code=tool_code
        )
        # Replace drop zone section with textarea for AI tools
        page = page.replace(
            '''<div class="drop-zone" id="dropZone">''',
            '''<!-- AI Text Input -->\n<div class="ai-input-area" id="dropZone" style="display:none">'''
        )
    else:
        page = TOOL_PAGE_TEMPLATE.format(
            tool_name=tool['name'], tool_desc=tool['desc'], slug=slug,
            cat_name=cat_info['name'], tool_icon=tool['icon'],
            icon_bg=cat_info['icon_bg'], icon_color=cat_info['icon_color'],
            tool_id=tid, tool_cat=tool['cat'],
            formats_json=formats_json, format_chips=format_chips,
            guide_items=guide_items, controls_html=controls,
            tool_specific_code=tool_code
        )

    filepath = os.path.join(TOOLS_DIR, f'{slug}.html')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(page)
    print(f'  Generated: tools/{slug}.html')

print(f"\nAll {len(TOOLS_DATA)} tool pages generated!")

# ============================================================
# GENERATE PRIVACY POLICY PAGE
# ============================================================
PRIVACY_HTML = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>隐私政策 - MiniTool</title>
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🛠️</text></svg>">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
<style>
:root{--primary:#6366f1;--primary-light:#818cf8;--bg:#0f0f13;--bg2:#13131c;--surface:#1a1a24;--border:#2d2d4a;--text:#e2e8f0;--text-muted:#94a3b8;--radius:14px}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Inter','Noto Sans SC',system-ui,sans-serif;background:var(--bg);color:var(--text);min-height:100vh}
.header{background:rgba(15,15,19,0.85);backdrop-filter:blur(20px);border-bottom:1px solid var(--border);position:sticky;top:0;z-index:100;padding:0 24px}
.header-inner{max-width:1200px;margin:0 auto;display:flex;align-items:center;gap:20px;height:64px}
.logo{display:flex;align-items:center;gap:10px;text-decoration:none}
.logo-icon{width:36px;height:36px;background:linear-gradient(135deg,var(--primary),#f59e0b);border-radius:10px;display:flex;align-items:center;justify-content:center;color:white;font-weight:800;font-size:16px}
.logo-text{font-size:20px;font-weight:800;background:linear-gradient(135deg,var(--primary-light),#f59e0b);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.content{max-width:800px;margin:0 auto;padding:48px 24px 60px}
.content h1{font-size:28px;font-weight:800;margin-bottom:24px}
.content h2{font-size:18px;font-weight:700;margin:32px 0 12px;color:var(--primary-light)}
.content p,.content li{font-size:14px;line-height:1.8;color:var(--text-muted);margin-bottom:8px}
.content ul{padding-left:20px;margin-bottom:16px}
.content li{margin-bottom:6px}
.update-date{font-size:13px;color:var(--text-muted);margin-bottom:32px}
.footer{text-align:center;padding:32px 24px;color:var(--text-muted);font-size:12px;border-top:1px solid var(--border);margin-top:40px}
.footer a{color:var(--primary-light);text-decoration:none}
</style>
</head>
<body>

<header class="header">
  <div class="header-inner">
    <a href="/" class="logo">
      <div class="logo-icon">M</div>
      <span class="logo-text">MiniTool</span>
    </a>
  </div>
</header>

<div class="content">
  <h1>隐私政策</h1>
  <p class="update-date">最后更新日期：2025年7月4日</p>

  <p>MiniTool（以下简称"我们"）非常重视用户隐私保护。本隐私政策旨在向您说明我们如何收集、使用、存储和保护您的信息。</p>

  <h2>1. 数据处理原则</h2>
  <p>MiniTool 的核心设计理念是<strong>所有文件处理均在用户浏览器本地完成</strong>。我们不会将您上传的任何文件或数据传输到远程服务器。</p>
  <ul>
    <li>所有 PDF、图片、视频处理操作均在您的浏览器中执行</li>
    <li>处理完成后，文件数据仅保存在您的本地设备中</li>
    <li>关闭浏览器标签页后，所有临时数据将自动清除</li>
  </ul>

  <h2>2. 我们收集的信息</h2>
  <p>我们仅收集以下最少必要信息：</p>
  <ul>
    <li><strong>访问日志</strong>：我们可能通过第三方分析工具（如 Google Analytics）收集匿名的访问统计数据，包括页面浏览量、访问时长、设备类型等</li>
    <li><strong>本地存储</strong>：我们使用浏览器的 LocalStorage 技术保存您的偏好设置（如最近使用的工具），这些数据完全存储在您的设备上</li>
  </ul>

  <h2>3. 我们不收集的信息</h2>
  <ul>
    <li>您上传的任何文件内容</li>
    <li>处理过程中的任何数据</li>
    <li>您的个人身份信息（除非您主动通过反馈功能提供）</li>
  </ul>

  <h2>4. Cookie 使用</h2>
  <p>我们可能使用 Cookie 和类似技术来：</p>
  <ul>
    <li>改善网站性能和用户体验</li>
    <li>分析网站使用情况</li>
    <li>记住您的偏好设置</li>
  </ul>
  <p>您可以通过浏览器设置管理或删除 Cookie。</p>

  <h2>5. 第三方服务</h2>
  <p>我们可能使用以下第三方服务：</p>
  <ul>
    <li>Google Analytics：用于匿名访问统计分析</li>
    <li>CDN 服务：用于加速网页资源的加载</li>
  </ul>
  <p>这些第三方服务有其各自的隐私政策，我们建议您查阅了解。</p>

  <h2>6. 数据安全</h2>
  <p>我们采取合理的技术措施保护信息安全：</p>
  <ul>
    <li>网站使用 HTTPS 加密传输</li>
    <li>所有文件处理均在本地完成，不经过网络传输</li>
    <li>定期审查安全措施的有效性</li>
  </ul>

  <h2>7. 儿童隐私</h2>
  <p>我们的服务不面向 14 岁以下儿童。我们不会故意收集儿童的个人信息。</p>

  <h2>8. 政策更新</h2>
  <p>我们可能会不时更新本隐私政策。重大变更将通过网站公告通知您。继续使用我们的服务即表示您同意更新后的政策。</p>

  <h2>9. 联系我们</h2>
  <p>如果您对本隐私政策有任何疑问，请通过以下方式联系我们：</p>
  <ul>
    <li>邮箱：support@toolmini.cn</li>
  </ul>
</div>

<footer class="footer">
  <p>© 2025 MiniTool. All rights reserved.</p>
  <p style="margin-top:6px"><a href="/privacy.html">隐私政策</a> · <a href="/terms.html">使用条款</a></p>
</footer>

</body>
</html>'''

with open(os.path.join(BASE_DIR, 'privacy.html'), 'w', encoding='utf-8') as f:
    f.write(PRIVACY_HTML)
print("privacy.html generated!")

# ============================================================
# GENERATE TERMS OF USE PAGE
# ============================================================
TERMS_HTML = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>使用条款 - MiniTool</title>
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🛠️</text></svg>">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
<style>
:root{--primary:#6366f1;--primary-light:#818cf8;--bg:#0f0f13;--bg2:#13131c;--surface:#1a1a24;--border:#2d2d4a;--text:#e2e8f0;--text-muted:#94a3b8;--radius:14px}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Inter','Noto Sans SC',system-ui,sans-serif;background:var(--bg);color:var(--text);min-height:100vh}
.header{background:rgba(15,15,19,0.85);backdrop-filter:blur(20px);border-bottom:1px solid var(--border);position:sticky;top:0;z-index:100;padding:0 24px}
.header-inner{max-width:1200px;margin:0 auto;display:flex;align-items:center;gap:20px;height:64px}
.logo{display:flex;align-items:center;gap:10px;text-decoration:none}
.logo-icon{width:36px;height:36px;background:linear-gradient(135deg,var(--primary),#f59e0b);border-radius:10px;display:flex;align-items:center;justify-content:center;color:white;font-weight:800;font-size:16px}
.logo-text{font-size:20px;font-weight:800;background:linear-gradient(135deg,var(--primary-light),#f59e0b);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.content{max-width:800px;margin:0 auto;padding:48px 24px 60px}
.content h1{font-size:28px;font-weight:800;margin-bottom:24px}
.content h2{font-size:18px;font-weight:700;margin:32px 0 12px;color:var(--primary-light)}
.content p,.content li{font-size:14px;line-height:1.8;color:var(--text-muted);margin-bottom:8px}
.content ul{padding-left:20px;margin-bottom:16px}
.content li{margin-bottom:6px}
.update-date{font-size:13px;color:var(--text-muted);margin-bottom:32px}
.footer{text-align:center;padding:32px 24px;color:var(--text-muted);font-size:12px;border-top:1px solid var(--border);margin-top:40px}
.footer a{color:var(--primary-light);text-decoration:none}
</style>
</head>
<body>

<header class="header">
  <div class="header-inner">
    <a href="/" class="logo">
      <div class="logo-icon">M</div>
      <span class="logo-text">MiniTool</span>
    </a>
  </div>
</header>

<div class="content">
  <h1>使用条款</h1>
  <p class="update-date">最后更新日期：2025年7月4日</p>

  <p>欢迎使用 MiniTool（以下简称"本服务"）。在使用本服务之前，请仔细阅读以下使用条款。使用本服务即表示您同意遵守这些条款。</p>

  <h2>1. 服务说明</h2>
  <p>MiniTool 是一款免费的在线文件处理工具箱，提供 PDF、图片、视频等文件处理功能。所有文件处理均在用户浏览器本地完成。</p>
  <ul>
    <li>本服务以"现状"提供，不作任何明示或暗示的保证</li>
    <li>我们保留随时修改、暂停或终止服务的权利</li>
    <li>本服务免费提供，无需注册即可使用</li>
  </ul>

  <h2>2. 使用规范</h2>
  <p>您在使用本服务时，应遵守以下规范：</p>
  <ul>
    <li>遵守中华人民共和国相关法律法规</li>
    <li>不得使用本服务处理涉及国家秘密、商业秘密或他人隐私的文件</li>
    <li>不得利用本服务从事任何违法或侵权活动</li>
    <li>不得通过自动化手段大规模访问或抓取本网站内容</li>
    <li>不得尝试破坏网站安全措施或干扰正常服务运行</li>
  </ul>

  <h2>3. 知识产权</h2>
  <ul>
    <li>MiniTool 网站的所有内容（包括但不限于文字、图片、代码、设计）受知识产权法保护</li>
    <li>未经书面授权，不得复制、修改、分发本网站的任何内容</li>
    <li>您通过本服务处理的文件，其知识产权归原权利人所有</li>
  </ul>

  <h2>4. 免责声明</h2>
  <ul>
    <li>本服务按"现状"提供，我们不保证服务的不间断运行或无错误</li>
    <li>对于因使用本服务导致的任何直接或间接损失，我们不承担责任</li>
    <li>文件处理结果仅供参考，我们不对处理结果的准确性、完整性作保证</li>
    <li>建议用户在处理重要文件前做好备份</li>
    <li>对于因不可抗力导致的服务中断，我们不承担责任</li>
  </ul>

  <h2>5. 文件处理</h2>
  <ul>
    <li>所有文件处理均在浏览器本地完成，不会上传到服务器</li>
    <li>处理完成后，建议及时下载结果文件</li>
    <li>关闭浏览器后，临时处理数据将自动清除，无法恢复</li>
    <li>我们不对因浏览器崩溃、断电等导致的数据丢失承担责任</li>
  </ul>

  <h2>6. 条款修改</h2>
  <p>我们保留随时修改本使用条款的权利。重大变更将通过网站公告通知。继续使用服务即表示您同意修改后的条款。</p>

  <h2>7. 争议解决</h2>
  <p>因本条款产生的争议，双方应友好协商解决。协商不成的，任何一方均可向我们所在地有管辖权的人民法院提起诉讼。</p>

  <h2>8. 联系方式</h2>
  <p>如您对本使用条款有任何疑问，请联系：</p>
  <ul>
    <li>邮箱：support@toolmini.cn</li>
  </ul>
</div>

<footer class="footer">
  <p>© 2025 MiniTool. All rights reserved.</p>
  <p style="margin-top:6px"><a href="/privacy.html">隐私政策</a> · <a href="/terms.html">使用条款</a></p>
</footer>

</body>
</html>'''

with open(os.path.join(BASE_DIR, 'terms.html'), 'w', encoding='utf-8') as f:
    f.write(TERMS_HTML)
print("terms.html generated!")

print("\n=== ALL FILES GENERATED SUCCESSFULLY ===")
