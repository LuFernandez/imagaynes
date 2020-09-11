clear all;
close all;

h = fspecial('unsharp')            %% Hi pass

freqz2(h);

% construyo una imagen (que es una delta en 0)
% suficientemente grande para poder ver bien el espectro

N=256;
big=zeros(N);       %make a big image
big(N/2,N/2)=1;     %unit impulse

h1=conv2(big,h);    %make conv with the filter ==> 

figure
S = fft2(h1);       %Spectrum
SM=abs(S);          %Modulo
imshow(fftshift(SM/max(max(SM)))); % show spect

figure
IMd = log(1+abs(SM));
imshow(fftshift(IMd/max(max(IMd)))); % show spect log scale
