library("ggplot2")
library("scales")
library("dlm")
library("tseries")
library("xts")
library("forecast")
library("lmtest")
library("astsa")

#sarima(w, 1,1,1,0,1,0, 52)
#arima(w, order=c(2,1,1), seasonal=list(order=c(1,0,2), period=52))
#arima(w, order=c(7,1,6), seasonal=list(order=c(1,1,1), period=52))

tsd <- function(x, lag=1){na.remove(diff(x, lag))}
workfile <- file.path("D:/Scripts/DataScience/DataSets/tovar_moving.csv")
datawork <- read.csv(workfile, header = TRUE, sep = ";", quote="\"", dec=".", fill = TRUE, comment.char=""  )

y <- zoo(datawork$qty, as.Date(datawork$date,"%d.%m.%Y"))
w <- period.sum(y, endpoints(y,"weeks"))

plot(w)

log_w <- log(w)
d1 <- diff(log_w, na.pad=FALSE)
ds <- diff(d1, 52, na.pad=FALSE)
ds1 <- diff(d1, 1, na.pad=FALSE)

#summary(arma(ds1,lag=list(ar=c(1:6,49,50),ma=c(1,2,51,52)),include.intercept=FALSE))
#L(103, 101, 59, 54, 53, 52, 51, 49, 7, 1) - AR
#L(103, 101, 54, 53, 2, 1) - MA

m <- arima(w, order=c(7,1,6), seasonal=list(order=c(1,1,1), period=52))
#(1-pnorm(abs(m$coef)/sqrt(diag(m$var.coef))))*2 #p-value для коэффициентов

#normalTest(m$residuals) # распределение остатков не нормальное
#gqtest(m$residuals ~ 1) # остатки гетероскедастичны
#bgtest(m$residuals ~ 1) # автокорреляция в остатках отсутсвует