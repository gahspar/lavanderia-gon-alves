import { cp, mkdir, readFile, rm } from 'node:fs/promises';
import { basename, dirname, join, resolve } from 'node:path';

const root = resolve(import.meta.dirname);
const dist = join(root, 'dist');

if (dirname(dist) !== root || basename(dist) !== 'dist') {
  throw new Error('Diretório de saída inválido.');
}

await rm(dist, { recursive: true, force: true });
await mkdir(join(dist, 'assets'), { recursive: true });

for (const file of ['index.html', 'styles.css', 'script.js', 'favicon.svg', 'robots.txt']) {
  await cp(join(root, file), join(dist, file));
}

await cp(join(root, 'assets'), join(dist, 'assets'), { recursive: true });

const index = await readFile(join(dist, 'index.html'), 'utf8');
if (!index.includes('Lavanderia Gonçalves & Duwe')) {
  throw new Error('A página principal não foi gerada corretamente.');
}

console.log('Build concluído em dist/');
