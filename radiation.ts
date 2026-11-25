// Compile: npx tsc radiation.ts --outDir /tmp/ts   Run: node /tmp/ts/radiation.js [bench N]
declare const process: { argv: string[] };
const SIGMA: number = 5.670374419e-8;
const flux = (e: number, t: number, ts: number): number => { const t2 = t * t, s2 = ts * ts; return e * SIGMA * (t2 * t2 - s2 * s2); };
const args: string[] = process.argv.slice(2);
if (args[0] === "bench") {
  const n: number = parseInt(args[1], 10); let s: number = 0;
  for (let i = 0; i < n; i++) s += flux(0.8, 300 + (i % 900), 300);
  console.log("checksum," + s.toExponential(6));
} else {
  for (let t = 400; t <= 1200; t += 200) console.log(`${t},${flux(0.8, t, 300).toFixed(3)}`);
}
