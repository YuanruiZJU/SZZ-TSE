

one_way <- function(train_data, test_data, varnames, train_label, label, type){
	mean_scores <- c()
	total_churn <- sum(train_data$la + train_data$ld)
	for (var in varnames){
		ordered_data <- train_data[order(train_data[var][,1]),]
		if (type == "2"){
			results <- calculate_cost_effectiveness2(ordered_data, total_churn, 0.2, "la", "ld", train_label, "buggy")
			recall20 <- results[2]
			mean_scores <- append(mean_scores, recall20)
		}
	}
	best_metric <- varnames[which(max(mean_scores) == mean_scores)]
	ordered_data <- test_data[order(test_data[best_metric][,1]),]
	total_churn2 <- sum(test_data$la + test_data$ld)
	results <- calculate_cost_effectiveness2(ordered_data, total_churn2, 0.2, "la", "ld", label, "buggy")
	precision20 <- results[1]
	recall20 <- results[2]
	F1_score20 <- 2 * precision20 * recall20 / (precision20 + recall20)
	popt_value <- Popt2(ordered_data, total_churn2, "la", "ld", label, "buggy")

	scores <- c(precision20, recall20, F1_score20, popt_value)
	return(scores)
}