
undersampling <- function(data, class){
	buggy_data <- data[which(data[class][,1] == "buggy"),]
	clean_data <- data[which(data[class][,1] == "clean"),]
	sampled_index <- sample(nrow(clean_data), nrow(buggy_data))
	sampled_data <- clean_data[sampled_index,]
	ret_data <- rbind(buggy_data, sampled_data)
	return(ret_data)
}

