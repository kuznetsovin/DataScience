library("ggplot2")
library("fBasics")
library("scales")
library("dlm")
library("tseries")
library("xts")
library("forecast")
library("lmtest")
library("astsa")

workfile <- file.path("/Users/igorkuznetsov/Projects/DataScience/DataSets/tovar_moving.csv")
datawork <- read.csv(workfile, header = TRUE, sep = ";", quote="\"", dec=".", fill = TRUE, comment.char=""  )

y <- zoo(datawork$qty, as.Date(datawork$date,"%d.%m.%Y"))
w <- period.sum(y, endpoints(y,"weeks"))

plot(w)

log_w <- log(w)
d1 <- diff(log_w, na.pad=FALSE)
ds <- diff(d1, 52, na.pad=FALSE)
ds1 <- diff(ds, 1, na.pad=FALSE)


m <- arima(w, order=c(4,1,13), seasonal=list(order=c(0,1,0), period=52))
tsdiag(m, 100)

