library("scoring")
library(SDMTools)


precision <- function(test_data, prob, label){
	obs <- as.numeric(test_data[label][,1] == "buggy")
	confusion_matrix <- confusion.matrix(obs, prob)
	tp <- confusion_matrix[2,2]
	fp <- confusion_matrix[2,1]
	return(tp/(tp+fp))
}

recall <- function(test_data, prob, label){
	obs <- as.numeric(test_data[label][,1] == "buggy")
	confusion_matrix <- confusion.matrix(obs, prob)
	tp <- confusion_matrix[2,2]
	fn <- confusion_matrix[1,2]
	return(tp/(tp+fn))
}

F1 <- function(test_data, prob, label){
	prec <- precision(test_data, prob, label)
	rec <- recall(test_data, prob, label)
	f1_value <- 2 * prec * rec / (prec + rec)
	return(f1_value)
}

accuracy <- function(test_data, prob, label){
	obs <- as.numeric(test_data[label][,1] == "buggy")
	confusion_matrix <- confusion.matrix(obs, prob)
	tp <- confusion_matrix[2,2]
	tn <- confusion_matrix[1,1]
	acc <- (tp + tn) / nrow(test_data)
	return(acc)
}

gmean <- function(test_data, prob, label){
	obs <- as.numeric(test_data[,label] == "buggy")
	confusion_matrix <- confusion.matrix(obs, prob)
	tp <- confusion_matrix[2,2]
	tn <- confusion_matrix[1,1]
	fp <- confusion_matrix[2,1]
	fn <- confusion_matrix[1,2]
	gmean_result <- sqrt(tp*tn/(tp+fn)/(tn+fp))
	return(gmean_result)
}


waste_miss <- function(test_data, prob, label){
	obs <- as.numeric(test_data[,label] == "buggy")
	confusion_matrix <- confusion.matrix(obs, prob)
	fp <- confusion_matrix[2,1]
	fn <- confusion_matrix[1,2]
	false_positive_indexes <- which(prob >= 0.5 & obs == 0)
	predicted_buggy_indexes <- which(prob >= 0.5)
	temp_data <- test_data[false_positive_indexes,] 
	predicted_buggy_data <- test_data[predicted_buggy_indexes,]
	waste_effort <- sum(temp_data$real_la + temp_data$real_ld)
	all_effort <- sum(predicted_buggy_data$real_la + predicted_buggy_data$real_ld)
	return(c(fp, fn, waste_effort, all_effort, waste_effort / all_effort))
}



# Using built-in methods in R, much faster!!!
calculate_cost_effectiveness2 <- function(ordered_data, total_churn, cut_off, var_la, var_ld, label, label_val){
	cum_loc <- cumsum(ordered_data[var_la][,1]+ordered_data[var_ld][,1])
	cum_ratio <- cum_loc / total_churn
	cut_index <- which(cum_ratio <= cut_off)
	inspected_data <- ordered_data[cut_index,]
	buggy_index <- which(inspected_data[label][,1] == label_val)
	inspected_num <- length(cut_index)
	buggy_num <- length(buggy_index)
	all_buggy_num <- length(which(ordered_data[label][,1] == label_val))
	results <- c(buggy_num/inspected_num, buggy_num/all_buggy_num)
	return(results)
}

