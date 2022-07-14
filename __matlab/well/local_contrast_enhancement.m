%% local contrast enhancement

function corr = local_contrast_enhancement(GRAY)
%

GRAYd = double(GRAY) / 255;

imgtype = 1;
subsamplingrate = 1;

mask = false(size(GRAY(:,:,1)));
mask([1:end],[1,end]) = 1;
mask([1,end],[1:end]) = 1;
MaskFOV = mask;

%fprintf('local contrast enhancement\n');

%figure; imshow(GRAYd);

f = GRAYd;
%f = imfilter(GRAYd, fspecial('gaussian', 3, 1));

if imgtype == 1
    SEsize3 = 35;
else
    SEsize3 = 35;
end
muf = roifilt2(fspecial('average', SEsize3), f, 1-MaskFOV);
%muf = imfilter(f, fspecial('average', SEsize3));
%figure; imshow(mat2gray(muf));

%{
if imgtype == 1
    SEsize4 = 3;
else
    SEsize4 = 3;
end
fmin = ordfilt2(f, 1, true(SEsize4));
fmax = ordfilt2(f, SEsize4^2, true(SEsize4));

figure; imshow(mat2gray(fmin));
figure; imshow(mat2gray(fmax));
%}

umin = 0.0;
umax = 1.0;
tmin = min(min(f));
tmax = max(max(f));
r = 5;
tr = f.^r;
mufr = muf.^r;
tminr = tmin.^r;
tmaxr = tmax.^r;

u2 = (umax - umin)/2.0;

% implemented after Walter & Klein, ISMDA 2002, LNCS 2526, pp. 210-220
% may work with integer intensities, but does not work with [0,1]
%g1 = umin + u2.*(tr - tminr)./(mufr - tminr);
%g2 = umax - u2.*(tr - tmaxr)./(mufr - tmaxr);

% simple local shifts to adjust the mean
% primarily inhomogeneity correction and not contrast enhancement
%g1 = u2+(f-muf);
%g2 = u2+(f-muf);

% basic idea (similar to the one above, but works with any intensity range
g1 = umin + u2.*((f-tmin)./(muf-tmin)).^r;
g2 = umax - u2.*((f-tmax)./(muf-tmax)).^r;

g1(f > muf) = 0;
g2(f <= muf) = 0;
g = g1+g2;

g(MaskFOV) = 0;

corr = uint8(g*255);

%figure; imshow(mat2gray(g1));
%figure; imshow(mat2gray(g2));
%figure; imshow(mat2gray(g));

%figure; imshow(mat2gray(GRAYd ./ corr)); title('G/corr');
%figure; imshow(mat2gray(GRAYd - corr)); title('G-corr');
%figure; imshow(mat2gray(f ./ corr)); title('G/corr');
%figure; imshow(mat2gray(f - corr)); title('G-corr');
