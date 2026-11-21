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

test('exit button and edge-back terminate the app from menu', () => {
  const source=fs.readFileSync(path.join(root,'src/pages/index/index.ux'),'utf8');
  const manifest=JSON.parse(fs.readFileSync(path.join(root,'src/manifest.json'),'utf8'));
  assert.match(source, /@click="exitGame"/);
  assert.match(source, /import app from '@system.app'/);
  assert.match(source, /app\.terminate\(\)/);
  assert.match(source, /if \(e\.direction === 'right'\)/);
  assert.match(source, /onBackPress\(\)/);
  assert.ok(manifest.features.some((f) => f.name === 'system.app'));
});
