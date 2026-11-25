// Usage: ./rcpp  |  ./rcpp bench N
#include <cstdio>
#include <cstdlib>
#include <cstring>
constexpr double SIGMA = 5.670374419e-8;
static double flux(double e, double T, double Ts){ double t2=T*T, s2=Ts*Ts; return e*SIGMA*(t2*t2 - s2*s2); }
int main(int argc, char** argv){
  if(argc > 2 && !std::strcmp(argv[1], "bench")){
    long n = std::atol(argv[2]); double s = 0;
    for(long i = 0; i < n; i++) s += flux(0.8, 300.0 + double(i % 900), 300.0);
    std::printf("checksum,%.6e\n", s); return 0;
  }
  for(int T = 400; T <= 1200; T += 200) std::printf("%d,%.3f\n", T, flux(0.8, T, 300.0));
}
