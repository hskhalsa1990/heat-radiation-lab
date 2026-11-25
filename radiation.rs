// Usage: ./radiation  |  ./radiation bench N
const SIGMA: f64 = 5.670374419e-8;
fn flux(e: f64, t: f64, ts: f64) -> f64 { let t2 = t * t; let s2 = ts * ts; e * SIGMA * (t2 * t2 - s2 * s2) }
fn main() {
    let a: Vec<String> = std::env::args().collect();
    if a.len() > 2 && a[1] == "bench" {
        let n: u64 = a[2].parse().unwrap();
        let mut s = 0.0f64;
        for i in 0..n { s += flux(0.8, 300.0 + (i % 900) as f64, 300.0); }
        println!("checksum,{:.6e}", s);
        return;
    }
    for t in (400..=1200).step_by(200) { println!("{},{:.3}", t, flux(0.8, t as f64, 300.0)); }
}
