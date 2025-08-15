const API_BASE = 'http://127.0.0.1:8000/api';

async function ask() {
  const q = document.getElementById('question').value.trim();
  if (!q) return;
  const btn = document.getElementById('ask');
  const ans = document.getElementById('answer');
  btn.disabled = true; btn.textContent = '思考中...';
  ans.innerHTML = '';
  try {
    const resp = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: q, top_k: 4 })
    });
    const data = await resp.json();
    const ctxHtml = (data.contexts || []).map((c, i) => `
      <div class="ctx">
        <div class="src">[${i + 1}] 来源：${c.source}（相似度 ${c.score.toFixed(3)}）</div>
        <pre>${c.text}</pre>
      </div>
    `).join('');
    ans.innerHTML = `
      <div class="model">模型：${data.model} ｜ 延迟：${data.latency_ms} ms</div>
      <div class="a">${data.answer.replace(/\n/g, '<br/>')}</div>
      <h3>引用</h3>
      ${ctxHtml}
    `;
  } catch (e) {
    ans.textContent = '请求失败：' + e;
  } finally {
    btn.disabled = false; btn.textContent = '提问';
  }
}

document.getElementById('ask').addEventListener('click', ask);


