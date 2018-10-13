%Tim Zaman, TU Delft ME, 01-01-2012
%This code is licensed under a
%Creative Commons Attribution 3.0 Unported License.

clc;clear all;close all

im=imread('IMGP2395.JPG');
im=im(:,:,1);

sigmaA=8;
sigmaB=10;
sigmaMax=max([sigmaA sigmaB]);
fsz=[sigmaMax, sigmaMax];

kernelA=fspecial('gaussian', fsz, sigmaA);
kernelB=fspecial('gaussian', fsz, sigmaB);
%imA = filter2(kernelA, im);
%imB = filter2(kernelB, im);
imA = imfilter(im, kernelA, 'symmetric', 'conv');
imB = imfilter(im, kernelB, 'symmetric', 'conv');


R1=single(im)-single(imA);
%R1=((single(imA)./single(im))-1).*single(imB);
R2=single(imA)-single(imB);

%R1=abs(R1);
%R2=abs(R2);
%R2(R2<1)=1;

R=R1./R2;

% make R rational
R(isnan(R))=0; % replace all nan with 0
R(isinf(R))=0; % replace all inf with 0
Rf=maxfilt2(R,8);
%Rf=max(max(Rf))-Rf;

blurmap=(sigmaA*sigmaB)./((sigmaB-sigmaA)*Rf+sigmaB);

figure;

subplot(3,3,1), imshow(im), title('original')
subplot(3,3,2), imshow(uint8(imA)), title('imA')
subplot(3,3,3), imshow(uint8(imB)), title('imB')
%subplot(3,3,4), imagesc(R1), title('R1')
subplot(3,3,4), imagesc(Rf), title('Rf')
set(gca,'xticklabel',[],'yticklabel',[])
set(gca,'xtick',[],'ytick',[]),axis image
subplot(3,3,5), imagesc(R2), title('R2')
set(gca,'xticklabel',[],'yticklabel',[])
set(gca,'xtick',[],'ytick',[]),axis image
subplot(3,3,6), imagesc(R), title('R')
set(gca,'xticklabel',[],'yticklabel',[])
set(gca,'xtick',[],'ytick',[]),axis image
subplot(3,3,7), imagesc(blurmap), title('blurmap')
set(gca,'xticklabel',[],'yticklabel',[])
set(gca,'xtick',[],'ytick',[]),axis image
subplot(3,3,8), imagesc(blurmap>1 & blurmap<4), title('\sigma [2:4]')
set(gca,'xticklabel',[],'yticklabel',[])
set(gca,'xtick',[],'ytick',[]),axis image
subplot(3,3,9), imagesc(blurmap>0 & blurmap<0.4), title('\sigma [0:0.5]')
set(gca,'xticklabel',[],'yticklabel',[])
set(gca,'xtick',[],'ytick',[]),axis image
