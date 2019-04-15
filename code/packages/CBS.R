get_ordered_data <- function(test_data, prob, type="CBS"){
	if(length(which(prob >= 0.5)) > 0){
		buggy_data <- test_data[which(prob >= 0.5),]
		ordered_buggy_data <- buggy_data[order(buggy_data$real_la+buggy_data$real_ld),]
		clean_data <- test_data[-which(prob>=0.5),]
		ordered_clean_data <- clean_data[order(clean_data$real_la + clean_data$real_ld),]
		ordered_data <- rbind(ordered_buggy_data, ordered_clean_data)
		return(ordered_data)
	}
	else{
		ordered_data <- test_data[order(test_data$real_la + test_data$real_ld),]
		return(ordered_data)
	}
}
