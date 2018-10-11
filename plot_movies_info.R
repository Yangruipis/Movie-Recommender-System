df <- read.csv("data/genres_freq.csv")

rotate_x <- function(data, column_to_plot, labels_vec, rot_angle) {
	plt <- barplot(data[[column_to_plot]], col = 'steelblue', xaxt = "n")
	text(plt,
		 par("usr")[3],
		 labels = labels_vec,
		 srt = rot_angle,
		 adj = c(1.1,1.1),
		 xpd = TRUE,
		 cex=0.6)
}
png(file = "figures/genres_hist.png")
rotate_x(df, "freq", df[["genres"]], 45)
dev.off()

pdf(file = "figures/genres_hist.pdf")
rotate_x(df, "freq", df[["genres"]], 45)
dev.off()
