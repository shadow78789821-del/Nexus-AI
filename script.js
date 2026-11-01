const modal = document.getElementById('toolModal');
const closeModal = document.getElementById('closeModal');
const chatForm = document.getElementById('chatForm');
const textForm = document.getElementById('textForm');
const chatLog = document.getElementById('chatLog');
const chatInputForm = document.getElementById('chatInputForm');
const chatInput = document.getElementById('chatInput');
const mainText = document.getElementById('mainText');
const resultArea = document.getElementById('resultArea');
const resultContent = document.getElementById('resultContent');
const toast = document.getElementById('toast');

const tools = {
  chat: {title:'AI Chat', eyebrow:'YOUR AI COMPANION', description:'Ask a question and explore an idea.', mode:'chat'},
  summarize: {title:'Text Summarizer', eyebrow:'SAVE YOUR TIME', description:'Turn long text into clear, useful notes.', mode:'text', label:'TEXT TO SUMMARIZE', placeholder:'Paste your notes or an article here...', hint:'Paste a paragraph or longer piece of text.'},
  study: {title:'Study Assistant', eyebrow:'LEARN WITH EASE', description:'Get a simple explanation of any topic.', mode:'text', label:'WHAT DO YOU WANT TO LEARN?', placeholder:'For example: Explain photosynthesis to a beginner...', hint:'Enter a subject, topic or question.'},
  quiz: {title:'Quiz Generator', eyebrow:'TEST YOURSELF', description:'Create practice questions to check your knowledge.', mode:'text', label:'QUIZ TOPIC', placeholder:'For example: Create a beginner quiz about the solar system...', hint:'Enter a topic and optionally mention how many questions.'}
};
let currentTool = 'chat';
let lastResult = '';

function showToast(message) {
  toast.textContent = message;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 2600);
}
function openWorkspace(tool='chat') {
  modal.classList.add('open');
  modal.setAttribute('aria-hidden','false');
  document.body.style.overflow='hidden';
  setTool(tool);
}
function closeWorkspace() {
  modal.classList.remove('open');
  modal.setAttribute('aria-hidden','true');
  document.body.style.overflow='';
}
function setTool(tool) {
  currentTool = tool;
  const config = tools[tool];
  document.getElementById('modalTitle').textContent = config.title;
  document.getElementById('panelEyebrow').textContent = config.eyebrow;
  document.getElementById('panelDescription').textContent = config.description;
  chatForm.classList.toggle('hidden', config.mode !== 'chat');
  textForm.classList.toggle('hidden', config.mode !== 'text');
  resultArea.classList.add('hidden');
  document.querySelectorAll('.side-tool').forEach(btn => btn.classList.toggle('selected', btn.dataset.tool === tool));
  if (config.mode === 'text') {
    document.getElementById('textLabel').textContent = config.label;
    mainText.placeholder = config.placeholder;
    document.getElementById('textHint').textContent = config.hint;
  }
}
document.querySelectorAll('[data-open-tool]').forEach(btn => btn.addEventListener('click', () => openWorkspace(btn.dataset.openTool)));
document.querySelectorAll('.side-tool').forEach(btn => btn.addEventListener('click', () => setTool(btn.dataset.tool)));
closeModal.addEventListener('click', closeWorkspace);
modal.addEventListener('click', e => { if (e.target === modal) closeWorkspace(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeWorkspace(); });

function addMessage(text, who) {
  const row = document.createElement('div');
  row.className = `message ${who === 'user' ? 'user-message' : 'assistant-message'}`;
  if (who !== 'user') {
    const avatar = document.createElement('span');
    avatar.className = 'message-avatar';
    avatar.textContent = '✳';
    row.appendChild(avatar);
  }
  const bubble = document.createElement('div');
  bubble.className = 'message-bubble';
  if (who !== 'user') {
    const label = document.createElement('b');
    label.textContent = 'Nexus AI';
    bubble.appendChild(label);
  }
  const p = document.createElement('p');
  p.textContent = text;
  bubble.appendChild(p);
  row.appendChild(bubble);
  chatLog.appendChild(row);
  chatLog.scrollTop = chatLog.scrollHeight;
  return p;
}
async function askBackend(mode, prompt) {
  const response = await fetch('/api/ask', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({mode, prompt})
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.error || 'The AI service could not complete your request.');
  return data.answer;
}
chatInputForm.addEventListener('submit', async e => {
  e.preventDefault();
  const prompt = chatInput.value.trim();
  if (!prompt) return;
  chatInput.value = '';
  addMessage(prompt, 'user');
  const loading = addMessage('Thinking...', 'assistant');
  const send = chatInputForm.querySelector('button');
  send.disabled = true;
  try {
    loading.textContent = await askBackend('chat', prompt);
  } catch (error) {
    loading.textContent = `${error.message}\n\nIf you're running the project for the first time, follow the README to add your AI API key and start the Python server.`;
  } finally {
    send.disabled = false;
    chatInput.focus();
  }
});
document.getElementById('runTextTool').addEventListener('click', async () => {
  const prompt = mainText.value.trim();
  if (!prompt) { showToast('Please enter some text or a topic first.'); return; }
  const button = document.getElementById('runTextTool');
  button.disabled = true;
  button.textContent = 'Working...';
  resultArea.classList.remove('hidden');
  resultContent.textContent = 'Nexus AI is preparing your result...';
  const mode = currentTool;
  try {
    lastResult = await askBackend(mode, prompt);
    resultContent.textContent = lastResult;
  } catch (error) {
    resultContent.textContent = `${error.message}\n\nFollow the README setup instructions to connect the AI service.`;
  } finally {
    button.disabled = false;
    button.innerHTML = 'Generate result <span>→</span>';
  }
});
document.getElementById('copyResult').addEventListener('click', async () => {
  if (!lastResult) return;
  try { await navigator.clipboard.writeText(lastResult); showToast('Result copied to clipboard.'); }
  catch { showToast('Clipboard access is unavailable in this browser.'); }
});
