library("pROC")
library("randomForest")
library("reshape")
library("e1071")
library("ScottKnottESD")
library("caret")

source("C://Users/yuanruifan/bitbucket/jit_defect_prediction/classification/packages/measures.R")

szz_baseline <- "buggy_RA"


predict_type <- c("prob", "response", "prob")
names(predict_type) <- c("random_forest", "logistic_regression", "naive_bayes")

probability <- function(prediction, model_type){
	if (model_type %in% c("random_forest", "naive_bayes")){
		v <- prediction[,2]
	}
	else{
		v <- prediction
	}
	return(v)
}

VarImportance <- function(model, model_type, varnames, test_set){
	n_instances <- nrow(test_set)
	prediction <- predict(model, test_set, type=predict_type[model_type])
	prob <- probability(prediction, model_type)
	clean_acc <- accuracy(test_data, prob, label=szz_baseline)
	acc_diff_vec <- c()
	for (var in varnames){
		temp_set <- test_set
		temp_set[var][,1] <- sample(temp_set[var][,1], n_instances)

		temp_prediction <- predict(model, temp_set, type=predict_type[model_type])
		temp_prob <- probability(temp_prediction, model_type)
		temp_acc <- accuracy(test_data, temp_prob, label=szz_baseline)
		acc_diff_vec <- append(acc_diff_vec, clean_acc - temp_acc) 
	}
	return(acc_diff_vec)
}

