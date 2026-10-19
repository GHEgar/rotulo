import { mkdirSync, readdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { basename, join, resolve } from 'node:path';
import { promisify } from 'node:util';
import fontnik from 'fontnik';

const load = promisify(fontnik.load);
const range = promisify(fontnik.range);

const [source = '../build/map', target = 'glyphs'] = process.argv.slice(2);
const fonts = readdirSync(source).filter((file) => file.endsWith('.ttf')).sort();

if (fonts.length === 0) {
    console.error(`No TTF files in ${resolve(source)}`);
    process.exit(1);
}

rmSync(target, { recursive: true, force: true });

for (const file of fonts) {
    const font = readFileSync(join(source, file));
    const [face] = await load(font);
    const starts = [...new Set(face.points.map((point) => point - (point % 256)))].sort((a, b) => a - b);
    const fontstack = basename(file, '.ttf').replace('-', ' ');
    const dir = join(target, fontstack);
    mkdirSync(dir, { recursive: true });
    for (const start of starts) {
        const end = start + 255;
        writeFileSync(join(dir, `${start}-${end}.pbf`), await range({ font, start, end }));
    }
    console.log(`${dir}: ${face.points.length} glyphs in ${starts.length} ranges`);
}
