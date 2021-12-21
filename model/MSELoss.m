function [MSE] = MSELoss(cases,model)
    %Calculuates the mean squared error of case data relative to the predicted model data
    a = zeros(1,length(cases));
    for i = 1:length(cases)
        a(1, i) = (model(i)-cases(i))^2;
    end
    MSE = mean(a(1,:));
end

