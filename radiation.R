# Usage: Rscript radiation.R  |  Rscript radiation.R bench N
sigma <- 5.670374419e-8
flux <- function(e, t, ts) e * sigma * ((t * t)^2 - (ts * ts)^2)
a <- commandArgs(trailingOnly = TRUE)
if (length(a) > 1 && a[1] == "bench") {
  n <- as.integer(a[2]); s <- 0
  for (i in 0:(n - 1)) s <- s + flux(0.8, 300 + (i %% 900), 300)
  cat(sprintf("checksum,%.6e\n", s))
} else {
  for (t in seq(400, 1200, by = 200)) cat(sprintf("%d,%.3f\n", t, flux(0.8, t, 300)))
}
