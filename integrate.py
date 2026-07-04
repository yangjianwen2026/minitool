# -*- coding: utf-8 -*-
"""
将所有HTML整合到index.html单文件，使用hash路由
- #/privacy, #/terms 显示内嵌视图
- #/pdf-merge 等自动打开对应工具
- 原30个工具页面改为轻量redirect（SEO兼容）
"""
import os, re

BASE = r"C:\Users\newna\.qianfan\workspace\14dabc72fd0e469abfba93777adccb0a"
IDX = os.path.join(BASE, "index.html")

with open(IDX, 'r', encoding='utf-8') as f:
    html = f.read()

# ================================================================
# 1. 添加隐私政策和条款的内嵌视图 HTML
#    放在 feedback-overlay 之后、footer 之前
# ================================================================
privacy_terms_views = '''
<!-- LEGAL PAGES (hash router views) -->
<div class="legal-overlay" id="privacyView" style="display:none">
  <div class="legal-page">
    <div class="legal-header">
      <a href="#/" class="legal-back" aria-label="返回首页"><i data-lucide="arrow-left" style="width:18px;height:18px"></i> 返回首页</a>
    </div>
    <h1>隐私政策</h1>
    <p class="legal-date">最后更新日期：2025年7月4日</p>
    <p>MiniTool（以下简称"我们"）非常重视用户隐私保护。本隐私政策旨在向您说明我们如何收集、使用、存储和保护您的信息。</p>
    <h2>1. 数据处理原则</h2>
    <p>MiniTool 的核心设计理念是<strong>所有文件处理均在用户浏览器本地完成</strong>。我们不会将您上传的任何文件或数据传输到远程服务器。</p>
    <ul><li>所有 PDF、图片、视频处理操作均在您的浏览器中执行</li><li>处理完成后，文件数据仅保存在您的本地设备中</li><li>关闭浏览器标签页后，所有临时数据将自动清除</li></ul>
    <h2>2. 我们收集的信息</h2>
    <p>我们仅收集以下最少必要信息：</p>
    <ul><li><strong>访问日志</strong>：我们可能通过第三方分析工具收集匿名的访问统计数据</li><li><strong>本地存储</strong>：我们使用浏览器的 LocalStorage 技术保存您的偏好设置</li></ul>
    <h2>3. 我们不收集的信息</h2>
    <ul><li>您上传的任何文件内容</li><li>处理过程中的任何数据</li><li>您的个人身份信息（除非您主动通过反馈功能提供）</li></ul>
    <h2>4. Cookie 使用</h2>
    <p>我们可能使用 Cookie 和类似技术来改善网站性能和用户体验、分析网站使用情况、记住您的偏好设置。您可以通过浏览器设置管理或删除 Cookie。</p>
    <h2>5. 第三方服务</h2>
    <p>我们可能使用 Google Analytics（匿名访问统计分析）和 CDN 服务来加速网页资源加载。这些第三方服务有其各自的隐私政策。</p>
    <h2>6. 数据安全</h2>
    <ul><li>网站使用 HTTPS 加密传输</li><li>所有文件处理均在本地完成，不经过网络传输</li><li>定期审查安全措施的有效性</li></ul>
    <h2>7. 儿童隐私</h2>
    <p>我们的服务不面向 14 岁以下儿童。我们不会故意收集儿童的个人信息。</p>
    <h2>8. 政策更新</h2>
    <p>我们可能会不时更新本隐私政策。重大变更将通过网站公告通知您。</p>
    <h2>9. 联系我们</h2>
    <p>邮箱：support@toolmini.cn</p>
  </div>
</div>

<div class="legal-overlay" id="termsView" style="display:none">
  <div class="legal-page">
    <div class="legal-header">
      <a href="#/" class="legal-back" aria-label="返回首页"><i data-lucide="arrow-left" style="width:18px;height:18px"></i> 返回首页</a>
    </div>
    <h1>使用条款</h1>
    <p class="legal-date">最后更新日期：2025年7月4日</p>
    <p>欢迎使用 MiniTool（以下简称"本服务"）。在使用本服务之前，请仔细阅读以下使用条款。使用本服务即表示您同意遵守这些条款。</p>
    <h2>1. 服务说明</h2>
    <p>MiniTool 是一款免费的在线文件处理工具箱，提供 PDF、图片、视频等文件处理功能。所有文件处理均在用户浏览器本地完成。</p>
    <ul><li>本服务以"现状"提供，不作任何明示或暗示的保证</li><li>我们保留随时修改、暂停或终止服务的权利</li><li>本服务免费提供，无需注册即可使用</li></ul>
    <h2>2. 使用规范</h2>
    <ul><li>遵守中华人民共和国相关法律法规</li><li>不得使用本服务处理涉及国家秘密、商业秘密或他人隐私的文件</li><li>不得利用本服务从事任何违法或侵权活动</li><li>不得通过自动化手段大规模访问或抓取本网站内容</li><li>不得尝试破坏网站安全措施或干扰正常服务运行</li></ul>
    <h2>3. 知识产权</h2>
    <ul><li>MiniTool 网站的所有内容受知识产权法保护</li><li>未经书面授权，不得复制、修改、分发本网站的任何内容</li><li>您通过本服务处理的文件，其知识产权归原权利人所有</li></ul>
    <h2>4. 免责声明</h2>
    <ul><li>本服务按"现状"提供，我们不保证服务的不间断运行或无错误</li><li>对于因使用本服务导致的任何直接或间接损失，我们不承担责任</li><li>文件处理结果仅供参考，我们不对处理结果的准确性、完整性作保证</li><li>建议用户在处理重要文件前做好备份</li></ul>
    <h2>5. 文件处理</h2>
    <ul><li>所有文件处理均在浏览器本地完成，不会上传到服务器</li><li>处理完成后，建议及时下载结果文件</li><li>关闭浏览器后，临时处理数据将自动清除，无法恢复</li></ul>
    <h2>6. 条款修改</h2>
    <p>我们保留随时修改本使用条款的权利。继续使用服务即表示您同意修改后的条款。</p>
    <h2>7. 争议解决</h2>
    <p>因本条款产生的争议，双方应友好协商解决。协商不成的，任何一方均可向我们所在地有管辖权的人民法院提起诉讼。</p>
    <h2>8. 联系方式</h2>
    <p>邮箱：support@toolmini.cn</p>
  </div>
</div>
'''

# 插入到 footer 之前
html = html.replace(
    '<footer class="footer">',
    privacy_terms_views + '\n<footer class="footer">'
)

# ================================================================
# 2. 添加法律页面的 CSS 样式
# ================================================================
legal_css = """
/* Legal Pages */
.legal-overlay {
  position: fixed; inset: 0; z-index: 250;
  background: var(--bg); overflow-y: auto;
  animation: fadeIn 0.25s ease;
}
.legal-page {
  max-width: 760px; margin: 0 auto; padding: 32px 24px 60px;
}
.legal-header {
  margin-bottom: 24px;
}
.legal-back {
  display: inline-flex; align-items: center; gap: 6px;
  color: var(--primary-light); text-decoration: none;
  font-size: 14px; font-weight: 600;
  padding: 8px 16px; border-radius: 8px;
  background: var(--surface); transition: background 0.2s;
}
.legal-back:hover { background: var(--surface2); }
.legal-page h1 {
  font-size: 28px; font-weight: 800; margin-bottom: 8px;
}
.legal-page h2 {
  font-size: 17px; font-weight: 700; margin: 28px 0 10px;
  color: var(--primary-light);
}
.legal-page p {
  font-size: 14px; line-height: 1.8; color: var(--text-muted); margin-bottom: 8px;
}
.legal-page ul {
  padding-left: 20px; margin-bottom: 12px;
}
.legal-page li {
  font-size: 14px; line-height: 1.8; color: var(--text-muted); margin-bottom: 4px;
}
.legal-date {
  font-size: 13px; color: var(--text-muted); margin-bottom: 28px !important;
}
"""

# 在 Responsive CSS 之前插入
html = html.replace(
    '/* Responsive */\n@media (max-width: 640px) {',
    legal_css + '\n/* Responsive */\n@media (max-width: 640px) {'
)

# ================================================================
# 3. 修改页脚链接为 hash 路由
# ================================================================
html = html.replace(
    '<a href="/privacy.html" style="color:var(--primary-light);text-decoration:none;font-size:12px">隐私政策</a>',
    '<a href="#/privacy" style="color:var(--primary-light);text-decoration:none;font-size:12px">隐私政策</a>'
)
html = html.replace(
    '<a href="/terms.html" style="color:var(--primary-light);text-decoration:none;font-size:12px">使用条款</a>',
    '<a href="#/terms" style="color:var(--primary-light);text-decoration:none;font-size:12px">使用条款</a>'
)

# ================================================================
# 4. 修改工具卡片的 🔗 链接为 hash 路由
# ================================================================
html = html.replace(
    """<a href="${tool.slug ? '/tools/' + tool.slug + '.html' : '#'}" class="tool-link" onclick="event.stopPropagation()" title="独立页面打开" aria-label="在独立页面打开${tool.name}">🔗</a>""",
    """<a href="#/${tool.slug || ''}" class="tool-link" onclick="event.stopPropagation()" title="独立页面打开" aria-label="在独立页面打开${tool.name}">🔗</a>"""
)

# ================================================================
# 5. 添加 hash 路由系统 JS
#    在 INIT 部分之后、PWA QR 代码之前
# ================================================================
router_js = """
// ─────────────────────────────────────────────
// HASH ROUTER
// ─────────────────────────────────────────────
const TOOL_SLUG_MAP = {
  'pdf-merge':'pdf_merge','pdf-split':'pdf_split','pdf-to-jpg':'pdf_to_jpg',
  'jpg-to-pdf':'jpg_to_pdf','pdf-compress':'pdf_compress','pdf-encrypt':'pdf_encrypt',
  'pdf-unlock':'pdf_unlock','pdf-sign':'pdf_sign','pdf-rotate':'pdf_rotate',
  'pdf-extract':'pdf_extract','pdf-to-word':'pdf_to_word','pdf-to-excel':'pdf_to_excel',
  'img-compress':'img_compress','img-convert':'img_convert','img-resize':'img_resize',
  'img-crop':'img_crop','img-rotate':'img_rotate','img-watermark':'img_watermark',
  'img-grid':'img_grid','img-join':'img_join','img-unwatermark':'img_unwatermark',
  'vid-to-gif':'vid_to_gif','gif-to-vid':'gif_to_vid','vid-thumb':'vid_thumb',
  'vid-unwatermark':'vid_unwatermark','ai-polish':'ai_polish','ai-continue':'ai_continue',
  'ai-title':'ai_title','ai-summary':'ai_summary','ai-marketing':'ai_marketing'
};

function hideAllViews() {
  document.getElementById('mainContent').style.display = '';
  document.getElementById('privacyView').style.display = 'none';
  document.getElementById('termsView').style.display = 'none';
  const ws = document.getElementById('workspaceOverlay');
  if (ws.classList.contains('open')) closeWorkspace();
}

function handleRoute() {
  const hash = location.hash.replace('#', '') || '/';
  const parts = hash.split('/').filter(Boolean);

  hideAllViews();

  if (parts.length === 0 || (parts.length === 1 && parts[0] === '')) {
    // Home
    document.getElementById('mainContent').style.display = '';
    document.title = 'MiniTool - 免费在线PDF/图片/视频处理工具箱 | 纯本地处理不上传';
  } else if (parts[0] === 'privacy') {
    document.getElementById('mainContent').style.display = 'none';
    document.getElementById('privacyView').style.display = '';
    document.title = '隐私政策 - MiniTool';
    lucide.createIcons();
  } else if (parts[0] === 'terms') {
    document.getElementById('mainContent').style.display = 'none';
    document.getElementById('termsView').style.display = '';
    document.title = '使用条款 - MiniTool';
    lucide.createIcons();
  } else {
    // Tool route: #/pdf-merge
    const slug = parts[0];
    const toolId = TOOL_SLUG_MAP[slug];
    if (toolId) {
      document.getElementById('mainContent').style.display = 'none';
      openTool(toolId);
      const tool = TOOLS.find(t => t.id === toolId);
      if (tool) document.title = tool.name + ' - MiniTool 免费在线工具';
    } else {
      // Unknown route, go home
      document.getElementById('mainContent').style.display = '';
      location.hash = '#/';
    }
  }
}

// Listen for hash changes (browser back/forward)
window.addEventListener('hashchange', handleRoute);

// Handle initial route
if (location.hash && location.hash !== '#' && location.hash !== '#/') {
  // Defer to after DOM ready
  setTimeout(handleRoute, 100);
}
"""

# 在 DOMContentLoaded 监听器之后插入路由
html = html.replace(
    """document.addEventListener('DOMContentLoaded', () => {
  renderRecentTools();
});""",
    """document.addEventListener('DOMContentLoaded', () => {
  renderRecentTools();
  // Handle initial hash route after tools are rendered
  if (location.hash && location.hash !== '#' && location.hash !== '#/') {
    handleRoute();
  }
});\n""" + router_js
)

# ================================================================
# 6. 修改 closeWorkspace 也处理 hash 路由
# ================================================================
old_close_workspace = """function closeWorkspace() {
  const overlay = document.getElementById('workspaceOverlay');
  overlay.classList.remove('open');
  document.getElementById('mainContent').style.display = '';
  document.body.style.overflow = '';
  clearFiles();
}"""

new_close_workspace = """function closeWorkspace() {
  const overlay = document.getElementById('workspaceOverlay');
  overlay.classList.remove('open');
  // If we're on a tool hash route, navigate back to home
  const hash = location.hash.replace('#', '');
  if (hash && hash !== '/' && TOOL_SLUG_MAP[hash.split('/').filter(Boolean)[0]]) {
    location.hash = '#/';
  } else {
    document.getElementById('mainContent').style.display = '';
  }
  document.body.style.overflow = '';
  clearFiles();
}"""

html = html.replace(old_close_workspace, new_close_workspace)

# ================================================================
# 7. 修改 openTool 也更新 hash（避免重复触发路由）
#    找到 patched openTool，在 _originalOpenTool(id) 前更新 hash
# ================================================================
old_open_tool_patch = """const _originalOpenTool = openTool;
openTool = function(id) {
  addRecentTool(id);
  _originalOpenTool(id);
};"""

new_open_tool_patch = """const _originalOpenTool = openTool;
openTool = function(id, fromRoute) {
  addRecentTool(id);
  // Update hash without triggering route handler (if not already from route)
  if (!fromRoute) {
    const tool = TOOLS.find(t => t.id === id);
    if (tool && tool.slug) {
      history.pushState(null, '', '#/' + tool.slug);
    }
  }
  _originalOpenTool(id);
};"""

html = html.replace(old_open_tool_patch, new_open_tool_patch)

# 修改 handleRoute 中调用 openTool 时标记 fromRoute=true
html = html.replace(
    "openTool(toolId);",
    "openTool(toolId, true);"
)

# ================================================================
# 8. 修改 sitemap.xml 中的工具 URL 也指向 hash 路由
# ================================================================
sitemap_path = os.path.join(BASE, "sitemap.xml")
sitemap = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://toolmini.cn/</loc><lastmod>2026-07-04</lastmod><changefreq>weekly</changefreq><priority>1.0</priority></url>
  <url><loc>https://toolmini.cn/#/privacy</loc><lastmod>2026-07-04</lastmod><changefreq>monthly</changefreq><priority>0.3</priority></url>
  <url><loc>https://toolmini.cn/#/terms</loc><lastmod>2026-07-04</lastmod><changefreq>monthly</changefreq><priority>0.3</priority></url>
"""
slugs = [
    'pdf-merge','pdf-split','pdf-to-jpg','jpg-to-pdf','pdf-compress','pdf-encrypt',
    'pdf-unlock','pdf-sign','pdf-rotate','pdf-extract','pdf-to-word','pdf-to-excel',
    'img-compress','img-convert','img-resize','img-crop','img-rotate','img-watermark',
    'img-grid','img-join','img-unwatermark','vid-to-gif','gif-to-vid','vid-thumb',
    'vid-unwatermark','ai-polish','ai-continue','ai-title','ai-summary','ai-marketing'
]
for slug in slugs:
    sitemap += f'  <url><loc>https://toolmini.cn/#/{slug}</loc><lastmod>2026-07-04</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n'
sitemap += '</urlset>'
with open(sitemap_path, 'w', encoding='utf-8') as f:
    f.write(sitemap)

# ================================================================
# 9. 将30个独立工具页面改为轻量 redirect（SEO: 搜索引擎仍可发现）
# ================================================================
tools_dir = os.path.join(BASE, "tools")
for fname in os.listdir(tools_dir):
    if not fname.endswith('.html'):
        continue
    slug = fname.replace('.html', '')
    fpath = os.path.join(tools_dir, fname)

    # 保留完整的 SEO 页面但添加 JS redirect 到 hash URL
    redirect_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{slug.replace('-',' ').title()} - MiniTool 免费在线工具</title>
<meta name="description" content="免费在线{slug.replace('-',' ')}工具，纯浏览器本地处理，无需注册，文件绝不上传。">
<link rel="canonical" href="https://toolmini.cn/#/{slug}">
<meta http-equiv="refresh" content="0;url=/{'' if slug == 'index' else '#' + '/' + slug}">
<script>window.location.replace('/#/{slug}');</script>
</head>
<body>
<noscript>
<p>正在跳转... 如未自动跳转，请<a href="/#/{slug}">点击这里</a>。</p>
</noscript>
</body>
</html>"""
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(redirect_html)

print(f"30 tool pages converted to redirects!")

# ================================================================
# 10. privacy.html 和 terms.html 也改为 redirect
# ================================================================
for page, slug in [('privacy.html', 'privacy'), ('terms.html', 'terms')]:
    fpath = os.path.join(BASE, page)
    redirect = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{'隐私政策' if slug=='privacy' else '使用条款'} - MiniTool</title>
<link rel="canonical" href="https://toolmini.cn/#/{slug}">
<meta http-equiv="refresh" content="0;url=/#/{slug}">
<script>window.location.replace('/#/{slug}');</script>
</head>
<body>
<noscript>
<p>正在跳转... 如未自动跳转，请<a href="/#/{slug}">点击这里</a>。</p>
</noscript>
</body>
</html>"""
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(redirect)

print("privacy.html & terms.html converted to redirects!")

# ================================================================
# 保存修改后的 index.html
# ================================================================
with open(IDX, 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html integrated with hash router!")
print("\n=== INTEGRATION COMPLETE ===")
