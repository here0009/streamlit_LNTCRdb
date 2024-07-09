#!/haplox/users/donglf/miniconda3/envs/r_env/bin/Rscript
# ref: https://machinelearningmastery.com/feature-selection-with-the-caret-r-package/
# ref: https://www.machinelearningplus.com/machine-learning/feature-selection/
# ref: https://www.datacareer.ch/blog/ridge-and-lasso-in-r/
# ref : https://remiller1450.github.io/s230f19/caret1.html

library(caret)
library(pROC)
library(doSNOW)
library(tidyverse)
library(gbm)
library(randomForest)
# library(kernlab)
set.seed(77) 

args <- commandArgs(trailingOnly = TRUE)

test_file <- args[1]
print(test_file)
output_dir <- args[2]
threads <- as.integer(args[3])
model_file <- args[4]
feature_file <- args[5]
tag <- args[6]
pred_type <- args[7]

print(pred_type)


control <- "Benign"
cancer <- "Malignant"
lines <- c()
cl <- makeCluster(threads, type = "SOCK")
registerDoSNOW(cl)


qc_filter2 = function(input_table, pred_type){
  print('records before filter:')
  print(dim(input_table)[1])
  if (pred_type == 'type'){
    input_table <- input_table[which(input_table$Type == cancer | input_table$Type == control), ] # should use which here
  }
  print('records after filter:')
  print(dim(input_table)[1])
  input_table <- input_table %>% mutate_at(stat_cols, ~replace_na(., 0))
  input_table <- input_table %>% mutate_at(stat_cols, ~replace(., . == '',0)) # replace black values with 0
  input_table <- as.data.frame(input_table)
  if (pred_type == 'type'){
    input_table$Type <- relevel(as.factor(input_table$Type), cancer, levels= c(control,cancer))
  }
  input_table
}

get_best_result = function(caret_fit) {
  best = which(rownames(caret_fit$results) == rownames(caret_fit$bestTune))
  best_result = caret_fit$results[best, ]
  rownames(best_result) = NULL
  best_result
}


model_train = function(X, y, method){
# Register cluster so that caret will know to train in parallel.
  model <- caret::train(X, y, method = method,preProcess = c("corr", "nzv", "center", "scale"),metric = "ROC",trControl = ctrl)
  print(model)
  print(varImp(model))
  print(confusionMatrix(model, mode='everything', positive=cancer))
  model
}



model_test_val = function(model, X){
  test_pred <- predict(model, X, type='prob')
  test_pred
}


get_roc_auc = function(test_pred, y){
  roc_auc <- roc(predictor=test_pred[[cancer]], response=y, levels= c(control,cancer), direction = "<", quiet = FALSE)
  roc_auc
}

get_ci_roc_auc = function(test_pred, y){
    set.seed(77)
    ci_auc <- ci.auc(predictor=test_pred[[cancer]], response=y, levels= c(control,cancer), direction = "<", quiet = FALSE, , conf.level=0.95, method='bootstrap')
    ci_auc
}


model_test_val_total = function(models_list, data, tag){
  sprintf("%d Samples for Test Data", dim(data)[1])
  svg(file.path(output_dir, paste0(tag, "_roc.svg")), bg=NA)
  dpi = 600
  # png(file.path(output_dir, paste0(tag, ".png")), width = 8*dpi, height = 8*dpi, res = dpi)
  color_palettes <- c('blue', 'red', 'green', 'yellow', 'violet')
  pred_val_matrix <- c()
  if ("Name" %in% names(data)){
    pred_val_df <- data %>% select("Sample_ID", "Type", "Name")
  }
  else{
    pred_val_df <- data %>% select("Sample_ID", "Type")
  }
  # 
  i <- 0
  total_metrics <- c()
  for (model_name in names(models_list)){
    print(model_name)
    i <- i + 1
    model <- models_list[[model_name]]
    # models_list$model_name
    pred_val <- model_test_val(model, data[,stat_cols])
    pred_val_df$Score <- pred_val[[cancer]]
    names(pred_val_df)[dim(pred_val_df)[2]] = model_name # rename the last col to model name, can not directly assign virable as col name in R ...
    roc_auc <- get_roc_auc(pred_val, data$Type)
    print(roc_auc)
    model_auc_metrics <- as.matrix(roc_auc$auc)
    total_metrics <- cbind(total_metrics, model_auc_metrics)
    if (i == 1) {
      plot(roc_auc, col = color_palettes[[i]])
      }
    else
    {
      lines(roc_auc, col = color_palettes[[i]])
    }
  }
  total_metrics <- format(round(total_metrics, 2))
  notes <- c(paste(names(models_list), total_metrics))
  legend("bottomright", legend = notes, col = color_palettes, lty = 1)
  dev.off()
  colnames(total_metrics) <- c('TCRnodseekPlus','randomForest', 'gbm', 'svmLinear', 'svmRadial')
  write.csv(total_metrics,file.path(output_dir, paste0(tag, "_roc.csv")),row.names=FALSE, quote=FALSE)
  write.csv(pred_val_df,file.path(output_dir, paste0(tag, "_pred_val.csv")),row.names=FALSE, quote=FALSE)
}

model_test_val_score = function(models_list, data, tag){
  sprintf("%d Samples for Test Data", dim(data)[1])
  pred_val_matrix <- c()
  if ("Name" %in% names(data)){
    pred_val_df <- data %>% select("Sample_ID", "Name")
  }
  else{
    pred_val_df <- data %>% select("Sample_ID")
  }
  total_metrics <- c()
  for (model_name in names(models_list)){
    print(model_name)
    model <- models_list[[model_name]]
    # models_list$model_name
    pred_val <- model_test_val(model, data[,stat_cols])
    pred_val_df$Score <- pred_val[[cancer]]
    names(pred_val_df)[dim(pred_val_df)[2]] = model_name # rename the last col to model name, can not directly assign virable as 
  write.csv(pred_val_df,file.path(output_dir, paste0(tag, "_pred_val.csv")),row.names=FALSE, quote=FALSE)
  }
}


model_test_group = function(model, X, y){
  test_pred <- predict(model, X)
  cm <- confusionMatrix(reference = y, data = test_pred, mode='everything', positive=cancer)
}


model_test_group_total = function(models_list, data, tag)
{
  # for test data
  sprintf("The Predicted Confusion matrix for %s samples", tag)
  sprintf("%d Samples for Test Data", dim(data)[1])
  total_metrics <- c()
  for (model_name in names(models_list)){
    print(model_name)
    model <- models_list[[model_name]]
    # models_list$model_name
    model_cm <- model_test_group(model, data[,stat_cols], data$Type)
   
    model_cm_metrics <- as.matrix(model_cm$byClass)
    total_metrics <- cbind(total_metrics, model_cm_metrics)
  }
  colnames(total_metrics) <- c('TCRnodseekPlus','randomForest', 'gbm', 'svmLinear', 'svmRadial')
  write.csv(total_metrics,file.path(output_dir, paste0(tag, "_model_metric.csv")),row.names=TRUE, quote=FALSE)
}

test_data <- read_csv(test_file)
models_list <- readRDS(model_file)
feature_table <- read_csv(feature_file)


features <- as.vector(unlist(feature_table['feature']))
# cols <- get_selected_features(features, 10)
stat_cols <- intersect(features, colnames(test_data))
print('Features for prediction')
print(stat_cols)
missing_features <-  setdiff(features, stat_cols)
print('The following features were missing:')
print(missing_features)


test_data <- qc_filter2(test_data,pred_type)
sample_type_counts <- c()
sample_type_counts <- cbind(sample_type_counts, table(test_data$Type))
print(sample_type_counts)

# models_list <- readRDS(file.path(output_dir, "models_list.rds"))

# for trainning data
print('The Predicted Confusion matrix for Test samples, total sample:')
sprintf("%d Samples for Test Data", dim(test_data)[1])

if ( pred_type == 'type' ){
  # prediction output is probability
  model_test_val_total(models_list, test_data, tag)
  # prediction output is class
  model_test_group_total(models_list, test_data, tag)
}else {
  model_test_val_score(models_list, test_data, tag)
}
stopCluster(cl)
