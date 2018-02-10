library(pROC)
library(car)
library(dplyr)
emp <- read.csv("../data/train.csv")
emp <- select(emp, -c(X, emp_ID))

CVInd <- function(n,K) {  #n is sample size; K is number of parts; returns K-length list of indices for each part
  m<-floor(n/K)  #approximate size of each part
  r<-n-m*K  
  I<-sample(n,n)  #random reordering of the indices
  Ind<-list()  #will be list of indices for all K parts
  length(Ind)<-K
  for (k in 1:K) {
    if (k <= r) kpart <- ((m+1)*(k-1)+1):((m+1)*k)  
    else kpart<-((m+1)*r+m*(k-r-1)+1):((m+1)*r+m*(k-r))
    Ind[[k]] <- I[kpart]  #indices for kth part of data
  }
  Ind
}

Nrep<-10 #number of replicates of CV
K<-5  #K-fold CV on each replicate
n.models = 3 #number of different models to fit and compare
n=nrow(emp)
y<-emp$left

set.seed(12345)
yhat = matrix(0,n,n.models)
yclass = matrix(0,n,n.models)
AUC <- matrix(0, Nrep, n.models)
CCR_CV = matrix(0,Nrep,n.models)
for (j in 1:Nrep) {
  Ind = CVInd(n,K)
  for (k in 1:K) {
    # model 1
    out<-glm(left~., data = emp[-Ind[[k]],], family = binomial)
    yhat[Ind[[k]],1]<-as.numeric(predict(out,emp[Ind[[k]],], type = "response"))
    yclass[Ind[[k]],1] <- yhat[Ind[[k]],1]>= .5
    
    #model 2
    out<-glm(left~.
             + promotion_last_5years*average_montly_hours
             + promotion_last_5years*time_spend_company, data = emp[-Ind[[k]],], family = binomial)
    yhat[Ind[[k]],2]<-as.numeric(predict(out,emp[Ind[[k]],], type = "response"))
    yclass[Ind[[k]],2] <- yhat[Ind[[k]],2]>= .5
    
    #model 3
    out<-glm(left~.
             + promotion_last_5years*number_project
             + promotion_last_5years*time_spend_company, data = emp[-Ind[[k]],], family = binomial)
    yhat[Ind[[k]],3]<-as.numeric(predict(out,emp[Ind[[k]],], type = "response"))
    yclass[Ind[[k]],3] <- yhat[Ind[[k]],3]>= .5
  } #end of k loop
  #get CV CCR
  CCR_CV[j,] = apply(yclass,2,function(x) mean(y == x))
  #get CV AUC
  roc_obj <- roc(y, yhat[,1])
  AUC[j,1] <- auc(roc_obj)
  roc_obj <- roc(y, yhat[,2])
  AUC[j,2] <- auc(roc_obj)
  roc_obj <- roc(y, yhat[,3])
  AUC[j,3] <- auc(roc_obj)
} #end of j loop
CCR_CV.ave <- apply(CCR_CV,2,mean) #mean of CV correct classification rate
AUC_CV.ave <- apply(AUC,2,mean) #mean of CV AUC
CCR_CV.ave
AUC_CV.ave


#################################################
### Final model
#################################################
fit <- glm(left~.
           + promotion_last_5years*average_montly_hours
           + promotion_last_5years*time_spend_company, data = emp, family = binomial)
summary(fit)
pred <- predict(fit,emp, type = "response")
roc_obj <- roc(emp$left, pred)
auc(roc_obj)
x = roc_obj$sensitivities + roc_obj$specificities
roc_obj$thresholds[which(x == max(x))]
x[which(x == max(x))]
tab <- table(emp$left, pred>.25)
tab[2,2]/(tab[2,2]+tab[2,1]) #TPR
sum(diag(tab))/sum(tab) #CCR

pred[1:2]
