function [MSE] = MSELoss(cases,model)
%OPTIMIZE Summary of this function goes here
%   Detailed explanation goes here
a = zeros(1,length(cases));
for i = 1:length(cases)
    a(1, i) = (model(i)-cases(i))^2;
end
MSE = mean(a(1,:));
end

