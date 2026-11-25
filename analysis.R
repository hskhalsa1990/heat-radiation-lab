# R analysis of the cleaned dataset
d <- read.csv("emissivity_clean.csv")
print(aggregate(flux_Wm2 ~ material, d, mean))
fit <- lm(flux_Wm2 ~ I(temp_K^4) * emissivity, data = d)
cat("R-squared:", summary(fit)$r.squared, "\n")
png("fig_r_boxplot.png", 900, 550)
boxplot(flux_Wm2 ~ material, d, las = 2, col = "orange", main = "Flux by material (R)")
dev.off()
