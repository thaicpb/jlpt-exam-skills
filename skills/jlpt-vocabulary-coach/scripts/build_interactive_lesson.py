#!/usr/bin/env python3
"""Build an interactive JLPT study fragment from the local vocabulary loader."""

from __future__ import annotations

import argparse
import json
import random
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
LOADER = SCRIPT_DIR / "load_vocabulary.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--level", required=True)
    parser.add_argument("--lesson")
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--limit", type=int)
    selection.add_argument("--sample", type=int)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def load_items(args: argparse.Namespace) -> dict[str, object]:
    command = [sys.executable, str(LOADER), "--level", args.level]
    if args.lesson:
        command.extend(["--lesson", args.lesson])
    if args.limit is not None:
        command.extend(["--limit", str(args.limit)])
    if args.sample is not None:
        command.extend(["--sample", str(args.sample)])
    if args.seed is not None:
        command.extend(["--seed", str(args.seed)])
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def choices(correct: str, pool: list[str], rng: random.Random) -> list[str]:
    distractors = list(dict.fromkeys(value for value in pool if value != correct))
    rng.shuffle(distractors)
    result = [correct, *distractors[:3]]
    rng.shuffle(result)
    return result


def enrich(payload: dict[str, object]) -> dict[str, object]:
    items = payload["items"]
    assert isinstance(items, list)
    rng = random.Random(payload.get("seed") or 0)
    meanings = [str(item["meaning_vi"]) for item in items]
    words = [str(item["word"]) for item in items]
    for item in items:
        item["quiz_options"] = choices(str(item["meaning_vi"]), meanings, rng)
        item["cloze_options"] = choices(str(item["word"]), words, rng)
        example = str(item["example"])
        word = str(item["word"])
        item["cloze"] = example.replace(word, "＿＿＿", 1) if word in example else None
    return payload


FRAGMENT = r'''<div id="jlpt-vocabulary-quest">
  <style>
    #jlpt-vocabulary-quest { color:var(--foreground); font-size:calc(var(--font-size-base) * 1.12); }
    #jlpt-vocabulary-quest .jvc-header { display:flex; align-items:flex-start; justify-content:space-between; gap:18px; flex-wrap:wrap; margin-bottom:18px; }
    #jlpt-vocabulary-quest .jvc-session-meta { display:flex; gap:8px; flex-wrap:wrap; margin-top:8px; }
    #jlpt-vocabulary-quest .jvc-scoreline { display:flex; align-items:center; justify-content:space-between; gap:14px; flex-wrap:wrap; margin:14px 0 10px; }
    #jlpt-vocabulary-quest .jvc-score-items { display:flex; gap:18px; flex-wrap:wrap; }
    #jlpt-vocabulary-quest .jvc-score-value { font-weight:500; }
    #jlpt-vocabulary-quest .jvc-modes { margin:18px 0; }
    #jlpt-vocabulary-quest .jvc-stage { display:grid; gap:18px; margin-top:16px; }
    #jlpt-vocabulary-quest .jvc-stage-head { display:flex; align-items:flex-start; justify-content:space-between; gap:16px; flex-wrap:wrap; }
    #jlpt-vocabulary-quest .jvc-stage-head h3 { margin:6px 0 4px; }
    #jlpt-vocabulary-quest .jvc-center { text-align:center; }
    #jlpt-vocabulary-quest .jvc-content { min-height:330px; display:flex; flex-direction:column; justify-content:center; gap:16px; }
    #jlpt-vocabulary-quest .jvc-kicker { color:var(--muted-foreground); font-weight:500; letter-spacing:.08em; }
    #jlpt-vocabulary-quest .jvc-word { font-size:calc(var(--font-size-base) * 4.6); font-weight:500; margin:8px 0; overflow-wrap:anywhere; }
    #jlpt-vocabulary-quest .jvc-reading { font-size:calc(var(--font-size-base) * 1.8); font-weight:500; }
    #jlpt-vocabulary-quest .jvc-meaning { font-size:calc(var(--font-size-base) * 1.45); }
    #jlpt-vocabulary-quest .jvc-example { font-size:calc(var(--font-size-base) * 1.5); margin:10px 0; }
    #jlpt-vocabulary-quest .jvc-detail { display:grid; gap:10px; }
    #jlpt-vocabulary-quest .jvc-detail-row { display:grid; gap:4px; }
    #jlpt-vocabulary-quest .jvc-options { margin-top:8px; }
    #jlpt-vocabulary-quest .jvc-feedback { min-height:76px; display:grid; place-items:center; gap:4px; }
    #jlpt-vocabulary-quest .jvc-feedback-title { font-size:calc(var(--font-size-base) * 1.35); font-weight:500; }
    #jlpt-vocabulary-quest .jvc-success { color:var(--green); }
    #jlpt-vocabulary-quest .jvc-error { color:var(--red); }
    #jlpt-vocabulary-quest .jvc-actions { justify-content:center; }
    #jlpt-vocabulary-quest .jvc-complete { min-height:330px; display:grid; place-items:center; text-align:center; }
    #jlpt-vocabulary-quest .jvc-complete h2 { font-size:calc(var(--font-size-base) * 2); }
    @media (max-width:520px) {
      #jlpt-vocabulary-quest { font-size:var(--font-size-base); }
      #jlpt-vocabulary-quest .jvc-word { font-size:calc(var(--font-size-base) * 3.5); }
      #jlpt-vocabulary-quest .jvc-reading { font-size:calc(var(--font-size-base) * 1.55); }
      #jlpt-vocabulary-quest .jvc-example { font-size:calc(var(--font-size-base) * 1.3); }
      #jlpt-vocabulary-quest .jvc-content { min-height:280px; }
    }
  </style>

  <header class="jvc-header">
    <div>
      <div class="jvc-kicker">HÀNH TRÌNH TỪ VỰNG</div>
      <h1>JLPT Vocabulary Quest</h1>
      <div class="jvc-session-meta">
        <span class="viz-badge" id="jvc-level"></span>
        <span class="viz-badge" id="jvc-size"></span>
        <span class="viz-badge" id="jvc-seed"></span>
      </div>
    </div>
    <div class="text-muted">Học ít một · nhớ thật lâu</div>
  </header>

  <div class="jvc-scoreline" aria-label="Kết quả phiên học">
    <div class="jvc-score-items">
      <span><span id="jvc-done-label">Đã xem</span> <strong class="jvc-score-value tabular-nums" id="jvc-done">0</strong></span>
      <span>Đúng <strong class="jvc-score-value tabular-nums" id="jvc-score">0</strong></span>
      <span>Chuỗi <strong class="jvc-score-value tabular-nums" id="jvc-streak">0</strong></span>
    </div>
    <span class="text-muted tabular-nums" id="jvc-progress-label">0%</span>
  </div>
  <div class="progress" role="progressbar" aria-label="Tiến độ của chế độ hiện tại" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100">
    <div class="progress-bar" id="jvc-progress" style="width:0%"></div>
  </div>

  <div class="nav nav-pills nav-justified jvc-modes" role="tablist" aria-label="Chế độ học">
    <button class="nav-link active" id="jvc-tab-flashcard" role="tab" aria-controls="jvc-panel" aria-selected="true" type="button" data-mode="flashcard">01 · Khám phá</button>
    <button class="nav-link" id="jvc-tab-quiz" role="tab" aria-controls="jvc-panel" aria-selected="false" type="button" data-mode="quiz">02 · Gợi nhớ</button>
    <button class="nav-link" id="jvc-tab-cloze" role="tab" aria-controls="jvc-panel" aria-selected="false" type="button" data-mode="cloze">03 · Ngữ cảnh</button>
  </div>

  <section class="card jvc-stage" id="jvc-panel" role="tabpanel" aria-labelledby="jvc-tab-flashcard">
    <div class="jvc-stage-head">
      <div>
        <span class="viz-badge" id="jvc-mode-label">THẺ NHỚ</span>
        <h3 id="jvc-mission">Nhìn kỹ và đoán trước khi lật</h3>
        <div class="text-muted" id="jvc-guide">Tự gọi lại cách đọc và nghĩa trong đầu.</div>
      </div>
      <strong class="tabular-nums" id="jvc-counter">1 / 10</strong>
    </div>
    <hr>
    <div class="jvc-center jvc-content" id="jvc-content"></div>
    <div class="jvc-feedback jvc-center" id="jvc-feedback" aria-live="polite"></div>
    <div class="viz-row jvc-actions" id="jvc-actions"></div>
  </section>

  <script type="application/json" id="jvc-data">__DATA__</script>
  <script>
  (() => {
    const root=document.getElementById('jlpt-vocabulary-quest');
    const payload=JSON.parse(root.querySelector('#jvc-data').textContent);
    const items=payload.items;
    const clozeItems=items.filter(item=>item.cloze);
    const state={
      mode:'flashcard',index:{flashcard:0,quiz:0,cloze:0},flipped:false,answered:false,review:new Set(),
      stats:{flashcard:{done:0,score:0,streak:0,best:0},quiz:{done:0,score:0,streak:0,best:0},cloze:{done:0,score:0,streak:0,best:0}}
    };
    const modeCopy={
      flashcard:{label:'THẺ NHỚ',mission:'Nhìn kỹ và đoán trước khi lật',guide:'Tự gọi lại cách đọc và nghĩa trong đầu.'},
      quiz:{label:'TRẮC NGHIỆM',mission:'Chọn đúng nghĩa của từ',guide:'Đừng đoán vội — hãy đọc từ một lần trước khi chọn.'},
      cloze:{label:'ĐIỀN TỪ',mission:'Hoàn thành câu trong ngữ cảnh',guide:'Đọc trọn câu rồi chọn từ phù hợp nhất.'}
    };
    const q=selector=>root.querySelector(selector);
    q('#jvc-level').textContent=payload.level;
    q('#jvc-size').textContent=`${items.length} từ`;
    q('#jvc-seed').textContent=payload.seed===null?'Theo thứ tự bài':`Seed ${payload.seed}`;

    function source(item){return `${item.source_file}:${item.source_line}`;}
    function currentList(){return state.mode==='cloze'?clozeItems:items;}
    function currentItem(){return currentList()[state.index[state.mode]];}
    function text(tag,value,className){const el=document.createElement(tag);el.textContent=value;if(className)el.className=className;return el;}
    function button(label,className='btn'){const el=document.createElement('button');el.type='button';el.className=className;el.textContent=label;return el;}
    function updateHeader(){
      const copy=modeCopy[state.mode];
      q('#jvc-mode-label').textContent=copy.label;q('#jvc-mission').textContent=copy.mission;q('#jvc-guide').textContent=copy.guide;
      const activeTab=q(`[data-mode="${state.mode}"]`);q('#jvc-panel').setAttribute('aria-labelledby',activeTab.id);
    }
    function updateStats(){
      const stats=state.stats[state.mode];
      q('#jvc-done-label').textContent=state.mode==='flashcard'?'Đã xem':'Đã làm';
      q('#jvc-done').textContent=stats.done;
      q('#jvc-score').textContent=state.mode==='flashcard'?'—':stats.score;
      q('#jvc-streak').textContent=state.mode==='flashcard'?'—':stats.streak;
      const list=currentList(),position=Math.min(state.index[state.mode],list.length);
      const percent=list.length?Math.round((position/list.length)*100):0;
      q('#jvc-progress').style.width=`${percent}%`;q('#jvc-progress-label').textContent=`${percent}%`;
      q('.progress').setAttribute('aria-valuenow',String(percent));
    }
    function resetSurface(){
      q('#jvc-content').replaceChildren();q('#jvc-actions').replaceChildren();
      q('#jvc-feedback').replaceChildren();q('#jvc-feedback').className='jvc-feedback jvc-center';
    }
    function next(){state.index[state.mode]+=1;state.flipped=false;state.answered=false;render();}
    function markCard(item,needsReview){
      state.stats.flashcard.done+=1;if(needsReview)state.review.add(item.word);updateStats();
    }
    function record(correct,item){
      const stats=state.stats[state.mode];stats.done+=1;
      if(correct){stats.score+=1;stats.streak+=1;stats.best=Math.max(stats.best,stats.streak);}else{stats.streak=0;state.review.add(item.word);}updateStats();
    }
    function feedback(correct,item){
      const box=q('#jvc-feedback');box.classList.add(correct?'jvc-success':'jvc-error');
      const streak=state.stats[state.mode].streak;
      const title=correct?(streak>=3?`Tuyệt vời — chuỗi ${streak} câu đúng!`:'Chính xác — bạn đang nhớ rất tốt!'):'Gần đúng rồi — xem lại một lượt nhé.';
      box.append(text('div',title,'jvc-feedback-title'));
      box.append(text('div',`${item.word}（${item.reading}）— ${item.meaning_vi}`));
      box.append(text('div',item.example,'text-muted'));
      box.append(text('div',source(item),'text-small text-muted'));
    }
    function detail(label,value,className){
      const row=document.createElement('div');row.className='jvc-detail-row';
      row.append(text('div',label,'jvc-kicker'),text('div',value,className));return row;
    }
    function renderFlashcard(item){
      const content=q('#jvc-content'),actions=q('#jvc-actions');
      content.append(text('div','TỪ MỚI','jvc-kicker'),text('div',item.word,'jvc-word'));
      if(!state.flipped){
        content.append(text('div','Bạn nhớ cách đọc và ý nghĩa không?','text-muted'));
        const flip=button('Lật thẻ xem đáp án','btn btn-primary');flip.addEventListener('click',()=>{state.flipped=true;render();});actions.append(flip);return;
      }
      const details=document.createElement('div');details.className='jvc-detail';
      details.append(detail('CÁCH ĐỌC',item.reading,'jvc-reading'),detail('Ý NGHĨA',item.meaning_vi,'jvc-meaning'),detail('CÂU MẪU',item.example,'jvc-example'),detail('NGUỒN',source(item),'text-small text-muted'));
      content.replaceChildren(details);
      const review=button('Cần xem lại');review.addEventListener('click',()=>{markCard(item,true);next();});
      const know=button('Mình đã hiểu','btn btn-primary');know.addEventListener('click',()=>{markCard(item,false);next();});actions.append(review,know);
    }
    function renderOptions(item,options,correct){
      const grid=document.createElement('div');grid.className='viz-grid jvc-options';
      options.forEach(value=>{
        const option=button(value,'btn btn-block');
        option.addEventListener('click',()=>{
          if(state.answered)return;state.answered=true;option.setAttribute('aria-pressed','true');
          const isCorrect=value===correct;record(isCorrect,item);feedback(isCorrect,item);
          [...grid.children].forEach(child=>child.disabled=true);
          const go=button('Tiếp tục hành trình','btn btn-primary');go.addEventListener('click',next);q('#jvc-actions').append(go);
        });grid.append(option);
      });q('#jvc-content').append(grid);
    }
    function renderQuiz(item){
      const content=q('#jvc-content');
      content.append(text('div','TỪ NÀY CÓ NGHĨA LÀ GÌ?','jvc-kicker'),text('div',item.word,'jvc-word'));
      renderOptions(item,item.quiz_options,item.meaning_vi);
    }
    function renderCloze(item){
      const content=q('#jvc-content');
      content.append(text('div','CHỌN TỪ HOÀN THÀNH CÂU','jvc-kicker'),text('div',item.cloze,'jvc-example'));
      renderOptions(item,item.cloze_options,item.word);
    }
    function renderComplete(){
      const content=q('#jvc-content');content.className='jvc-complete';
      const wrap=document.createElement('div');
      wrap.append(text('div','HOÀN THÀNH CHẶNG NÀY','jvc-kicker'),text('h2','Bạn đã đi hết một vòng!'));
      const stats=state.stats[state.mode];
      const summary=state.mode==='flashcard'
        ? `Đã xem ${stats.done} từ · ${state.review.size} từ đang cần ôn`
        : `Đúng ${stats.score}/${stats.done} lượt · Chuỗi tốt nhất ${stats.best}`;
      wrap.append(text('p',summary,'jvc-meaning'));
      if(state.review.size){wrap.append(text('p',`Cần ôn: ${[...state.review].slice(0,8).join(' · ')}`,'text-muted'));}
      const again=button('Luyện lại chế độ này','btn btn-primary');again.addEventListener('click',()=>{state.index[state.mode]=0;state.flipped=false;state.answered=false;render();});wrap.append(again);content.append(wrap);
    }
    function render(){
      const list=currentList();resetSurface();q('#jvc-content').className='jvc-center jvc-content';updateHeader();
      if(!list.length){q('#jvc-counter').textContent='0 / 0';q('#jvc-content').append(text('p','Không có câu ví dụ phù hợp để tạo bài điền từ.','jvc-meaning'));updateStats();return;}
      if(state.index[state.mode]>=list.length){q('#jvc-counter').textContent=`${list.length} / ${list.length}`;renderComplete();updateStats();return;}
      const item=currentItem();q('#jvc-counter').textContent=`${state.index[state.mode]+1} / ${list.length}`;
      if(state.mode==='flashcard')renderFlashcard(item);if(state.mode==='quiz')renderQuiz(item);if(state.mode==='cloze')renderCloze(item);updateStats();
    }
    root.querySelectorAll('[data-mode]').forEach(tab=>tab.addEventListener('click',()=>{
      root.querySelectorAll('[data-mode]').forEach(other=>{const active=other===tab;other.classList.toggle('active',active);other.setAttribute('aria-selected',String(active));});
      state.mode=tab.dataset.mode;state.flipped=false;state.answered=false;render();
    }));
    render();
  })();
  </script>
</div>
'''


def main() -> None:
    args = parse_args()
    payload = enrich(load_items(args))
    if not payload["items"]:
        raise SystemExit("No vocabulary rows matched the request")
    encoded = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(FRAGMENT.replace("__DATA__", encoded), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
