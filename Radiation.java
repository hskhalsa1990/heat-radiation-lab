// Usage: java Radiation  |  java Radiation bench N
import java.util.Locale;
public class Radiation {
    static final double SIGMA = 5.670374419e-8;
    static double flux(double e, double t, double ts) { double t2 = t * t, s2 = ts * ts; return e * SIGMA * (t2 * t2 - s2 * s2); }
    public static void main(String[] a) {
        if (a.length > 1 && a[0].equals("bench")) {
            long n = Long.parseLong(a[1]); double s = 0;
            for (long i = 0; i < n; i++) s += flux(0.8, 300.0 + (double) (i % 900), 300.0);
            System.out.println(String.format(Locale.ROOT, "checksum,%.6e", s)); return;
        }
        for (int t = 400; t <= 1200; t += 200) System.out.println(String.format(Locale.ROOT, "%d,%.3f", t, flux(0.8, t, 300.0)));
    }
}
