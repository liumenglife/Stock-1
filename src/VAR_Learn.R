library(vars)
data(Canada)
def.par <- par(no.readonly = TRUE)
Canada = as.data.frame(Canada)
layout(matrix(1:4, nrow=2, ncol=2))
plot.ts(Canada["e"], main="Employment", ylab="", xlab="")
plot.ts(Canada["prod"], main="Productivity", ylab="", xlab="")
plot.ts(Canada["rw"], main="Real Wage", ylab="", xlab="")
plot.ts(Canada["U"], main="Unemployment Rate", ylab="", xlab="")

VARselect(Canada, lag.max=5, type='const')

var.2c <- VAR(Canada, p=2, type = "const")
names(var.2c)
summary(var.2c)
plot(var.2c)

