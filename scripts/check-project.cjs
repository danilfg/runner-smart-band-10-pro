const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'src/manifest.json'), 'utf8'));
assert.equal(manifest.router.entry, 'pages/index');
assert.equal(manifest.config.designWidth, 336);
assert.ok(manifest.deviceTypeList.includes('watch'));
const source = fs.readFileSync(path.join(root, 'src/pages/index/index.ux'), 'utf8');
assert.ok(source.includes('export default'));
assert.ok(source.includes('tick()'));
const imagePaths = new Set([...source.matchAll(/['"](\/common\/[^'"\s]+\.png)['"]/g)].map(m => m[1]));
for (const relative of imagePaths) {
  assert.ok(fs.existsSync(path.join(root, 'src', relative.slice(1))), 'Missing asset '+relative);
}
for (const asset of ['hero_boy.png','hero_gecko.png','villain_car.png','city_0.png','city_1.png','coin.png']) {
  assert.ok(fs.statSync(path.join(root,'src/common',asset)).size > 200, asset);
}
console.log('Manifest, routes and '+imagePaths.size+' image references checked.');
