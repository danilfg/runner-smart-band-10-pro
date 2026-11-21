const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const {execFileSync} = require('node:child_process');
const path = require('node:path');
const root=path.resolve(__dirname,'..');
test('game contains two selectable characters and replay', () => {
  const s=fs.readFileSync(path.join(root,'src/pages/index/index.ux'),'utf8');
  for(const token of ['pickBoy()', 'pickGecko()', 'start()', 'finish()', 'storage.set', 'handleSwipe(e)']) assert.ok(s.includes(token));
});
test('static project check passes', () => {
  assert.match(execFileSync(process.execPath,['scripts/check-project.cjs'],{cwd:root,encoding:'utf8'}),/checked/);
});
