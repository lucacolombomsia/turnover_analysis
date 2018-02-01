library(pROC)
emp <- read.csv("../data/turnover.csv")

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
n.models = 1 #number of different models to fit and compare
n=nrow(emp)
y<-emp$left

yhat=matrix(0,n,n.models)
MSE<-matrix(0,Nrep,n.models)
for (j in 1:Nrep) {
  Ind<-CVInd(n,K)
  for (k in 1:K) {
    out<-glm(left~., data = emp[-Ind[[k]],], family = binomial) #the first model to compare
    yhat[Ind[[k]],1]<-as.numeric(predict(out,emp[Ind[[k]],]))
  } #end of k loop
  MSE[j,]=apply(yhat,2,function(x) sum((y-x)^2))/n
} #end of j loop
MSE
MSEAve<- apply(MSE,2,mean); MSEAve #averaged mean square CV error
MSEsd <- apply(MSE,2,sd); MSEsd   #SD of mean square CV error

yhat=rep(0,n)
#CCR<-matrix(0,Nrep,n.models)
for (j in 1:Nrep) {
  Ind<-CVInd(n,K)
  for (k in 1:K) {
    out<-glm(left~., data = emp[-Ind[[k]],], family = binomial) #the first model to compare
    yhat[Ind[[k]]]<-as.numeric(predict(out,emp[Ind[[k]],], type = "response"))
  } #end of k loop
  CCR[j,]=apply(yhat,2,function(x) sum((y-x)^2))/n
} #end of j loop

roc_obj <- roc(y, yhat)
auc(roc_obj)
roc_obj$thresholds[which.max(roc_obj$sensitivities + roc_obj$specificities)]
names(roc_obj)

#cv_predictions <- data.frame(y = emp$left, yhat = yhat)
tab=table(emp$left, yhat>.45)
tab    
CCR=sum(diag(tab))/sum(tab)
CCR

