close all

t_width = 5; %Time (X Axis) Width, Times Beta (1/14 days)

ps = 0.7;
gam = 1/6;
beta = 1/14;
del = 1/4;
eps = 1/10;
eta = 1/730;
chi = ps*(del - beta) + beta;

%Initial Conditions and Creation of Compartment and Function Arrays
I(1) = 0.005;
di0 = 0;

S(1) = 0.989; %susceptible
E(1) = 0.006;           %exposed
Q(1) = 0;                                   %quarantined
R(1) = 0;                                   %removed
C(1) = I(1);

inputs = {'Interpreter','latex','fontsize',20};
    
for sig = 25
    for k = 0.5
        f = @(t,x)[eta*x(5)/beta - sig*(x(3)+k*x(4))*x(1);
                   sig*(x(3)+k*x(4))*x(1) - gam*x(2)/beta;
                   (gam*x(2) - ps*del*x(3))/beta - (1-ps)*x(3);
                   (ps*del*x(3) - eps*x(4))/beta;
                   (1-ps)*x(3) + (eps*x(4) - eta*x(5))/beta;
                   gam*x(2)/beta]; 
        [ta,xa] = ode45(f,[0,t_width],[S(1),E(1),I(1),Q(1),R(1),C(1)]);
        
        figure(4)
        plot(ta, xa(:,2), '--k', 'LineWidth', 1.5)
        hold on;
        plot(ta, xa(:,3), 'k', 'LineWidth', 1.5)
        hold on;
        plot(ta, xa(:,4), ':k', 'LineWidth', 1.5)
        hold on;
        plot(ta, xa(:,3)+xa(:,4), '-.k', 'LineWidth', 1.5)
        set(gca,'LineWidth',1.5, 'FontSize', 20, 'ticklabelinterpreter', 'latex')
        legend({'$$e(t)$$','$$i(t)$$','$$q(t)$$','$$a(t)$$'}, inputs{:})
        xlabel("$$t$$", inputs{:}), ylabel("Fraction of Population", inputs{:});
        set(gcf,'color','w');
        
        figure(5)
        plot(ta,xa(:,5),'k', 'Linewidth',1.5)
        hold on;
        plot(ta,xa(:,6),'--k','Linewidth',1.5)
        set(gca,'LineWidth',1.5, 'FontSize', 20, 'ticklabelinterpreter', 'latex')
        legend({'$$r(t)$$','$$c(t)$$'}, inputs{:})
        xlabel("$$t$$", inputs{:}), ylabel("Fraction of Population", inputs{:});
        set(gcf,'color','w');
    end
end

%{
figure(1)
plot(ta, xa(:,3), 'k','linewidth',1.5);
hold on;
xlabel("$$t$$", inputs{:});
ylabel("$$i(t)$$", inputs{:});
set(gcf,'color','w');
set(gca,'FontSize', 20,'LineWidth',1.5, 'ticklabelinterpreter', 'latex')
annotation('arrow',[.360 .28],[.27 .77],'linewidth',4);

figure(2)
plot(ta, xa(:,6),'k','linewidth',1.5)
hold on;
xlabel('$$t$$',inputs{:}), ylabel('$$c(t)$$',inputs{:})
annotation('arrow',[.85 .85],[.35 .75],'linewidth',4);
set(gca,'FontSize', 20,'LineWidth',1.5, 'ticklabelinterpreter', 'latex')
set(gcf,'color','w');

figure(3)
rt = smoothdata((gam*xa(:,2))./(chi*xa(:,3)),'gaussian');
plot(ta, rt,'k', 'linewidth',1.5)
xlabel('$$t$$',inputs{:}), ylabel('$$R_{t}$$',inputs{:})
yline(1,'--');
hold on;
set(gca,'LineWidth',1.5, 'FontSize', 20, 'ticklabelinterpreter', 'latex')
set(gcf,'color','w');

figure(4)
plot(ta, xa(:,2), '--k', 'LineWidth', 1.5)
hold on;
plot(ta, xa(:,3), 'k', 'LineWidth', 1.5)
hold on;
plot(ta, xa(:,4), ':k', 'LineWidth', 1.5)
hold on;
plot(ta, xa(:,5), '-.k', 'LineWidth', 1.5)
set(gca,'LineWidth',1.5, 'FontSize', 20, 'ticklabelinterpreter', 'latex')
set(gcf,'color','w');

xlabel("$$t$$", inputs{:});
ylabel("Fraction of Population", inputs{:});
legend({'$$e(t)$$','$$i(t)$$','$$q(t)$$','$$r(t)$$'}, inputs1{:})
%}

clear all
