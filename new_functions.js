// ─────────────────────────────────────────────
// TOOL USAGE TIPS
// ─────────────────────────────────────────────
const TOOL_TIPS = {
  pdf_merge:      '提示：可一次选择多个PDF文件 | 按选择顺序合并 | 合并后原文件不会被修改',
  pdf_split:      '提示：输入页码如 1-3,5,7-9 | 可拆分后分别下载 | 支持不连续页码',
  pdf_to_jpg:     '提示：每页生成一张图片 | 图片按页码命名 | 输出为ZIP压缩包',
  jpg_to_pdf:     '提示：图片按选择顺序排列 | 支持批量转换 | 自动适配页面大小',
  pdf_to_word:    '提示：纯文本PDF效果最佳 | 复杂排版可能丢失格式 | 建议使用PDF转JPG辅助OCR',
  pdf_to_excel:   '提示：自动识别表格边框 | 合并单元格需手动调整 | 建议先预览效果',
  pdf_compress:   '提示：压缩率越高画质越低 | 建议先试低压缩 | 可多次压缩对比效果',
  pdf_encrypt:    '提示：密码区分大小写 | 请牢记密码否则无法打开 | 建议使用强密码',
  pdf_unlock:     '提示：需输入正确密码才能解锁 | 解锁后文件无密码保护 | 请确保有权限操作',
  pdf_sign:       '提示：在画布上手写签名 | 可调整签名位置和大小 | 支持多次重签',
  pdf_rotate:     '提示：可选择旋转全部或指定页面 | 旋转角度为90°倍数 | 可预览后确认',
  pdf_extract:    '提示：输入页码如 1,3,5-8 | 提取页面组成新PDF | 原文件不变',
  img_compress:   '提示：质量越低文件越小 | 建议压缩后预览效果 | JPG格式压缩效果最明显',
  img_convert:    '提示：PNG转JPG会丢失透明度 | WebP格式兼顾质量和体积 | GIF转其他格式失去动画',
  img_resize:     '提示：锁定宽高比避免变形 | 放大可能导致模糊 | 建议先缩小再放大',
  img_crop:       '提示：拖拽裁剪框调整范围 | 可移动和缩放裁剪区域 | 裁剪后不可恢复',
  img_rotate:     '提示：旋转90°/180°/270° | 自定义角度可能裁切边缘 | 预览确认后处理',
  img_watermark:  '提示：文字水印支持调整透明度 | 图片水印建议使用PNG格式 | 可调整位置和大小',
  img_grid:       '提示：自动分割为3x3九宫格 | 适合社交媒体分享 | 输出9张单独图片',
  img_join:       '提示：支持横向或纵向拼接 | 自动调整画布大小 | 背景默认为白色',
  img_unwatermark:'提示：涂抹需去除的区域 | 智能填充周围像素 | 复杂背景可能效果不佳',
  vid_to_gif:     '提示：建议剪辑短片段 | GIF文件可能较大 | 可调整帧率和尺寸',
  gif_to_vid:     '提示：转换为MP4格式 | 保持动画效果 | 文件体积可能增大',
  vid_thumb:      '提示：可设置截取时间点 | 输出为JPG图片 | 支持批量提取多帧',
  vid_unwatermark:'提示：涂抹需去除的Logo区域 | 处理时间较长请耐心等待 | 建议预览效果后确认',
  ai_polish:      '提示：输入需要润色的文字 | AI优化表达和流畅度 | 可多次生成对比效果',
  ai_continue:    '提示：输入文章开头或大纲 | AI续写完整内容 | 可指定写作风格',
  ai_title:       '提示：输入文章主题或内容 | 生成多个标题供选择 | 可指定标题风格',
  ai_summary:     '提示：输入长篇文章内容 | 生成精炼摘要 | 可指定摘要长度',
  ai_marketing:   '提示：输入产品信息和卖点 | 生成推广文案 | 可指定文案风格和长度'
};

// ─────────────────────────────────────────────
// RECENT TOOLS
// ─────────────────────────────────────────────
function renderRecentTools() {
  let recent = [];
  try {
    recent = JSON.parse(localStorage.getItem('minitool_recent') || '[]');
  } catch(e) { recent = []; }
  if (!recent.length) return;
  
  const container = document.getElementById('toolsContainer');
  let html = '<div class="section-title"><i data-lucide="clock" style="width:14px;height:14px"></i> 最近使用</div>';
  html += '<div class="tools-grid" data-cat="recent">';
  recent.forEach(id => {
    const tool = TOOLS.find(t => t.id === id);
    if (!tool) return;
    html += `
    <div class="tool-card" data-cat="${tool.cat}" data-id="${tool.id}" onclick="openTool('${tool.id}'); location.hash='tool=${tool.id}'; return false;">
      <div class="tool-card-inner">
        <div class="tool-icon"><i data-lucide="${tool.icon}" style="width:22px;height:22px"></i></div>
        <h3>${tool.name}</h3>
        <p>${tool.desc}</p>
        <span class="tool-tag">${tool.formats[0] === 'text' ? '文字' : tool.formats.map(f=>f.replace('.','')).join('/')}</span>
      </div>
    </div>`;
  });
  html += '</div>';
  container.insertAdjacentHTML('afterbegin', html);
  lucide.createIcons();
}

// ─────────────────────────────────────────────
// HASH ROUTING (for direct tool URLs)
// ─────────────────────────────────────────────
function initHashRouting() {
  const hash = location.hash;
  if (hash && hash.startsWith('#tool=')) {
    const toolId = hash.replace('#tool=', '');
    setTimeout(() => openTool(toolId), 800); // Wait for tools to render
  }
}
